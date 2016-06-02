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

    def __init__(self, db, steamID):
        self.db = db
        self.steamID = steamID


    @router.subroute('list')
    def list(self, request, params):
        r = q.parse(
            { 'search': q.one(q.Text)
            }, request.args)
        search = r['search']
        def GET():
            return self.db.authors.list(search=search)
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
                try:
                    self.db.authors.addAuthor(steamID, name)
                except ValueError as e:
                    return APIError(http.BAD_REQUEST, e.message)
        return EasyResource(handlePOST=POST)


    @router.subroute(Integer('id'), 'update')
    def update(self, request, params):
        authorID = params['id']


    @router.subroute('remove')
    def remove(self, request, params):
        pass
