from xapitrader.core.api import APIConnector

def login(client: APIConnector, userId: int, password: str, appName: str = "") -> str:
    loginResponse = client.commandExecute('login', dict(userId=userId, password=password, appName=appName))
    status = loginResponse['status']
    if(status == False):
        raise Exception('Login failed! UserId or password might not be correct!')
    ssid = loginResponse['streamSessionId']
    return ssid
