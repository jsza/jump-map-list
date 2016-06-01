from axiom.store import Store

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
from jumpmaplist.items import Level



class Options(usage.Options):
    optParameters = (
        [ ['strport', 'sp', None, 'Strport description. eg. "tcp:1337:interface=127.0.0.1"']
        , ['dbdir', 'd', None, 'Database directory path.']
        , ['bundle-path', 'b', None, 'Bundle path']
        ])



class MapListServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    tapname = 'jump-map-list'
    description = 'jump.tf map list service.'
    options = Options

    def makeService(self, options):
        # author = Author(store=s, name=u'jayess', steamID=123)
        # la = LevelAuthor(store=s, author=author, level=level)
        # print(s.query(LevelAuthor, LevelAuthor.author == author).count())
        # la.deleteFromStore()
        # print(s.query(LevelAuthor, LevelAuthor.author == author).count())
        # return MultiService()

        class LongSession(Session):
            sessionTimeout = 3600

        store = Store(options['dbdir'])
        keyPath = FilePath(options['dbdir']).child('fernet.key')

        portal = Portal(MapListRealm(store, options['bundle-path']))
        portal.registerChecker(PreauthenticatedChecker())
        portal.registerChecker(AllowAnonymousAccess())

        root = HTTPOpenIDAuthSessionWrapper(portal, [], '/', keyPath)

        site = Site(root)
        site.sessionFactory = LongSession
        return strports.service(options['strport'], site)



serviceMaker = MapListServiceMaker()
