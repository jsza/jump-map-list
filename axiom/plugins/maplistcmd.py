from axiom.scripts.axiomatic import AxiomaticCommand, AxiomaticSubCommand

from jumpmaplist.database import addUser



class AddSuperuser(AxiomaticSubCommand):
    longdesc = """
    Add a user by steamID who will be able to add or remove other users from
    the web interface.
    """

    optParameters = (
        [ ['steamid', 's', None, 'SteamID to add as a superuser.']
        ])

    def postOptions(self):
        store = self.parent.getStore()
        steamID = int(self.decodeCommandLine(self['steamid']))
        addUser(store, steamID, superuser=True)



class MapListCmd(AxiomaticCommand):
    name = 'maplist'
    description = 'Utilities for interacting with the jump map list database.'

    subCommands = (
        [ ('add-superuser', None, AddSuperuser, 'Add a superuser.')
        ])

    def getStore(self):
        return self.parent.getStore()
