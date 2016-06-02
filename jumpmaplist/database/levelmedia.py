from axiom import attributes


from jumpmaplist.items import LevelMedia
from jumpmaplist.database import BaseDatabase



class LevelMediaDatabase(BaseDatabase):
    def get(self, levelMediaID):
        levelMediaID = levelMediaID
        levelMedia = self.store.getItemByID(levelMediaID)
        if not isinstance(levelMedia, LevelMedia):
            raise ValueError('Item ID is not a LevelMedia.')
        return levelMedia


    def delete(self, levelMedia):
        def _t():
            for other in self.store.query(LevelMedia,
                attributes.AND(LevelMedia.level == levelMedia.level,
                               LevelMedia.index > levelMedia.index)):
                other.index -= 1
            levelMedia.deleteFromStore()
        self.store.transact(_t)


    def move(self, levelMedia, newIndex):
        ourItem = levelMedia
        level = ourItem.level
        oldIndex = ourItem.index
        count = self.db.levels.nextIndexForLevelMedia(level)
        if newIndex < 1:
            raise ValueError('New index cannot be less than 1.')
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
