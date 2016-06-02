from jumpmaplist.items import User, LevelMedia



def addUser(store, steamID, superuser, adderSteamID):
    user = store.findFirst(User, User.steamID == steamID)
    if user:
        raise ValueError('User already exists for {!r}'.format(steamID))
    return User(store=store, steamID=steamID, superuser=superuser,
                adderSteamID=adderSteamID)



def getUser(store, steamID):
    user = store.findUnique(User, User.steamID == steamID, default=None)
    return user



def deleteUser(store, userID):
    try:
        item = store.getItemByID(userID)
    except KeyError:
        pass

    if isinstance(item, User):
        item.deleteFromStore()
    else:
        pass



def nextIndexForLevelMedia(store, level):
    item = store.findFirst(LevelMedia, LevelMedia.level == level,
                           sort=LevelMedia.index.desc)
    return (item.index if item else 0) + 1
