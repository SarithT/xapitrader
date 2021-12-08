from xapitrader.core.api.JsonSocket import JsonSocket
from xapitrader.core.api import settings

class APIConnector(JsonSocket):
    def __init__(self, address=settings.DEFAULT_XAPI_ADDRESS, port=settings.DEFAULT_XAPI_PORT, encrypt=True):
        super(APIConnector, self).__init__(address, port, encrypt)
        if(not self.connect()):
            raise Exception("Cannot connect to " + address + ":" + str(port) + " after " + str(settings.API_MAX_CONN_TRIES) + " retries")

    def execute(self, dictionary):
        self._sendObj(dictionary)
        return self._readObj()    

    def disconnect(self):
        self.close()
        
    def commandExecute(self,commandName, arguments=None):
        return self.execute(baseCommand(commandName, arguments))

# Command template
def baseCommand(commandName: str, arguments: dict=None):
    if arguments==None:
        arguments = dict()
    return dict([('command', commandName), ('arguments', arguments)])