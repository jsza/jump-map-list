from twisted.cred.credentials import ICredentials
from zope.interface import implementer



class IPreauthenticated(ICredentials):
    pass



@implementer(IPreauthenticated)
class Preauthenticated:
    def __init__(self, username):
        self.username = username

