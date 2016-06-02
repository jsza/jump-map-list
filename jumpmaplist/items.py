from epsilon.extime import Time

from axiom import attributes as A
from axiom.item import Item



def nowAttribute(allowNone=False, defaultFactory=Time):
    return A.timestamp(doc='Date the item was added.',
                       allowNone=allowNone,
                       defaultFactory=defaultFactory)



class Author(Item):
    name      = A.text(allowNone=False)
    steamID   = A.integer(doc='64-bit community steam ID.')
    timestamp = nowAttribute()

    def toDict(self):
        return (
            { 'id': str(self.storeID)
            , 'name': self.name
            , 'steamid': str(self.steamID)
            , 'timestamp': self.timestamp.asPOSIXTimestamp()
            })



# Call them levels here to avoid clashing with `map`.
class Level(Item):
    name      = A.text(allowNone=False)
    levelType = A.integer(allowNone=False)
    timestamp = nowAttribute(allowNone=False)

    def toDict(self):
        return (
            { 'id': str(self.storeID)
            , 'name': self.name
            , 'level_type': self.levelType
            })



class LevelAuthor(Item):
    level  = A.reference(reftype=Level, allowNone=False,
                         whenDeleted=A.reference.CASCADE)
    author = A.reference(reftype=Author, allowNone=False,
                         whenDeleted=A.reference.CASCADE)

    def toDict(self):
        print self.author
        return (
            { 'id': str(self.storeID)
            , 'author_id': str(self.author.storeID)
            , 'name': self.author.name
            , 'steamid': str(self.author.steamID)
            })



class LevelClassTier(Item):
    level     = A.reference(reftype=Level, allowNone=False,
                            whenDeleted=A.reference.CASCADE)
    tfClass   = A.integer(doc='TF2 class index.', allowNone=False)
    tier      = A.integer(allowNone=False)

    def toDict(self):
        return (
            { 'id': str(self.storeID)
            , 'level_id': str(self.level.storeID)
            , 'tf_class': self.tfClass
            , 'tier': self.tier
            })



class LevelDownload(Item):
    level = A.reference(reftype=Level, allowNone=False,
                        whenDeleted=A.reference.CASCADE)
    url   = A.text(doc='Download URL.', allowNone=False)

    def toDict(self):
        return (
            { 'id': str(self.storeID)
            , 'level_id': str(self.level.storeID)
            , 'url': self.url
            })



class LevelMedia(Item):
    level        = A.reference(reftype=Level, allowNone=False,
                               whenDeleted=A.reference.CASCADE)
    mediaType    = A.integer(doc='See `jumpmaplist.constants.mediatype`.',
                             allowNone=False)
    url          = A.text(doc='Remote URL for the media.', allowNone=False)
    index        = A.integer(doc='Order at which to display the media.',
                          allowNone=False)
    adderSteamID = A.integer(doc='SteamID of the user who added this media.',
                             allowNone=False)
    timestamp    = nowAttribute()

    def toDict(self):
        return (
            { 'id': str(self.storeID)
            , 'media_type': self.mediaType
            , 'url': self.url
            , 'index': self.index
            , 'adder_steamid': str(self.adderSteamID)
            , 'timestamp': self.timestamp.asPOSIXTimestamp()
            })



class User(Item):
    steamID      = A.integer(doc='64-bit community steam ID.', allowNone=False)
    superuser    = A.boolean(doc='User can add or delete other users.',
                             allowNone=False)
    adderSteamID = A.integer(doc='SteamID of the user who added this user.')
    timestamp    = nowAttribute()

    def toDict(self):
        asi = self.adderSteamID
        return (
            { 'id': str(self.storeID)
            , 'steamid': str(self.steamID)
            , 'superuser': self.superuser
            , 'adder_steamid': str(asi) if asi else None
            , 'timestamp': self.timestamp.asPOSIXTimestamp()
            })



class LogEntry(Item):
    superuser = A.integer(doc='Whether this should be visible only to superusers.',
                          allowNone=False)
    logType   = A.text(doc='Log message type. See `jumpmaplist.constants.logtypes`.',
                       allowNone=False)
    data      = A.text(doc='JSON-encoded log data.', allowNone=False)
    timestamp = nowAttribute()
