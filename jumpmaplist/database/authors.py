from axiom import attributes

from jumpmaplist.database import BaseDatabase
from jumpmaplist.items import Author



class AuthorDatabase(BaseDatabase):
    def list(self, search):
        result = []
        if search:
            query = self.store.query(Author,
                                     Author.name.like(
                                        u'%{}%'.format(search)))
        else:
            query = self.store.query(Author)
        for author in query:
            result.append(
                { 'id': author.storeID
                , 'name': author.name
                , 'steamid': author.steamID
                })
        return result


    def count(self):
        return self.query(Author).count


    def add(self, steamID, name):
        if self.find(steamID, name):
            raise ValueError('Author with that name or steamID already exists.')
        Author(store=self.store, name=name, steamID=steamID)


    def getAuthor(self, authorID):
        author = self.store.getItemByID(authorID)
        if not isinstance(author, Author):
            raise ValueError('Item ID is not a Author.')
        return author


    def find(self, steamID, name):
        return self.store.findFirst(Author,
            attributes.OR(Author.steamID == steamID,
                          Author.name == name))


    def logAddLevel(self, level, user):
        self.logEntry(u'ADD_LEVEL',
            {'name': level.name, 'level_type': level.levelType,
             'steamid': user.steamID},
             False)


    def logRemoveLevel(self, level, user):
        self.logEntry(u'DELETE_LEVEL',
            {'name': level.name, 'level_type': level.levelType,
             'steamid': user.steamID},
             False)
