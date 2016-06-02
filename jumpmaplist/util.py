from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.threads import deferToThread
from twisted.python.urlpath import URLPath
from twisted.web.resource import Resource
from twisted.web.server import quote, networkString, nativeString

from txspinneret.resource import _RenderableResource, NotAcceptable
from txspinneret.util import _parseAccept



class ContentTypeRouter(Resource):
    """
    Negotiate an appropriate representation based on the ``Accept`` header.

    Rendering this resource will negotiate a representation and render the
    matching handler.
    """
    def __init__(self, handlers, fallback=False):
        """
        :type  handlers: ``iterable`` of `bytes` and `Resource`
        :param handlers: Iterable of negotiable resources.

        :type  fallback: `bool`
        :param fallback: Fall back to the first handler in the case where
            negotiation fails?
        """
        Resource.__init__(self)
        self._handlers = list(handlers)
        self._fallback = fallback
        self._acceptHandlers = {}
        for acceptType, handler in self._handlers:
            if acceptType in self._acceptHandlers:
                raise ValueError(
                    'Duplicate handler for %r' % (acceptType,))
            self._acceptHandlers[acceptType] = handler


    def _negotiateHandler(self, request):
        """
        Negotiate a handler based on the content types acceptable to the
        client.

        :rtype: 2-`tuple` of `twisted.web.iweb.IResource` and `bytes`
        :return: Pair of a resource and the content type.
        """
        acceptHeader = request.requestHeaders.getRawHeaders('Accept')
        if acceptHeader is not None:
            accept = _parseAccept(acceptHeader)
            for contentType in accept.keys():
                handler = self._acceptHandlers.get(contentType.lower())
                if handler is not None:
                    return handler, contentType

        if self._fallback:
            contentType, handler = self._handlers[0]
            return handler, contentType
        return NotAcceptable(), None


    def getChildWithDefault(self, name, request):
        request.setHeader('vary', 'accept')
        resource, contentType = self._negotiateHandler(request)
        return resource.getChildWithDefault(name, request)



class LeafRenderableResource(_RenderableResource):
    def getChild(self, path, request):
        return self



def getRequestHostnamePort(request):
    host = request.getHeader(b'host')

    if host:
        parsed = host.split(b':', 1)
        hostname = parsed[0]
        try:
            port = int(parsed[1])
        except (ValueError, IndexError):
            if request.isSecure():
                port = 443
            else:
                port = 80
    else:
        h = request.getHost()
        hostname = networkString(h.host)
        port = h.port

    return hostname, port



def getUrlForRequest(request):
    prepath = request.prepath
    hostname, port = getRequestHostnamePort(request)
    if request.isSecure():
        default = 443
    else:
        default = 80
    if port == default:
        hostport = ''
    else:
        hostport = ':%d' % port
    prefix = networkString('http%s://%s%s/' % (
        request.isSecure() and 's' or '',
        nativeString(request.getRequestHostname()),
        hostport))
    path = b'/'.join([quote(segment, safe=b'') for segment in prepath])
    return prefix + path



@inlineCallbacks
def getSteamIDFromURL(url, steamAPI):
    path = URLPath.fromString(url)
    steamID = None
    if path.netloc.lower() == 'steamcommunity.com':
        if path.path.startswith('/id/'):
            vanityURL = path.path[4:].rstrip('/')
            response = yield deferToThread(
                steamAPI['ISteamUser'].ResolveVanityURL,
                vanityurl=vanityURL)
            try:
                steamID = int(response['response']['steamid'])
            except (KeyError, ValueError):
                pass
        elif path.path.startswith('/profiles/'):
            try:
                steamID = int(path.path[10:].rstrip('/'))
            except ValueError:
                pass
    returnValue(steamID)
