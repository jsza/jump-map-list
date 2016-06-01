from jumpmaplist.items import User



def addUser(store, steamID, superuser):
    user = store.findFirst(User, User.steamID == steamID)
    if user:
        raise ValueError('User already exists for {!r}'.format(steamID))
    return User(store=store, steamID=steamID, superuser=superuser)



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
