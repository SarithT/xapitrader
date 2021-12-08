from xapitrader.utils import time
from xapitrader.types import types

class Transaction():
    def __init__(self, position, trade_info: types.TRADE_TRANS_INFO):
        self._position = position
        self._trade_info = trade_info

    def getTradeInfo(self) -> types.TRADE_TRANS_INFO:
        return self._trade_info

    def open(self):
        self._openPrice = self._trade_info.price
        self._is_open = True
        self._open_date = time.now()
    
    def close(self, closePrice):
        if self._is_open:
            self._closePrice = closePrice
            self._close_date = time.now()
            self._profit = self._closePrice - self._openPrice
            self._profit_percent = (self._profit/self._openPrice)*100
            self._is_open = False
            filename = self._trade_info.symbol
            with open(f'{filename}.log', mode='a+',encoding = 'utf-8') as f:
                details = self._get_string()
                f.write(details + "\n")

    def _get_string(self):
        if not self._is_open:
            open_time = self._open_date.strftime("%m/%d/%Y, %H:%M:%S")
            close_time = self._close_date.strftime("%m/%d/%Y, %H:%M:%S")
            return f'{self._position} {open_time} {self._openPrice} {close_time} {self._closePrice} {self._profit} {self._profit_percent}'
        return 'error'