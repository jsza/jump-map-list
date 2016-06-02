import json

from jumpmaplist.items import LogEntry



class BaseDatabase(object):
    def __init__(self, store, db):
        self.store = store
        self.db = db


    def logEntry(self, logType, data, superuser):
        LogEntry(store=self.store, logType=logType,
                 data=json.dumps(data).decode('ascii'), superuser=superuser)
