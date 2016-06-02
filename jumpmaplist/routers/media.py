from twisted.web import http
from txspinneret.route import Router, Integer, routedResource

from jumpmaplist.resource import EasyResource, APIError



@routedResource
class LevelMediaRouter(object):
    router = Router()

    def __init__(self, db, steamID):
        self.db = db
        self.steamID = steamID


    @router.subroute('id', Integer('id'))
    def byID(self, request, params):
        try:
            levelMedia = self.db.levelmedia.get(params['id'])
        except ValueError as e:
            return APIError(http.BAD_REQUEST, e.message)
        return SingleLevelMediaRouter(self.db, self.steamID, levelMedia)



@routedResource
class SingleLevelMediaRouter(object):
    router = Router()

    def __init__(self, db, steamID, levelMedia):
        self.db = db
        self.steamID = steamID
        self.levelMedia = levelMedia


    @router.subroute('delete')
    def delete(self, request, params):
        def POST():
            self.db.levelmedia.delete(self.levelMedia)
        return EasyResource(handlePOST=POST)


    @router.subroute('move', Integer('index'))
    def move(self, request, params):
        def POST():
            try:
                self.db.levelmedia.move(self.levelMedia, params['index'])
            except ValueError as e:
                return APIError(http.BAD_REQUEST, e.message)
        return EasyResource(handlePOST=POST)
