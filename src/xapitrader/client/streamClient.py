from typing import List
from xapitrader.core.api import APIStreamConnector
from xapitrader.core.data.stream import commands
from xapitrader.core import auth
from xapitrader.types import types
from datetime import datetime

class APIStreamClient():
    def __init__(self, ssId: str) -> None:
        self._client = APIStreamConnector(ssId=ssId)
        self._ssid = ssId

    def disconnect(self):
        return self._client.disconnect()

    def getBalance(self):
        return commands.getBalance(self._client, self._ssid)

    def getCandles(self, symbol: str):
        return commands.getBalance(self._client, self._ssid, symbol)

    def getKeepAlive(self):
        return commands.getKeepAlive(self._client, self._ssid)

    def getNews(self):
        return commands.getNews(self._client, self._ssid)

    def getProfits(self):
        return commands.getProfits(self._client, self._ssid)

    def getTickPrices(self, symbol: str, minArrivalTime: int = 1, maxLevel: int = 2):
        return commands.getTickPrices(self._client, self._ssid, symbol, minArrivalTime, maxLevel)

    def getTrades(self):
        return commands.getTrades(self._client, self._ssid)

    def getTradeStatus(self):
        return commands.getTradeStatus(self._client, self._ssid)

    def ping(self):
        return commands.ping(self._client, self._ssid)
