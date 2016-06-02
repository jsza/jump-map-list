from jumpmaplist.database.base import BaseDatabase
from jumpmaplist.database.authors import AuthorDatabase
from jumpmaplist.database.levelmedia import LevelMediaDatabase
from jumpmaplist.database.levels import LevelDatabase
from jumpmaplist.database.users import UserDatabase



class Database(BaseDatabase):
    def __init__(self, store):
        BaseDatabase.__init__(self, store, self)

        self.authors = AuthorDatabase(self.store, self)
        self.levelmedia = LevelMediaDatabase(self.store, self)
        self.levels = LevelDatabase(self.store, self)
        self.users = UserDatabase(self.store, self)
