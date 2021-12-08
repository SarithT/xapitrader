from xapitrader.utils.time import TimeGuard

class RetriveDataInterface:
    def __init__(self, client):
        self._client = client

    def _executeCommand(self):
        """Execute command on client"""
        pass

    def _parseResponse(self, jsonResponse: dict):
        """Format response"""
        pass

    def _handleResponse(self, jsonResponse: dict):
        """Handle response"""
        status = jsonResponse['status']
        if status == False:
            errorCode = jsonResponse['errorCode']
            errorDescr = jsonResponse['errorDescr']
            raise Exception(f'{errorCode} - {errorDescr}')
        return self._parseResponse(jsonResponse)

    def setTimeGuard(self, timeGuard: TimeGuard):
        """Sets TimeGuard for timeGuardedCall"""
        self._timeGuard = timeGuard
        self._timeGuard.start()

    def call(self):
        """Return a response from executed command on client"""
        response = self._executeCommand()
        return self._handleResponse(response)

    def timeGuardedCall(self):
        """
        Execute command on client with specific interval between calls using TimeGuard.
        It blocks execution until interval condition is met.
        """
        if self._timeGuard is None:
            raise Exception('TimeGuard is not set!')
        if self._timeGuard.passed():
            return self.call()
