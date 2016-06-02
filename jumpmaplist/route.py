from txspinneret import query as q

from jumpmaplist.constants.tf2 import JUMP_CLASSES
from jumpmaplist.constants.tiers import VALID_TIERS
from jumpmaplist.constants.mediatype import MEDIA_TYPES



def JumpClass(name, base=10, encoding=None):
    """
    Match a jump class index route parameter.

    See `txpinneret.query.Integer`.
    """
    def _match(request, value):
        value = q.Integer(value, base, encoding)
        if value in JUMP_CLASSES:
            return name, value
        return name, None
    return _match



def MapTier(name, base=10, encoding=None):
    """
    Match a map tier route parameter.

    See `txpinneret.query.Integer`.
    """
    def _match(request, value):
        value = q.Integer(value, base, encoding)
        if value in VALID_TIERS:
            return name, value
        return name, None
    return _match



def MediaType(name, base=10, encoding=None):
    """
    Match a media type route parameter.

    See `txpinneret.query.Integer`.
    """
    def _match(request, value):
        value = q.Integer(value, base, encoding)
        if value in MEDIA_TYPES:
            return name, value
        return name, None
    return _match
