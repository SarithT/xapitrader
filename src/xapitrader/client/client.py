from typing import List
from xapitrader.core.api import APIConnector
from xapitrader.core.data.retreive import commands
from xapitrader.core import auth
from xapitrader.core.data.transaction import TradingGuard
from xapitrader.core.data.transaction import SimulatingTradingGuard
from xapitrader.types import types
from datetime import datetime
from xapitrader import settings

class APIClient():
    def __init__(self) -> None:
        self._client = APIConnector()

    def disconnect(self):
        self._client.disconnect()
    
    def login(self, userId, password) -> int:
        return auth.login(self._client, userId, password)

    def logout(self):
        return auth.logout(self._client)

    def getAllSymbols(self):
        return commands.getAllSymbols(self._client)

    def getChartRangeRequest(self, end: datetime, period: types.PERIOD, start: datetime, symbol: str, ticks = 0):
        return commands.getChartRangeRequest(self._client, end, period, start, symbol, ticks)

    def getChartLastRequest(self, period: types.PERIOD, start: datetime, symbol: str):
        return commands.getChartLastRequest(self._client, period, start, symbol)

    def getCommissionDef(self, symbol: str, volume: float):
        return commands.getCommissionDef(self._client, symbol, volume)

    def getCurrentUserData(self):
        return commands.getCurrentUserData(self._client)

    def getMarginLevel(self):
        return commands.getMarginLevel(self._client)

    def getMarginTrade(self, symbol: str, volume: float):
        return commands.getMarginTrade(self._client, symbol, volume)

    def getProfitCalculation(self, closePrice: float, cmd: types.CMD, openPrice: float, symbol: str, volume: float):
        return commands.getProfitCalculation(self._client, closePrice, cmd, openPrice, symbol, volume)

    def getServerTime(self):
        return commands.getServerTime(self._client)

    def getSymbol(self, symbol: str):
        return commands.getProfitCalculation(self._client, symbol)

    def getTickPrices(self, symbols: List[str], timestamp: int, level: types.Level = 0):
        return commands.getTickPrices(self._client, symbols, timestamp, level)

    def getTradeRecords(self, orders: List[int]):
        return commands.getTradeRecords(self._client, orders)

    def getTrades(self, openedOnly: bool):
        return commands.getTrades(self._client, openedOnly)

    def getTradingHours(self, symbols: List[str]):
        return commands.getTradingHours(self._client, symbols)

    def ping(self):
        return commands.ping(self._client)

    def tradeTransaction(self, symbol: str, cmd: types.CMD, type: types.TRANSACTION_TYPE, volume: float, price: float, sl: float=0.0, tp: float=0.0, offset: int=0, order: int=0, expiration: int=0, customComment: str=""):
        trade_info = types.TRADE_TRANS_INFO(cmd, customComment, expiration, offset, order, price, sl, symbol, tp, type, volume)
        return commands.tradeTransaction(self._client, trade_info)

    def tradeTransactionStatus(self, order: int):
        return commands.tradeTransactionStatus(self._client, order)

    def openTransaction(self, symbol: str, cmd: types.CMD, volume: float, price: float, sl: float=0.0, tp: float=0.0, offset: int=0, expiration: int=0, customComment: str=""):
        trade_info = types.TRADE_TRANS_INFO(cmd, customComment, expiration, offset, types.TRANSACTION_TYPE.OPEN, price, sl, symbol, tp, type, volume)
        if settings.SIMULATION_MODE:
            return SimulatingTradingGuard.open_transaction(self._client, trade_info)
        else:
            return TradingGuard.open_transaction(self._client, trade_info)

    def closeTransaction(self, position:int, closePrice: float):
        if settings.SIMULATION_MODE:
            return SimulatingTradingGuard.close_transaction(self._client, position, closePrice)
        else:
            return TradingGuard.close_transaction(self._client, position, closePrice)

