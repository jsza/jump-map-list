from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web import http

from txspinneret import query as q
from txspinneret.route import Router, Integer, Text, routedResource

from jumpmaplist.resource import EasyResource, APIError
from jumpmaplist.routers.users import InvalidCommunityURL
from jumpmaplist.util import getSteamIDFromURL



@routedResource
class AuthorsRouter(object):
    router = Router()

    def __init__(self, db, steamID, steamAPI):
        self.db = db
        self.steamID = steamID
        self.steamAPI = steamAPI


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
        @inlineCallbacks
        def POST():
            r = q.parse(
                { 'steamID': q.one(q.Text)
                }, request.args)
            steamID = r['steamID']
            name = params['name']

            url = request.content.read().strip()
            steamID = yield getSteamIDFromURL(url, self.steamAPI)
            if not steamID: returnValue(InvalidCommunityURL())

            response = yield self.steamAPI['ISteamUser'].GetPlayerSummaries(
                (steamID,))['response']
            if not len(response['players']):
                returnValue(
                    APIError(http.BAD_REQUEST, 'Steam user does not exist.'))

            if steamID:
                steamID = int(steamID)
                try:
                    returnValue(self.db.authors.add(steamID, name))
                except ValueError as e:
                    returnValue(APIError(http.BAD_REQUEST, e.message))
        return EasyResource(handlePOST=POST)


    @router.subroute(Integer('id'), 'update')
    def update(self, request, params):
        authorID = params['id']


    @router.subroute(Integer('id'), 'remove')
    def remove(self, request, params):
        def POST():
            try:
                self.db.authors.remove(params['id'])
            except ValueError as e:
                returnValue(APIError(http.BAD_REQUEST, e.message))
        return EasyResource(handlePOST=POST)
