from axiom.store import Store

from valve.steam.api.interface import API

from twisted.application import strports
from twisted.application.service import IServiceMaker
from twisted.cred.checkers import AllowAnonymousAccess
from twisted.cred.portal import Portal
from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.python.filepath import FilePath
from twisted.web.server import Session, Site
from zope.interface import implements

from jumpmaplist.cred.guard import HTTPOpenIDAuthSessionWrapper
from jumpmaplist.cred.realm import MapListRealm
from jumpmaplist.cred.checkers import PreauthenticatedChecker
from jumpmaplist.database import Database



class Options(usage.Options):
    optParameters = (
        [ ['strport', 'sp', None, 'Strport description. eg. "tcp:1337:interface=127.0.0.1"']
        , ['dbdir', 'd', None, 'Database directory path. eg. "jumpmaplist.axiom"']
        , ['bundle-path', 'b', None, 'Bundle path']
        , ['steamkey', None, 'Steam web API key.']
        ])



class MapListServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    tapname = 'jump-map-list'
    description = 'jump.tf map list service.'
    options = Options

    def makeService(self, options):
        class LongSession(Session):
            sessionTimeout = 3600

        if options['steamkey'] is None:
            raise ValueError('Must specify steam API key.')
        if options['strport'] is None:
            raise ValueError('Must specify strport description.')
        if options['dbdir'] is None:
            raise ValueError('Must specify database path.')
        steamAPI = API(key=options['steamkey'])

        store = Store(options['dbdir'])
        keyPath = FilePath(options['dbdir']).child('fernet.key')

        database = Database(store)

        loginRedirect = '/'
        portal = Portal(MapListRealm(database, options['bundle-path'],
                                     steamAPI, loginRedirect))
        portal.registerChecker(PreauthenticatedChecker())
        portal.registerChecker(AllowAnonymousAccess())

        root = HTTPOpenIDAuthSessionWrapper(portal, [], loginRedirect, keyPath,
                                            database)

        site = Site(root)
        site.sessionFactory = LongSession
        return strports.service(options['strport'], site)



serviceMaker = MapListServiceMaker()
