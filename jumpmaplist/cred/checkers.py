from twisted.cred.checkers import ICredentialsChecker
from zope.interface import implements

from jumpmaplist.cred.credentials import IPreauthenticated



class PreauthenticatedChecker(object):
    implements(ICredentialsChecker)
    credentialInterfaces = [IPreauthenticated]

    def requestAvatarId(self, credentials):
        return credentials.username
