from jumpmaplist.database import BaseDatabase
from jumpmaplist.items import User



class UserDatabase(BaseDatabase):
    def list(self):
        result = []
        query = self.store.query(User)
        for user in query:
            result.append(user.asDict())
        return result


    def add(self, steamID, superuser, adderSteamID):
        user = self.store.findFirst(User, User.steamID == steamID)
        if user:
            raise ValueError('User already exists for {!r}'.format(steamID))
        def _t():
            user = User(store=self.store, steamID=steamID, superuser=superuser,
                        adderSteamID=adderSteamID)
            self.logAdd(user, adderSteamID)
            return user
        return self.store.transact(_t)


    def get(self, steamID):
        user = self.store.findUnique(User, User.steamID == steamID,
                                     default=None)
        return user


    def delete(self, userID, deleterSteamID):
        try:
            item = self.store.getItemByID(userID)
        except KeyError:
            return

        if isinstance(item, User):
            def _t():
                item.deleteFromStore()
                self.logDelete(item, deleterSteamID)
            self.store.transact(_t)


    def logAdd(self, user, adderSteamID):
        self.logEntry(u'ADD_USER',
            {'steamid': user.steamID, 'adder_steamid': adderSteamID},
            True)


    def logDelete(self, user, deleterSteamID):
        self.logEntry(u'DELETE_USER',
            {'steamid': user.steamID, 'deleter_steamid': deleterSteamID},
            True)
