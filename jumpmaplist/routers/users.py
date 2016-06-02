from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.web import http
from twisted.web.resource import ForbiddenResource

from txspinneret import query as q
from txspinneret.route import Router, Integer, routedResource

from jumpmaplist.resource import EasyResource, APIError
from jumpmaplist.util import getSteamIDFromURL



class InvalidCommunityURL(APIError):
    def __init__(self):
        APIError.__init__(self, http.BAD_REQUEST, 'Community URL is invalid.')



@routedResource
class UsersRouter(object):
    router = Router()

    def __init__(self, db, steamID, steamAPI):
        self.db = db
        self.steamID = steamID
        self.steamAPI = steamAPI


    @router.subroute('list')
    def list(self, request, params):
        def GET():
            return self.db.users.list()
        return EasyResource(GET)


    @router.subroute('add')
    def add(self, request, params):
        @inlineCallbacks
        def POST():
            ourUser = self.db.users.get(self.steamID)
            if not ourUser.superuser:
                returnValue(ForbiddenResource())

            r = q.parse(
                { 'superuser': q.one(q.Boolean)
                }, request.args)
            superuser = r['superuser']

            url = request.content.read().strip()
            steamID = yield getSteamIDFromURL(url, self.steamAPI)
            if not steamID: returnValue(InvalidCommunityURL())

            response = yield self.steamAPI['ISteamUser'].GetPlayerSummaries(
                (steamID,))['response']
            if not len(response['players']):
                returnValue(
                    APIError(http.BAD_REQUEST, 'Steam user does not exist.'))

            try:
                user = self.db.users.add(steamID=steamID, superuser=superuser,
                                         adderSteamID=self.steamID)
            except ValueError:
                returnValue(APIError(http.BAD_REQUEST, 'User already exists.'))

            returnValue(user.toDict())
        return EasyResource(handlePOST=POST)


    @router.subroute(Integer('userID'), 'delete')
    def delete(self, request, params):
        def POST():
            userID = params['userID']
            ourUser = self.db.users.get(self.steamID)
            if not ourUser.superuser:
                return ForbiddenResource()
            item = self.db.store.getItemByID(userID)
            if item == ourUser:
                return APIError(http.BAD_REQUEST,
                                'You cannot delete your own user.')
            try:
                self.db.users.delete(userID, self.steamID)
            except ValueError as e:
                return APIError(http.BAD_REQUEST, e.message)
        return EasyResource(handlePOST=POST)
