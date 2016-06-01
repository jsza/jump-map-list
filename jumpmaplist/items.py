from axiom import attributes as A
from axiom.item import Item



class Author(Item):
    name    = A.text(allowNone=False)
    steamID = A.integer(doc='64-bit community steam ID.')

    def toDict(self):
        return (
            { 'id': self.storeID
            , 'name': self.name
            , 'steamid': self.steamID
            })



# Call them levels here to avoid clashing with `map`.
class Level(Item):
    name      = A.text(allowNone=False)
    levelType = A.integer(allowNone=False)

    def toDict(self):
        return (
            { 'id': self.storeID
            , 'name': self.name
            , 'level_type': self.levelType
            })



class LevelAuthor(Item):
    level  = A.reference(reftype=Level, allowNone=False)
    author = A.reference(reftype=Author, allowNone=False)

    def toDict(self):
        return (
            { 'id': self.storeID
            , 'author_id': self.author.storeID
            , 'name': self.author.name
            , 'steamid': self.author.steamID
            })



class LevelClassTier(Item):
    level   = A.reference(reftype=Level, allowNone=False)
    tfClass = A.integer(doc='TF2 class index.', allowNone=False)
    tier    = A.integer(allowNone=False)

    def toDict(self):
        return (
            { 'id': self.storeID
            , 'level_id': self.level.storeID
            , 'tf_class': self.tfClass
            , 'tier': self.tier
            })



class LevelDownload(Item):
    level = A.reference(reftype=Level, allowNone=False)
    url   = A.text(doc='Download URL.', allowNone=False)

    def toDict(self):
        return (
            { 'id': self.storeID
            , 'level_id': self.level.storeID
            , 'url': self.url
            })



class LevelMedia(Item):
    level     = A.reference(reftype=Level, allowNone=False)
    mediaType = A.integer(doc='See `jumpmaplist.constants.mediatype`.',
                          allowNone=False)
    url       = A.text(doc='URL for the media', allowNone=False)



class User(Item):
    steamID   = A.integer(doc='64-bit community steam ID.', allowNone=False)
    superuser = A.boolean(doc='User can add or delete other users.', allowNone=False)
