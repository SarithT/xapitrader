from typing import List
from xapitrader.core.data.retreive.base import RetriveDataInterface
from xapitrader.core.api import APIConnector
from xapitrader.types import types
from xapitrader.types import utils
from xapitrader.utils import time
from datetime import datetime

class getAllSymbols(RetriveDataInterface):
    def __init__(self, client: APIConnector):
        super().__init__(client)

    def _executeCommand(self):
        return self._client.commandExecute('getAllSymbols')

    def _parseResponse(self, jsonResponse: dict):
        data = [utils.unpack_to(record, types.SYMBOL_RECORD) for record in jsonResponse['returnData']]
        return data
        

class getChartRangeRequest(RetriveDataInterface):

    def __init__(self, client: APIConnector, end: datetime, period: types.PERIOD, start: datetime, symbol: str, ticks = 0):
        super().__init__(client)
        self._end = end
        self._period = period
        self._start = start
        self._symbol = symbol
        self._ticks = ticks
        self._validate()

    def _validate(self):
        if self._end > time.now():
            raise Exception("Specified end date is greater than now!")
        
        if not self._validate_time_period():
            raise Exception("Time period cannot be use for specified candle period!")

        if not self._validate_time_period():
            raise Exception("Time range cannot be use for specified candle period!")

        return True
        
    def _validate_time_period(self):
        time_period = time.delta_miliseconds(self._start, self._end)
    
        if self._period in [types.PERIOD.PERIOD_M1, types.PERIOD.PERIOD_M5, types.PERIOD.PERIOD_M15]:
            return True if time_period < time.DELTA_ONE_MONTH else False

        if self._period in [types.PERIOD.PERIOD_M30, types.PERIOD.PERIOD_H1, types.PERIOD.PERIOD_H4]:
            return True if time_period < time.DELTA_SIX_MONTHS else False

        if self._period in [types.PERIOD.PERIOD_D1, types.PERIOD.PERIOD_W1, types.PERIOD.PERIOD_MN1]:
            return True if time_period < time.DELTA_SIX_MONTHS else False

    def _validate_time_range(self):
        time_range = time.delta_miliseconds(self._start, time.now())
    
        if self._period in [types.PERIOD.PERIOD_M1, types.PERIOD.PERIOD_M5, types.PERIOD.PERIOD_M15]:
            return True if time_range < time.DELTA_ONE_MONTH else False

        if self._period in [types.PERIOD.PERIOD_M30, types.PERIOD.PERIOD_H1]:
            return True if time_range < time.DELTA_SEVEN_MONTHS else False

        if self._period in [types.PERIOD.PERIOD_H4, types.PERIOD.PERIOD_D1, types.PERIOD.PERIOD_W1, types.PERIOD.PERIOD_MN1]:
            return True if time_range < time.DELTA_THIRTEEN_MONTHS else False

    def _executeCommand(self):
        return self._client.commandExecute('getChartRangeRequest',
            dict(info=dict(
                end=time.miliseconds_from_initial(self._end),
                period=self._period,
                start=time.miliseconds_from_initial(self._start),
                ticks=self._ticks,
                symbol=self._symbol)))
    
    def _parseResponse(self, jsonResponse: dict):
        digits = jsonResponse['returnData']["digits"]
        data = [utils.unpack_to(record, types.RATE_INFO_RECORD) for record in jsonResponse['returnData']["rateInfos"]]
        return data, digits

class getChartLastRequest(getChartRangeRequest):
    def __init__(self, client: APIConnector, period: types.PERIOD, start: datetime, symbol: str):
        super().__init__(client, time.now(), period, start, symbol, 0)

    def _executeCommand(self):
        return self._client.commandExecute('getChartLastRequest',
            dict(info=dict(
                period=self._period,
                start=time.miliseconds_from_initial(self._start),
                symbol=self._symbol)))

class getCommissionDef(RetriveDataInterface):
    def __init__(self, client: APIConnector, symbol: str, volume: float):
        super().__init__(client)
        self._symbol = symbol
        self._volume = volume

    def _executeCommand(self):
        return self._client.commandExecute('getCommissionDef',
            dict(symbol=self._symbol,
                volume=self._volume))

    def _parseResponse(self, jsonResponse: dict):
        commission = jsonResponse['returnData']['commission']
        rateOfExchange = jsonResponse['returnData']['rateOfExchange']
        return commission, rateOfExchange

class getCurrentUserData(RetriveDataInterface):
    def __init__(self, client: APIConnector):
        super().__init__(client)

    def _executeCommand(self):
        return self._client.commandExecute('getCurrentUserData')

    def _parseResponse(self, jsonResponse: dict):
        return jsonResponse['returnData']

class getMarginLevel(RetriveDataInterface):
    def __init__(self, client: APIConnector):
        super().__init__(client)

    def _executeCommand(self):
        return self._client.commandExecute('getMarginLevel')

    def _parseResponse(self, jsonResponse: dict):
        return jsonResponse['returnData']

class getMarginTrade(RetriveDataInterface):
    def __init__(self, client: APIConnector, symbol: str, volume: float):
        super().__init__(client)
        self._symbol = symbol
        self._volume = volume

    def _executeCommand(self):
        return self._client.commandExecute('getMarginTrade',
            dict(symbol=self._symbol,
                volume=self._volume))

    def _parseResponse(self, jsonResponse: dict):
        return jsonResponse['returnData']

