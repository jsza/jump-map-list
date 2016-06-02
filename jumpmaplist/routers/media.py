from axiom import attributes

from twisted.web import http
from twisted.web.static import Data

from txspinneret import query as q
from txspinneret.route import Router, Integer, Text, routedResource

from jumpmaplist.items import (
    Author, Level, LevelAuthor, LevelClassTier, LevelMedia)
from jumpmaplist.resource import EasyResource, APIError
from jumpmaplist.route import JumpClass, MapTier, MediaType
from jumpmaplist.database import nextIndexForLevelMedia



@routedResource
class LevelMediaRouter(object):
    router = Router()

    def __init__(self, store, steamID):
        self.store = store
        self.steamID = steamID


    @router.subroute('id', Integer('id'))
    def byID(self, request, params):
        levelMediaID = params['id']
        levelMedia = self.store.getItemByID(levelMediaID)
        if not isinstance(levelMedia, LevelMedia):
            return APIError(http.BAD_REQUEST, 'Item ID is not a LevelMedia.')
        return SingleLevelMediaRouter(self.store, self.steamID, levelMedia)



@routedResource
class SingleLevelMediaRouter(object):
    router = Router()

    def __init__(self, store, steamID, levelMedia):
        self.store = store
        self.steamID = steamID
        self.levelMedia = levelMedia


    @router.subroute('delete')
    def delete(self, request, params):
        def POST():
            def _t():
                item = self.levelMedia
                for other in self.store.query(LevelMedia,
                    attributes.AND(LevelMedia.level == item.level,
                                   LevelMedia.index > item.index)):
                    other.index -= 1
                item.deleteFromStore()
            self.store.transact(_t)
        return EasyResource(handlePOST=POST)


    @router.subroute('move', Integer('index'))
    def move(self, request, params):
        def POST():
            ourItem = self.levelMedia
            level = ourItem.level
            oldIndex = ourItem.index
            newIndex = params['index']
            count = nextIndexForLevelMedia(self.store, level)
            if newIndex < 1:
                return APIError(http.BAD_REQUEST,
                                'New index cannot be less than 1.')
            if newIndex > count:
                newIndex = count
            if newIndex == oldIndex:
                return
            def _t():
                if newIndex > oldIndex:
                    query = self.store.query(LevelMedia,
                        attributes.AND(LevelMedia.level == level,
                                       LevelMedia.index <= newIndex,
                                       LevelMedia.index > oldIndex))
                    for item in query:
                        item.index -= 1
                elif newIndex < oldIndex:
                    query = self.store.query(LevelMedia,
                        attributes.AND(LevelMedia.level == level,
                                       LevelMedia.index >= newIndex,
                                       LevelMedia.index < oldIndex))
                    for item in query:
                        item.index += 1
                ourItem.index = newIndex
            self.store.transact(_t)
        return EasyResource(handlePOST=POST)
