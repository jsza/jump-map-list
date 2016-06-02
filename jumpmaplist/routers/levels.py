from axiom import attributes

from twisted.web import http
from twisted.web.static import Data

from txspinneret import query as q
from txspinneret.route import Router, Integer, Text, routedResource

from jumpmaplist.items import (
    Author, Level, LevelAuthor, LevelClassTier, LevelMedia)
from jumpmaplist.resource import EasyResource, APIError
from jumpmaplist.route import JumpClass, MapTier, MediaType



@routedResource
class LevelsRouter(object):
    router = Router()

    def __init__(self, db, steamID):
        self.db = db
        self.steamID = steamID


    @router.subroute('list')
    def list(self, request, params):
        def GET():
            return self.db.levels.list()
        return EasyResource(GET)


    @router.subroute('add', Text('name'))
    def add(self, request, params):
        name = params['name'].strip()
        if len(name) == 0:
            return APIError(http.BAD_REQUEST, 'Map name cannot be blank.')

        def POST():
            try:
                return self.db.levels.add(name=name, levelType=0,
                                          adderSteamID=self.steamID)
            except ValueError as e:
                return APIError(http.BAD_REQUEST, e.message)
        return EasyResource(handlePOST=POST)


    @router.subroute('id', Integer('id'))
    def byID(self, request, params):
        try:
            level = self.db.levels.get(params['id'])
        except ValueError as e:
            return APIError(http.BAD_REQUEST, e.message)
        return SingleLevelRouter(self.db, self.steamID, level)



@routedResource
class SingleLevelRouter(object):
    router = Router()

    def __init__(self, db, steamID, level):
        self.db = db
        self.steamID = steamID
        self.level = level


    @router.subroute('tier', JumpClass('class'), MapTier('tier'))
    def setTier(self, request, params):
        tfClass = params['class']
        tier = params['tier']
        def POST():
            self.db.levels.setTier(self.level, tfClass, tier)
        return EasyResource(handlePOST=POST)


    @router.subroute('delete')
    def delete(self, request, params):
        def POST():
            self.level.deleteFromStore()
        return EasyResource(handlePOST=POST)


    @router.subroute('authors')
    def authors(self, request, params):
        return SingleLevelAuthorsRouter(self.db, self.steamID, self.level)


    @router.subroute('media')
    def media(self, request, params):
        return SingleLevelMediaRouter(self.db, self.steamID, self.level)



@routedResource
class SingleLevelAuthorsRouter(object):
    router = Router()

    def __init__(self, db, steamID, level):
        self.db = db
        self.steamID = steamID
        self.level = level


    @router.subroute('list')
    def list(self, request, params):
        def GET():
            return self.db.levels.listAuthors(self.level)
        return EasyResource(GET)


    @router.subroute('add', Integer('id'))
    def add(self, request, params):
        authorID = params['id']
        def POST():
            try:
                return self.db.levels.addAuthor(self.level, authorID)
            except ValueError as e:
                return APIError(http.BAD_REQUEST, e.message)
        return EasyResource(handlePOST=POST)


    @router.subroute('remove', Integer('id'))
    def remove(self, request, params):
        authorID = params['id']
        def POST():
            try:
                self.db.levels.removeAuthor(self.level, authorID)
            except ValueError as e:
                return APIError(http.BAD_REQUEST, e.message)
        return EasyResource(handlePOST=POST)



@routedResource
class SingleLevelMediaRouter(object):
    router = Router()

    def __init__(self, db, steamID, level):
        self.db = db
        self.steamID = steamID
        self.level = level


    @router.subroute('list')
    def list(self, request, params):
        def GET():
            return self.db.levels.listMedia(self.level)
        return EasyResource(GET)


    @router.subroute('add', MediaType('type'))
    def add(self, request, params):
        def POST():
            url = request.content.read().decode('utf8').strip()
            mediaType = params['type']
            return self.db.levels.addMedia(self.level, mediaType, url,
                                           self.steamID)
        return EasyResource(handlePOST=POST)
