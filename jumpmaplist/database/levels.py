from axiom import attributes

from jumpmaplist.constants.mediatype import MEDIA_TYPES
from jumpmaplist.database import BaseDatabase
from jumpmaplist.items import Level, LevelAuthor, LevelClassTier, LevelMedia



class LevelDatabase(BaseDatabase):
    def list(self):
        result = []
        for level in self.store.query(Level):
            result.append(self.detailedInfo(level))
        return result


    def add(self, name, levelType, adderSteamID):
        query = self.store.query(Level, Level.name == name)
        if query.count() > 0:
            raise ValueError('Map already exists.')
        level = Level(store=self.store, name=name, levelType=levelType)
        self.logAddLevel(level, adderSteamID)
        return self.detailedInfo(level)


    def detailedInfo(self, level):
        result = level.toDict()
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

        mediaCountResult = {}
        for mediaType in MEDIA_TYPES:
            mediaCountResult[mediaType] = self.store.query(LevelMedia,
                attributes.AND(LevelMedia.level == level,
                               LevelMedia.mediaType == mediaType)).count()

        result.update(
            { 'class_tiers': classTiersResult
            , 'author_count': authorCount
            , 'author_name': authorName
            , 'media_counts': mediaCountResult
            })
        return result


    def get(self, levelID):
        level = self.store.getItemByID(levelID)
        if not isinstance(level, Level):
            raise ValueError('Item ID is not a Level.')
        return level


    def setTier(self, level, tfClass, tier):
        levelClassTier = self.store.findFirst(LevelClassTier,
            attributes.AND(LevelClassTier.level == level,
                           LevelClassTier.tfClass == tfClass))
        if not levelClassTier:
            levelClassTier = LevelClassTier(store=self.store,
                                            level=level,
                                            tfClass=tfClass,
                                            tier=tier)
        else:
            levelClassTier.tier = tier


    def listAuthors(self, level):
        result = []
        query = self.store.query(LevelAuthor,
                                 LevelAuthor.level == level)
        for levelAuthor in query:
            author = levelAuthor.author
            result.append(
                { 'id': levelAuthor.storeID
                , 'author_id': author.storeID
                , 'name': author.name
                , 'steamid': author.steamID
                })
        return result


    def addAuthor(self, level, authorID):
        author = self.db.authors.get(authorID)

        levelAuthor = self.store.findFirst(LevelAuthor,
                attributes.AND(
                LevelAuthor.level == level,
                LevelAuthor.author == author))

        if not levelAuthor:
            levelAuthor = LevelAuthor(store=self.store, level=level,
                                      author=author)
        return (
            { 'id': levelAuthor.storeID
            , 'author_id': author.storeID
            , 'name': author.name
            , 'steamid': author.steamID
            })


    def removeAuthor(self, level, authorID):
        author = self.db.authors.get(authorID)

        query = self.store.query(LevelAuthor,
            attributes.AND(
                LevelAuthor.author == author,
                LevelAuthor.level  == level))

        for item in query:
            item.deleteFromStore()


    def listMedia(self, level):
        query = self.store.query(LevelMedia,
                                 LevelMedia.level == level,
                                 sort=LevelMedia.index.asc)
        result = []
        for lm in query:
            result.append(
                { 'id': lm.storeID
                , 'media_type': lm.mediaType
                , 'url': lm.url
                , 'index': lm.index
                , 'adder_steamid': str(lm.adderSteamID)
                , 'timestamp': lm.timestamp.asPOSIXTimestamp()
                })
        return result


    def addMedia(self, level, mediaType, url, adderSteamID):
        index = self.nextIndexForLevelMedia(level)
        levelMedia = LevelMedia(store=self.store, level=level,
                                index=index, mediaType=mediaType, url=url,
                                adderSteamID=adderSteamID)
        return (
            { 'id': levelMedia.storeID
            , 'media_type': levelMedia.mediaType
            , 'url': levelMedia.url
            , 'index': levelMedia.index
            , 'adder_steamid': str(levelMedia.adderSteamID)
            , 'timestamp': levelMedia.timestamp.asPOSIXTimestamp()
            })


    def nextIndexForLevelMedia(self, level):
        item = self.store.findFirst(LevelMedia, LevelMedia.level == level,
                                    sort=LevelMedia.index.desc)
        return (item.index if item else 0) + 1


    def logAddLevel(self, level, adderSteamID):
        self.logEntry('ADD_LEVEL',
            {'name': level.name, 'level_type': level.levelType,
             'steamid': adderSteamID},
             False)


    def logRemoveLevel(self, level, adderSteamID):
        self.logEntry('DELETE_LEVEL',
            {'name': level.name, 'level_type': level.levelType,
             'steamid': adderSteamID},
             False)
