from xapitrader.core.api import APIConnector

def logout(client: APIConnector) -> str:
    loginResponse = client.commandExecute('logout')
    status = loginResponse['status']
    if(status == False):
        raise Exception('Logout failed!')
    return status