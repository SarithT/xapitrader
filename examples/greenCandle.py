# from api import xAPIConnector
# from api.data.getChartLastRequest import ChartLastRequest, Period
# from api.data.getTickPrices import TickPrices
# from api.data.getAllSymbols import AllSymbols
# from api.data.ping import Ping
# from utils import logger as log
# from utils import time, string
# from strategy.tradingGuard import TradingGuard
# import json
# import datetime
# import time as pythonTime
# from collections import deque

# class Candle(object):
#     def __init__(self, open, close, ctm_string):
#         self._open = open
#         self._close = close
#         self._ctm_string = ctm_string
    
#     def is_green(self):
#         return self._close >= 0

# def are_last_three_candles_green(candles):
#     for candle in candles:
#         if not candle.is_green():
#             return False
#     return True

# class GreenCandleStrategy(object):
#     def __init__(self, client, symbol):
#         self._symbol = symbol
#         self._logger = log.getLogger(symbol)
#         self._client = client
#         self._timestamp = time.miliseconds_from_initial(time.now())
#         self._small_candle_locked = False
#         self._previous_small_candles = deque([],3)
#         self._previous_big_candles = deque([],3)
#         self._trading_guard = TradingGuard(symbol, self._logger)

#     def run(self):
#         self._logger.info('Running GreenCandleStrategy...')

#         big_candles = ChartLastRequest(
#             self._client,
#             time.miliseconds_from_initial(time.datetime_from_now(hours=1)),
#             Period.PERIOD_M15,
#             self._symbol,
#             time.TimeGuard(datetime.timedelta(minutes=15), offset = datetime.timedelta(minutes=1, seconds=5)))
        
#         small_candles = ChartLastRequest(
#             self._client,
#             time.miliseconds_from_initial(time.datetime_from_now(hours=1)),
#             Period.PERIOD_M5,
#             self._symbol,
#             time.TimeGuard(datetime.timedelta(minutes=5), offset = datetime.timedelta(minutes=1, seconds=5)))
        
#         prices = TickPrices(
#             self._client,
#             [self._symbol],
#             time.miliseconds_from_initial(time.datetime_from_now(days=1)),
#             time.TimeGuard(datetime.timedelta(seconds=5)))

#         # symbols = AllSymbols(self._client)
#         # x = symbols.call()
#         # x = [stc['symbol'] for stc in x['returnData']]
#         # print(x)

#         initial_response = small_candles.call()
#         self._digits = initial_response['returnData']['digits']
#         initial_candles = initial_response['returnData']['rateInfos']
#         initial_candles = initial_candles[-3:]
#         for candle in initial_candles:
#             self._previous_small_candles.append(Candle(candle['open'], candle['close'], candle['ctmString']))

#         while True:
#             tick = prices.timeGuardedCall()
#             if tick:
#                 if self._previous_small_candles[-1].is_green() and not self._trading_guard.is_open():
#                     self._trading_guard.open_transaction(tick['returnData']['quotations'][0]['ask'])

#                 if self._trading_guard.is_open():
#                     if not self._previous_small_candles[-1].is_green() and not self._small_candle_locked:
#                         self._trading_guard.close_transaction(tick['returnData']['quotations'][0]['bid'])
#                     elif are_last_three_candles_green(self._previous_small_candles) and not self._small_candle_locked:
#                         self._small_candle_locked = True
#                     elif self._small_candle_locked:
#                         if not self._previous_big_candles[-1].is_green():
#                             self._trading_guard.close_transaction(tick['returnData']['quotations'][0]['bid'])
#                             self._small_candle_locked = False

#             candles_5M = small_candles.timeGuardedCall()
#             if candles_5M:
#                 last_candle = candles_5M['returnData']['rateInfos'][-1]
#                 self._previous_small_candles.append(Candle(last_candle['open'], last_candle['close'], last_candle['ctmString']))
            
#             candles_15M = big_candles.timeGuardedCall()
#             if candles_15M:
#                 last_candle = candles_15M['returnData']['rateInfos'][-1]
#                 self._previous_big_candles.append(Candle(last_candle['open'], last_candle['close'], last_candle['ctmString']))
