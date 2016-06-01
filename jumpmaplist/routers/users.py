from axiom import attributes

from twisted.web import http
from twisted.web.resource import ForbiddenResource, ErrorPage
from twisted.web.static import Data

from txspinneret import query as q
from txspinneret.route import Router, Integer, Text, routedResource

from jumpmaplist.database import getUser, addUser, deleteUser
from jumpmaplist.items import User
from jumpmaplist.resource import EasyResource, APIError



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
                result.append(
                    { 'id': user.storeID
                    , 'steamid': str(user.steamID)
                    , 'superuser': user.superuser
                    })
            return result
        return EasyResource(GET)


    @router.subroute('add', Integer('steamID'))
    def add(self, request, params):
        def POST():
            ourUser = getUser(self.store, self.steamID)
            if not ourUser.superuser:
                return ForbiddenResource()
            steamID = params['steamID']

            response = self.steamAPI['ISteamUser'].GetPlayerSummaries(
                (steamID,))['response']
            if not len(response['players']):
                return APIError(http.BAD_REQUEST, 'Steam user does not exist.')

            try:
                user = addUser(self.store, steamID, superuser=False)
            except ValueError:
                return APIError(http.BAD_REQUEST, 'User already exists.')

            return (
                { 'id': user.storeID
                , 'steamid': str(user.steamID)
                , 'superuser': user.superuser
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
