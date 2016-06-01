from twisted.web.static import Data

from txspinneret.route import Router, routedResource

from jumpmaplist.items import Author
from jumpmaplist.routers.authors import AuthorsRouter
from jumpmaplist.routers.levels import LevelsRouter



@routedResource
class PublicRouter(object):
    router = Router()

    def __init__(self, store):
        self.store = store


    @router.subroute('list')
    def list(self, request, params):
        result = self.store.query(Author).count()
        return Data(str(result), 'text/plain')



@routedResource
class PrivateRouter(object):
    router = Router()

    def __init__(self, store, steamID):
        self.store = store
        self.steamID = steamID


    @router.subroute('authors')
    def authors(self, request, params):
        return AuthorsRouter(self.store, self.steamID)


    @router.subroute('levels')
    def levels(self, request, params):
        return LevelsRouter(self.store, self.steamID)
