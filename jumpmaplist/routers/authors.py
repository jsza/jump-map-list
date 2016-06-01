from axiom import attributes

from twisted.web import http
from twisted.web.static import Data

from txspinneret import query as q
from txspinneret.route import Router, Integer, Text, routedResource

from jumpmaplist.items import Author, Level, LevelAuthor, LevelClassTier
from jumpmaplist.resource import EasyResource, APIError



@routedResource
class AuthorsRouter(object):
    router = Router()

    def __init__(self, store, steamID):
        self.steamID = steamID
        self.store = store


    @router.subroute('list')
    def list(self, request, params):
        r = q.parse(
            { 'search': q.one(q.Text)
            }, request.args)
        search = r['search']
        def GET():
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
        return EasyResource(GET)


    @router.subroute('add', Text('name'))
    def add(self, request, params):
        def POST():
            r = q.parse(
                { 'steamID': q.one(q.Text)
                }, request.args)
            steamID = r['steamID']
            name = params['name']

            if steamID:
                steamID = int(steamID)
                exists = self.store.findFirst(Author,
                    attributes.OR(Author.steamID == steamID,
                                  Author.name == name))
                if exists:
                    return APIError(
                        http.BAD_REQUEST,
                        'Author with that name or steamID already exists.')

            Author(store=self.store, name=name, steamID=steamID)
        return EasyResource(handlePOST=POST)


    @router.subroute(Integer('id'), 'update')
    def update(self, request, params):
        authorID = params['id']


    @router.subroute('remove')
    def remove(self, request, params):
        pass
