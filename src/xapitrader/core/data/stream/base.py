class StreamDataInterface:
    def __init__(self, client, streamSessionId: str):
        self._client = client
        self._streamSessionId = streamSessionId

    def _command(self):
        """Execute command on client"""
        pass

    def _set_func(self):
        """Execute command on client"""
        pass

    def _handleResponse(self, jsonResponse):
        """Format response"""
        pass


    def subscribe(self, callback):
        """Return a response from executed command on client"""
        self._set_func(callback)
        command = self._command()
        command['streamSessionId'] = self._streamSessionId
        self._client.execute(command)

    def unsubscribe(self):
        """Return a response from executed command on client"""
        command = self._command()
        stopCommand = 'stop' + self._command()['command'][2:]
        command['command'] = stopCommand
        command['streamSessionId'] = self._streamSessionId
        self._client.execute(command)


