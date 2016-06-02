from axiom import attributes

from twisted.internet.threads import deferToThread
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python.urlpath import URLPath
from twisted.web import http
from twisted.web.resource import ForbiddenResource, ErrorPage
from twisted.web.static import Data

from txspinneret import query as q
from txspinneret.route import Router, Integer, Text, routedResource

from jumpmaplist.database import getUser, addUser, deleteUser
from jumpmaplist.items import User
from jumpmaplist.resource import EasyResource, APIError
from jumpmaplist.util import getSteamIDFromURL



class InvalidCommunityURL(APIError):
    def __init__(self):
        APIError.__init__(self, http.BAD_REQUEST, 'Community URL is invalid.')



@routedResource
class UsersRouter(object):
    router = Router()

    def __init__(self, store, steamID, steamAPI):
        self.steamID = steamID
        self.store = store
        self.steamAPI = steamAPI


    @router.subroute('list')
    def list(self, request, params):
        def GET():
            result = []
            query = self.store.query(User)
            for user in query:
                asi = user.adderSteamID
                result.append(
                    { 'id': user.storeID
                    , 'steamid': str(user.steamID)
                    , 'superuser': user.superuser
                    , 'adder_steamid': str(asi) if asi else None
                    , 'timestamp': user.timestamp.asPOSIXTimestamp()
                    })
            return result
        return EasyResource(GET)


    @router.subroute('add')
    def add(self, request, params):
        @inlineCallbacks
        def POST():
            ourUser = getUser(self.store, self.steamID)
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
                user = addUser(self.store, steamID, superuser=superuser,
                               adderSteamID=self.steamID)
            except ValueError:
                returnValue(APIError(http.BAD_REQUEST, 'User already exists.'))

            asi = user.adderSteamID
            returnValue (
                { 'id': user.storeID
                , 'steamid': str(user.steamID)
                , 'superuser': user.superuser
                , 'adder_steamid': str(asi) if asi else None
                , 'timestamp': user.timestamp.asPOSIXTimestamp()
                })
        return EasyResource(handlePOST=POST)


    @router.subroute(Integer('userID'), 'delete')
    def delete(self, request, params):
        def POST():
            userID = params['userID']
            ourUser = getUser(self.store, self.steamID)
            if not ourUser.superuser:
                return ForbiddenResource()
            item = self.store.getItemByID(userID)
            if item == ourUser:
                return APIError(http.BAD_REQUEST,
                                'You cannot delete your own user.')
            deleteUser(self.store, userID)
        return EasyResource(handlePOST=POST)
