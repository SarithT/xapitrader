import math
import datetime
import traceback
from xapitrader.client import APIClient
from xapitrader.utils import logger
from xapitrader.utils import time
from xapitrader.tools import indicators
from xapitrader.types import types

def upper_middle_variant(upper_band, middle_band, tick, trading_guard):
    if not trading_guard.is_open():
        ask = tick['returnData']['quotations'][0]['ask']
        if ask >= upper_band:
            trading_guard.open_transaction(ask)
    if trading_guard.is_open():
        bid = tick['returnData']['quotations'][0]['bid']
        if bid <= middle_band:
            trading_guard.close_transaction(bid)


class BollingerBandsStrategy:
    def __init__(self, client, symbol):
        self._symbol = symbol
        self._client = client
        self._timestamp = time.miliseconds_from_initial(time.now())
        self._bands_period = 20
        self._current_lower = 0
        self._current_middle = 0
        self._current_upper = 0
        self._is_open = False

    def run(self):
        logger.Logger.info('Running BollingerBandsStrategy...')
        
        # specify how to fetch candles from api -> 5 minutes candles from the last 1 day
        candles = self._client.getChartLastRequest(
            types.PERIOD.PERIOD_M5,
            time.datetime_from_now(days=1),
            self._symbol)

        # set TimeGuard for calling this only every 5 minutes with offset of 1 minute and 5 second
        # offset is set as new candle is available in xapi after 1 minute
        candles.setTimeGuard(
            time.TimeGuard(
                datetime.timedelta(minutes=types.PERIOD.PERIOD_M5),
                offset = datetime.timedelta(minutes=1, seconds=5)))

        # specify how tick price will be fetched
        prices = self._client.getTickPrices(
            [self._symbol],
            time.miliseconds_from_initial(time.datetime_from_now(days=1)))
        # set TimeGuard to call it max 10 seconds after previous call
        prices.setTimeGuard(time.TimeGuard(datetime.timedelta(seconds=10)))

        # call immediately to obtain initial candles 
        initial_candles, digits = candles.call()
        # calculate bollinger bands based on initial candles
        self._current_lower, self._current_middle, self._current_upper = indicators.bollinger_bands(initial_candles, self._bands_period)
        
        # start loop
        while True:
            # call to obtain new candles, make sure it is done only after specific time passes
            response, digits = candles.timeGuardedCall()
            # calculate bollinger bands based on new candles
            self._current_lower, self._current_middle, self._current_upper = indicators.bollinger_bands(response, self._bands_period)
            # obtain current price for symbol
            tick = prices.call()
            tick = tick[0]
            if not self._is_open:
                ask = tick.ask
                if ask >= self._current_upper:
                    # open BUY transaction with current 'ask' price
                    self.position = self._client.openTransaction(self._symbol, types.CMD.BUY, 0.1, ask)
                    self._is_open = True
            if self._is_open:
                bid = tick.bid
                if bid <= self._current_middle:
                    # close previous BUY transaction with current 'bid' price
                    self._client.closeTransaction(self.position, bid)
                    self._is_open = False

if __name__ == "__main__":
    userId = 'xxxxx'
    password = 'yyyyy'

    client = APIClient() # create client
    ssid = client.login(userId, password) # login to application using xtb credentials
    symbol = 'EURUSD'

    try:
        BollingerBandsStrategy(client, symbol).run()
    except Exception as err:
        traceback.print_exc()
        print(err)
    finally:
        # graceful shutdown
        client.logout()
        client.disconnect()