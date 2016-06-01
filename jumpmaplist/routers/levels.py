from axiom import attributes

from twisted.web import http
from twisted.web.static import Data

from txspinneret import query as q
from txspinneret.route import Router, Integer, Text, routedResource

from jumpmaplist.items import Author, Level, LevelAuthor, LevelClassTier
from jumpmaplist.resource import EasyResource, APIError
from jumpmaplist.route import JumpClass, MapTier



@routedResource
class LevelsRouter(object):
    router = Router()

    def __init__(self, store, steamID):
        self.store = store
        self.steamID = steamID

    @router.subroute('list')
    def list(self, request, params):
        def GET():
            result = []
            for level in self.store.query(Level):
                authors = self.store.query(LevelAuthor,
                                           LevelAuthor.level == level)
                authorCount = authors.count()
                for a in authors:
                    authorName = a.author.name
                    break
                else:
                    authorName = None

                classTiers = self.store.query(LevelClassTier,
                                              LevelClassTier.level == level)
                classTiersResult = {}
                for ct in classTiers:
                    classTiersResult[ct.tfClass] = ct.toDict()

                result.append(
                    { 'id': level.storeID
                    , 'name': level.name
                    , 'class_tiers': classTiersResult
                    , 'author_count': authorCount
                    , 'author_name': authorName
                    })
            return result
        return EasyResource(GET)


    @router.subroute('add', Text('name'))
    def add(self, request, params):
        name = params['name'].strip()
        if len(name) == 0:
            return APIError(http.BAD_REQUEST, 'Map name cannot be blank.')

        def POST():
            query = self.store.query(Level, Level.name == name)
            if query.count() > 0:
                return APIError(http.BAD_REQUEST, 'Map already exists.')
            level = Level(store=self.store, name=name, levelType=1)
            return (
                { 'id': level.storeID
                , 'name': level.name
                , 'class_tiers': {}
                , 'author_count': 0
                , 'author_name': None
                })
        return EasyResource(handlePOST=POST)


    @router.subroute('id', Integer('id'))
    def byID(self, request, params):
        levelID = params['id']
        level = self.store.getItemByID(levelID)
        if not isinstance(level, Level):
            return APIError(http.BAD_REQUEST, 'Item ID is not a Level.')
        return SingleLevelRouter(self.store, self.steamID, level)



@routedResource
class SingleLevelRouter(object):
    router = Router()

    def __init__(self, store, steamID, level):
        self.store = store
        self.steamID = steamID
        self.level = level


    @router.subroute('tier', JumpClass('class'), MapTier('tier'))
    def setTier(self, request, params):
        tfClass = params['class']
        tier = params['tier']
        def POST():
            levelClassTier = self.store.findFirst(LevelClassTier,
                attributes.AND(LevelClassTier.level == self.level,
                               LevelClassTier.tfClass == tfClass))
            if not levelClassTier:
                levelClassTier = LevelClassTier(store=self.store,
                                                level=self.level,
                                                tfClass=tfClass,
                                                tier=tier)
            else:
                levelClassTier.tier = tier

        return EasyResource(handlePOST=POST)


    @router.subroute('delete')
    def delete(self, request, params):
        def POST():
            self.level.deleteFromStore()
        return EasyResource(handlePOST=POST)


    @router.subroute('authors')
    def authors(self, request, params):
        return SingleLevelAuthorsRouter(self.store, self.steamID, self.level)



@routedResource
class SingleLevelAuthorsRouter(object):
    router = Router()

    def __init__(self, store, steamID, level):
        self.store = store
        self.steamID = steamID
        self.level = level


    @router.subroute('list')
    def list(self, request, params):
        def GET():
            result = []
            query = self.store.query(LevelAuthor,
                                     LevelAuthor.level == self.level)
            for levelAuthor in query:
                author = levelAuthor.author
                result.append(
                    { 'id': levelAuthor.storeID
                    , 'author_id': author.storeID
                    , 'name': author.name
                    , 'steamid': author.steamID
                    })
            return result
        return EasyResource(GET)


    @router.subroute('add', Integer('id'))
    def add(self, request, params):
        authorID = params['id']
        def POST():
            author = self.store.getItemByID(authorID)
            if not isinstance(author, Author):
                return APIError(http.BAD_REQUEST,
                                'Item ID is not a Author.')

            levelAuthor = self.store.findFirst(LevelAuthor,
                    attributes.AND(
                    LevelAuthor.level == self.level,
                    LevelAuthor.author == author))

            if not levelAuthor:
                levelAuthor = LevelAuthor(store=self.store, level=self.level,
                                          author=author)
            return (
                { 'id': levelAuthor.storeID
                , 'author_id': author.storeID
                , 'name': author.name
                , 'steamid': author.steamID
                })
        return EasyResource(handlePOST=POST)


    @router.subroute('remove', Integer('id'))
    def remove(self, request, params):
        authorID = params['id']
        def POST():
            author = self.store.getItemByID(authorID)
            if not isinstance(author, Author):
                return APIError(http.BAD_REQUEST,
                                'Item ID is not a Author.')

            query = self.store.query(LevelAuthor,
                attributes.AND(
                    LevelAuthor.author == author,
                    LevelAuthor.level  == self.level))

            for item in query:
                item.deleteFromStore()
        return EasyResource(handlePOST=POST)



@routedResource
class SingleLevelMediaRouter(object):
    router = Router()

    def __init__(self, store, steamID, level):
        self.store = store
        self.steamID = steamID
        self.level = level


    @router.subroute('list')
    def list(self, request, params):
        pass


    @router.subroute('add')
    def add(self, request, params):
        pass


    @router.subroute('remove')
    def remove(self, request, params):
        pass
