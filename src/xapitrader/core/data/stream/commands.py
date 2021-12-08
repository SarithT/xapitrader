from xapitrader.core.data.stream.base import StreamDataInterface
from xapitrader.types import types
from xapitrader.types import utils


class getBalance(StreamDataInterface):
    def __init__(self, client, streamSessionId: str):
        super().__init__(client, streamSessionId)

    def _set_func(self, callback):
        self._client.set_balanceFun(callback)

    def _command(self):
        return dict(command='getBalance')

    def _handleResponse(self, jsonResponse):
        jsonResponse['data'] = utils.unpack_to(jsonResponse['data'], types.STREAMING_BALANCE_RECORD)
        return jsonResponse

class getCandles(StreamDataInterface):
    def __init__(self, client, streamSessionId: str, symbol: str):
        super().__init__(client, streamSessionId)
        self._symbol = symbol

    def _set_func(self, callback):
        self._client.set_candlesFun(callback)

    def _command(self):
        return dict(command='getCandles', symbol=self._symbol)

    def _handleResponse(self, jsonResponse):
        jsonResponse['data'] = utils.unpack_to(jsonResponse['data'], types.STREAMING_CANDLE_RECORD)
        return jsonResponse

class getKeepAlive(StreamDataInterface):
    def __init__(self, client, streamSessionId: str):
        super().__init__(client, streamSessionId)

    def _command(self):
        return dict(command='getKeepAlive')

    def _handleResponse(self, jsonResponse):
        return jsonResponse

class getNews(StreamDataInterface):
    def __init__(self, client, streamSessionId: str):
        super().__init__(client, streamSessionId)

    def _command(self):
        return dict(command='getNews')

    def _handleResponse(self, jsonResponse):
        return jsonResponse

class getProfits(StreamDataInterface):
    def __init__(self, client, streamSessionId: str):
        super().__init__(client, streamSessionId)

    def _command(self):
        return dict(command='getProfits')

    def _handleResponse(self, jsonResponse):
        jsonResponse['data'] = utils.unpack_to(jsonResponse['data'], types.STREAMING_PROFIT_RECORD)
        return jsonResponse

class getTickPrices(StreamDataInterface):
    def __init__(self, client, streamSessionId: str, symbol: str, minArrivalTime: int = 1, maxLevel: int = 2):
        super().__init__(client, streamSessionId)
        self._symbol = symbol
        self._minArrivalTime = minArrivalTime
        self._maxLevel = maxLevel

    def _command(self):
        return dict(command='getTickPrices', symbol=self._symbol, minArrivalTime=self._minArrivalTime, maxLevel=self._maxLevel)
    
    def _handleResponse(self, jsonResponse):
        return jsonResponse

    def _handleResponse(self, jsonResponse):
        jsonResponse['data'] = utils.unpack_to(jsonResponse['data'], types.TICK_RECORD)
        return jsonResponse

class getTrades(StreamDataInterface):
    def __init__(self, client, streamSessionId: str):
        super().__init__(client, streamSessionId)

    def _command(self):
        return dict(command='getTrades')

    def _handleResponse(self, jsonResponse):
        jsonResponse['data'] = utils.unpack_to(jsonResponse['data'], types.STREAMING_TRADE_RECORD)
        return jsonResponse

class getTradeStatus(StreamDataInterface):
    def __init__(self, client, streamSessionId: str):
        super().__init__(client, streamSessionId)

    def _command(self):
        return dict(command='getTradeStatus')

class ping(StreamDataInterface):
    def __init__(self, client, streamSessionId: str):
        super().__init__(client, streamSessionId)

    def _command(self):
        return dict(command='ping')