class getProfitCalculation(RetriveDataInterface):

    def __init__(self, client: APIConnector, closePrice: float, cmd: types.CMD, openPrice: float, symbol: str, volume: float):
        super().__init__(client)
        self._closePrice = closePrice
        self._cmd = cmd
        self._openPrice = openPrice
        self._symbol = symbol
        self._volume = volume

    def _executeCommand(self):
        return self._client.commandExecute('getMarginTrade',
            dict(closePrice=self._closePrice,
                cmd=self._cmd,
                openPrice=self._openPrice,
                symbol=self._symbol,
                volume=self._volume))

    def _parseResponse(self, jsonResponse: dict):
        return jsonResponse['returnData']

class getServerTime(RetriveDataInterface):
    def __init__(self, client: APIConnector):
        super().__init__(client)

    def _executeCommand(self):
        return self._client.commandExecute('getServerTime', dict())

    def _parseResponse(self, jsonResponse: dict):
        return jsonResponse['returnData']

class getSymbol(RetriveDataInterface):
    def __init__(self, client: APIConnector, symbol: str):
        super().__init__(client)
        self._symbol = symbol

    def _executeCommand(self):
        return self._client.commandExecute('getSymbol',
            dict(symbol=self._symbol))
    
    def _parseResponse(self, jsonResponse: dict) -> dict:
        data = utils.unpack_to(jsonResponse['returnData'], types.SYMBOL_RECORD)
        return data

class getTickPrices(RetriveDataInterface):

    def __init__(self, client: APIConnector, symbols: List[str], timestamp: int, level: types.Level = 0):
        super().__init__(client)
        self._level = level
        self._symbols = symbols
        self._timestamp = timestamp

    def _executeCommand(self):
        return self._client.commandExecute('getTickPrices',
            dict(level=self._level,
                symbols=self._symbols,
                timestamp=self._timestamp
            ))

    def _parseResponse(self, jsonResponse: dict) -> dict:
        data = [utils.unpack_to(record, types.TICK_RECORD) for record in jsonResponse['returnData']["quotations"]]
        return data

class getTradeRecords(RetriveDataInterface):
    def __init__(self, client: APIConnector, orders: List[int]):
        super().__init__(client)
        self._orders = orders

    def _executeCommand(self):
        return self._client.commandExecute('getTradeRecords',
            dict(
                orders=self._orders)
            )

    def _parseResponse(self, jsonResponse: dict) -> dict:
        data = [utils.unpack_to(record, types.TRADE_RECORD) for record in jsonResponse['returnData']]
        return data

class getTrades(RetriveDataInterface):
    def __init__(self, client: APIConnector, openedOnly: bool):
        super().__init__(client)
        self._openedOnly = openedOnly

    def _executeCommand(self):
        return self._client.commandExecute('getTrades',
            dict(
                openedOnly=self._openedOnly
            ))

    def _parseResponse(self, jsonResponse: dict) -> dict:
        data = [utils.unpack_to(record, types.TRADE_RECORD) for record in jsonResponse['returnData']]
        return data

class getTradingHours(RetriveDataInterface):
    def __init__(self, client: APIConnector, symbols: List[str]):
        super().__init__(client)
        self._symbols = symbols

    def _executeCommand(self):
        return self._client.commandExecute('getTradingHours',
            dict(
                symbols=self._symbols
            ))

    def _parseResponse(self, jsonResponse: dict) -> dict:
        data = [utils.unpack_to(record, types.TRADING_HOURS_RECORD) for record in jsonResponse['returnData']]
        return data


class ping(RetriveDataInterface):
    def __init__(self, client: APIConnector):
        super().__init__(client)

    def _executeCommand(self):
        return self._client.commandExecute('ping', dict())

    def _parseResponse(self, jsonResponse: dict):
        return jsonResponse['returnData']

class tradeTransaction(RetriveDataInterface):

    def __init__(self, client, trade_trans_info: types.TRADE_TRANS_INFO):
        super().__init__(client)
        self._trade_trans_info = trade_trans_info
    def _executeCommand(self):
        return self._client.commandExecute('tradeTransaction',
            dict(
                tradeTransInfo=dict(
                    cmd=self._trade_trans_info.cmd,
                    type=self._trade_trans_info.type,
                    volume=self._trade_trans_info.volume,
                    price=self._trade_trans_info.price,
                    sl=self._trade_trans_info.sl,
                    tp=self._trade_trans_info.tp,
                    offset=self._trade_trans_info.offset,
                    order=self._trade_trans_info.order,
                    expiration=self._trade_trans_info.expiration,
                    customComment=self._trade_trans_info.customComment,
                )
            ))

    def _parseResponse(self, jsonResponse: dict):
        return jsonResponse['returnData']

class tradeTransactionStatus(RetriveDataInterface):
    def __init__(self, client: APIConnector, order: int):
        super().__init__(client)
        self._order = order

    def _executeCommand(self):
        return self._client.commandExecute('tradeTransactionStatus', 
            dict(
                order=self._order
            ))

    def _parseResponse(self, jsonResponse: dict):
        return types.TRADE_TRANSACTION_STATUS(jsonResponse['returnData'])
