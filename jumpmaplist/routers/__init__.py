from twisted.internet.threads import deferToThread
from twisted.web.static import Data

from txspinneret import query as q
from txspinneret.route import Router, routedResource

from jumpmaplist.resource import EasyResource
from jumpmaplist.routers.authors import AuthorsRouter
from jumpmaplist.routers.levels import LevelsRouter
from jumpmaplist.routers.media import LevelMediaRouter
from jumpmaplist.routers.users import UsersRouter



@routedResource
class PublicRouter(object):
    router = Router()

    def __init__(self, db):
        self.db = db


    @router.subroute('list')
    def list(self, request, params):
        result = self.db.authors.count()
        return Data(str(result), 'text/plain')



@routedResource
class PrivateRouter(object):
    router = Router()

    def __init__(self, db, steamID, steamAPI):
        self.db = db
        self.steamID = steamID
        self.steamAPI = steamAPI


    @router.subroute('authors')
    def authors(self, request, params):
        return AuthorsRouter(self.db, self.steamID, self.steamAPI)


    @router.subroute('levels')
    def levels(self, request, params):
        return LevelsRouter(self.db, self.steamID)


    @router.subroute('users')
    def users(self, request, params):
        return UsersRouter(self.db, self.steamID, self.steamAPI)


    @router.subroute('levelmedia')
    def media(self, request, params):
        return LevelMediaRouter(self.db, self.steamID)


    @router.subroute('steamavatars')
    def steamavatars(self, request, params):
        def GET():
            args = q.parse({'steamids': q.one(q.Text)}, request.args)
            steamids = args['steamids'].split(',')
            def _tx():
                raw = self.steamAPI['ISteamUser'].GetPlayerSummaries(steamids)
                result = {}
                for player in raw['response']['players']:
                    if player.get('gameid'):
                        status = 'in-game'
                    else:
                        if player['personastate'] > 0:
                            status = 'online'
                        else:
                            status = 'offline'
                    result[player['steamid']] = {
                        'status': status,
                        'personaname': player['personaname'],
                        'avatar': {
                            'small': player['avatar'],
                            'medium': player['avatarmedium'],
                            'large': player['avatarfull']
                        }
                    }
                return result
            return deferToThread(_tx)
        return EasyResource(GET)
