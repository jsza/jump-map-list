from axiom import attributes

from jumpmaplist.database import BaseDatabase
from jumpmaplist.items import Author



class AuthorDatabase(BaseDatabase):
    def list(self, search):
        if search:
            query = self.store.query(Author,
                                     Author.name.like(u'%{}%'.format(search)),
                                     sort=Author.name.asc)
        else:
            query = self.store.query(Author, sort=Author.name.asc)
        return [a.toDict() for a in query]


    def count(self):
        return self.query(Author).count


    def add(self, steamID, name):
        item = self.find(steamID, name)
        if item:
            if item.steamID == steamID:
                raise ValueError('Author with that steamID already exists.')
            elif item.name.lower() == name.lower():
                raise ValueError('Author with that name already exists.')
        author = Author(store=self.store, name=name, steamID=steamID)
        return author.toDict()


    def remove(self, authorID):
        author = self.get(authorID)
        author.deleteFromStore()


    def get(self, authorID):
        author = self.store.getItemByID(authorID)
        if not isinstance(author, Author):
            raise ValueError('Item ID is not a Author.')
        return author


    def find(self, steamID, name):
        return self.store.findFirst(Author,
            attributes.OR(Author.steamID == steamID,
                          Author.name == name))
