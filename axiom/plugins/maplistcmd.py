from axiom.scripts.axiomatic import AxiomaticCommand, AxiomaticSubCommand

from twisted.python.filepath import FilePath

from jumpmaplist.items import Author



def steamidTo64(steamid):
    steamid = steamid[8:]
    y, z = map(int, steamid.split(':'))
    return str(z * 2 + y + 76561197960265728)



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



class ImportAuthors(AxiomaticSubCommand):
    longdesc = """
    Import authors from CSV format.
    """

    optParameters = (
        [ ['file', 'f', None, 'Path to file.']
        ])

    def postOptions(self):
        store = self.parent.getStore()
        path = self.decodeCommandLine(self['file'])
        content = FilePath(path).getContent()
        for line in content.strip().split('\n'):
            steamID, name = line.split(',', 1)
            Author(store=store, name=name, steamID=int(steamidTo64(steamID)))
        steamID = int(self.decodeCommandLine(self['steamid']))



class MapListCmd(AxiomaticCommand):
    name = 'maplist'
    description = 'Utilities for interacting with the jump map list database.'

    subCommands = (
        [ ('add-superuser', None, AddSuperuser, 'Add a superuser.')
        , ('import-authors', None, ImportAuthors, 'Import authors.')
        ])

    def getStore(self):
        return self.parent.getStore()
