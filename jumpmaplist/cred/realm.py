from twisted.cred.portal import IRealm
from twisted.internet.defer import maybeDeferred
from twisted.web.resource import IResource
from zope.interface import implements

from jumpmaplist.cred.guard import ExpireTokenResource
from jumpmaplist.routers import PublicRouter, PrivateRouter
from jumpmaplist.resource import ApplicationElement, LoginElement
from jumpmaplist.util import ContentTypeRouter, LeafRenderableResource



class MapListRealm(object):
    implements(IRealm)

    def __init__(self, database, jsPath, steamAPI, redirectTo):
        self.db = database
        self.jsPath = jsPath or 'https://static.tempus.xyz/maplist/js'
        self.steamAPI = steamAPI
        self.redirectTo = redirectTo


    def anonymous(self):
        html = LeafRenderableResource(LoginElement())
        json = PublicRouter(self.db)

        return ContentTypeRouter([
            ('text/html', html),
            ('application/json', json)
        ])


    def registered(self, avatarId):
        # steam:XXXXXXXXXXXXXXXXX
        steamID = int(avatarId[6:])
        user = self.db.users.get(steamID)
        if not user:
            return ExpireTokenResource(self.redirectTo)

        html = LeafRenderableResource(ApplicationElement(steamID, self.jsPath,
                                                         user.superuser))
        json = PrivateRouter(self.db, steamID, self.steamAPI)

        return ContentTypeRouter([
            ('text/html', html),
            ('application/json', json)
        ])


    def requestAvatar(self, avatarId, mind, *interfaces):
        if IResource in interfaces:
            if avatarId:
                d = maybeDeferred(self.registered, avatarId)
            else:
                d = maybeDeferred(self.anonymous)
            return d.addCallback(
                lambda avatar: (IResource, avatar, lambda: None))
        raise NotImplementedError()
