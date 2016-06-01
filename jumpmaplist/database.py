from jumpmaplist.items import User



def addUser(store, steamID, superuser):
    user = store.findFirst(User, User.steamID == steamID)
    if user:
        raise ValueError('User already exists for {!r}'.format(steamID))
    User(store=store, steamID=steamID, superuser=superuser)
