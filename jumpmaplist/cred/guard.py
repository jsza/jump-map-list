import json

from cryptography.fernet import Fernet, InvalidToken

from openid.consumer import consumer
from openid.store.memstore import MemoryStore
from openid.yadis.discover import DiscoveryFailure

from twisted.internet.defer import DeferredSemaphore
from twisted.internet.threads import deferToThread
from twisted.python.urlpath import URLPath
from twisted.web import http
from twisted.web.guard import HTTPAuthSessionWrapper
from twisted.web.resource import Resource, IResource, ForbiddenResource
from twisted.web.static import Data
from twisted.web.template import renderElement
from twisted.web.util import Redirect, DeferredResource

from jumpmaplist.cred.credentials import Preauthenticated
from jumpmaplist.util import getUrlForRequest



class OpenIDEndpoint(Resource):
    def __init__(self, providerURL, store, semaphore, loginCallback):
        Resource.__init__(self)
        self.providerURL = providerURL
        self.store = store
        self.loginCallback = loginCallback
        self.semaphore = semaphore


    def getConsumer(self, request):
        return consumer.Consumer({'id': request.getSession().uid}, self.store)


    def getChild(self, name, request):
        if name == 'login':
            return self.handleLogin(request)
        elif name == 'process':
            return self.handleProcess(request)


    def handleLogin(self, request):
        path = URLPath.fromBytes(getUrlForRequest(request))

        def _tx():
            oidconsumer = self.getConsumer(request)
            oidrequest = oidconsumer.begin(self.providerURL)
            return oidrequest.redirectURL(str(path.parent()),
                                          str(path.sibling('process')),
                                          immediate=False)

        def _eb(failure):
            failure.trap(DiscoveryFailure)
            request.setResponseCode(http.SEVICE_UNAVAILABLE)
            return Data('Steam login service unavailable.', 'text/plain')

        d = self.semaphore.run(deferToThread, _tx)
        d.addCallback(Redirect)
        d.addErrback(_eb)
        return DeferredResource(d)


    def handleProcess(self, request):
        path = URLPath.fromBytes(getUrlForRequest(request))
        args = {k: v[0] for k, v in request.args.iteritems()}
        oidconsumer = self.getConsumer(request)

        def _cb(info):
            if info.status == consumer.FAILURE:
                request.setResponseCode(http.UNAUTHORIZED)
                return Data('Login failed', 'text/plain')

            ident = info.getDisplayIdentifier()
            return self.loginCallback(request, ident)

        d = self.semaphore.run(oidconsumer.complete, args, str(path))
        d.addCallback(_cb)
        return DeferredResource(d)



class HTTPOpenIDAuthSessionWrapper(HTTPAuthSessionWrapper):
    """
    Wrap a portal, enforcing supported header-based authentication schemes.

    Also provides OpenID login handlers.
    """

    cookieName = 'MAP_LIST_AUTH'
    sessionTimeout = 604800

    def __init__(self, portal, credentialFactories, redirectTo, keyPath,
                 db):
        HTTPAuthSessionWrapper.__init__(self, portal, credentialFactories)
        self.openIDStore = MemoryStore()
        self.loginSemaphore = DeferredSemaphore(1)
        self.redirectTo = redirectTo
        self.db = db
        if keyPath.exists():
            self.fernet = Fernet(keyPath.getContent())
        else:
            key = Fernet.generate_key()
            keyPath.setContent(key)
            self.fernet = Fernet(key)


    def getChildWithDefault(self, name, request):
        if name == 'openid':
            return OpenIDEndpoint('https://steamcommunity.com/openid',
                                  self.openIDStore, self.loginSemaphore,
                                  self._steamLogin)
        if name == 'logout':
            # Delete auth cookie
            request.addCookie(self.cookieName, '',
                              path=b'/', max_age=0)
            request.getSession().expire()
            return Redirect(self.redirectTo)
        return HTTPAuthSessionWrapper.getChildWithDefault(self, name, request)


    def _authorizedResource(self, request):
        token = request.getCookie(self.cookieName)
        if token is None:
            return HTTPAuthSessionWrapper._authorizedResource(self, request)

        try:
            username = self.decryptToken(token)
        except InvalidToken:
            request.addCookie(self.cookieName, '',
                  path=b'/', max_age=0)
            return HTTPAuthSessionWrapper._authorizedResource(self, request)

        def _cb((interface, avatar, logout)):
            return avatar

        credentials = Preauthenticated(username)
        d = self._portal.login(credentials, None, IResource)
        d.addCallback(_cb)
        return DeferredResource(d)


    def _steamLogin(self, request, claimedID):
        prefix = 'http://steamcommunity.com/openid/id/'
        if claimedID.startswith(prefix):
            steamID = int(claimedID[len(prefix):])
        else:
            # This should never occur unless Valve changes the ID format
            raise ValueError('Claimed ID is invalid: {}'.format(claimedID))

        if not self.db.users.get(steamID):
            # If no users exist, grant superuser access to first login.
            if self.db.users.count() == 0:
                self.db.users.add(steamID=steamID, superuser=True)
            else:
                return ForbiddenResource('You are not authorized to access this site.')

        token = self.makeToken(steamID)

        request.addCookie(self.cookieName, token, path=b'/',
                          max_age=self.sessionTimeout)
        return Redirect(self.redirectTo)


    def makeToken(self, steamID):
        if not isinstance(steamID, (int, long)):
            raise ValueError(
                'Steam ID must be an int, got {!r}'.format(steamID))
        authid = u'steam:{:d}'.format(steamID)
        return self._generateToken(authid)


    def decryptToken(self, token):
        auth = self._loadToken(token.encode('ascii'))
        return auth['username']


    def _loadToken(self, token):
        return json.loads(self.fernet.decrypt(token, ttl=self.sessionTimeout))


    def _generateToken(self, username):
        # sanity check
        if not username.startswith('steam:'):
            raise ValueError('Username must start with {!r}, got {!r}'.format(
                'steam:', username))
        data = json.dumps({'username': username})
        return self.fernet.encrypt(data)



class ElementRenderer(Resource):
    def __init__(self, element):
        self.element = element


    def render(self, request):
        return renderElement(request, self.element)



class ExpireTokenResource(Resource):
    isLeaf = True

    def __init__(self, redirectTo):
        self.redirectTo = redirectTo


    def render(self, request):
        request.addCookie(HTTPOpenIDAuthSessionWrapper.cookieName, b'',
                          path=b'/', max_age=0)
        return Redirect(self.redirectTo).render(request)
