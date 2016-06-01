import jumpmaplist

from twisted.web.template import Element, renderer, XMLFile
from twisted.python.filepath import FilePath

import json
from twisted.internet.defer import maybeDeferred
from twisted.python.compat import nativeString
from twisted.web.error import UnsupportedMethod
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.static import Data



class ApplicationElement(Element):
    loader = XMLFile(FilePath(jumpmaplist.__file__).sibling('templates').child(
        'index.html'))

    def __init__(self, steamid, jsPath):
        self.steamid = steamid
        self.jsPath = jsPath


    @renderer
    def bundlepath(self, request, tag):
        return tag(src=self.jsPath)



class LoginElement(Element):
    loader = XMLFile(FilePath(jumpmaplist.__file__).sibling('templates').child(
        'login.html'))



class EasyResource(Resource):
    def __init__(self, handleGET=None, handlePOST=None, handleDELETE=None,
                 handlePUT=None):
        Resource.__init__(self)
        self.handleGET = handleGET
        self.handlePOST = handlePOST
        self.handleDELETE = handleDELETE
        self.handlePUT = handlePUT


    def render(self, request):
        method = nativeString(request.method)
        handler = getattr(self, 'handle' + method, None)

        if handler is None:
            allowedMethods = [x
                              for x
                              in ['GET', 'POST', 'DELETE', 'PUT']
                              if getattr(self, 'handle' + x, None)]
            raise UnsupportedMethod(allowedMethods)

        def _cb(result):
            if isinstance(result, Resource):
                request.write(result.render(request))
                request.finish()
            else:
                request.setHeader('Content-Type', 'application/json')
                request.write(json.dumps(result))
                request.finish()

        def _eb(failure):
            failure.printTraceback()
            request.setResponseCode(500)
            request.finish()

        maybeDeferred(handler).addCallback(_cb).addErrback(_eb)
        return NOT_DONE_YET


    def handleOPTIONS(self):
        return None



class JSONData(Data):
    def __init__(self, obj):
        Data.__init__(self, json.dumps(obj), 'application/json')


    def render_POST(self, request):
        return self.render_GET(request)


    def render_DELETE(self, request):
        return self.render_GET(request)


    def render_PUT(self, request):
        return self.render_GET(request)



class JSONError(JSONData):
    def __init__(self, code, obj):
        JSONData.__init__(self, obj)
        self.code = code


    def render(self, request):
        request.setResponseCode(self.code)
        return JSONData.render(self, request)



class APIError(JSONError):
    def __init__(self, code, text):
        JSONError.__init__(self, code, {'error': text})
