from xapitrader.types import types

def is_green_candle(candle: types.RATE_INFO_RECORD):
    return candle.close > candle.open

def is_red_candle(candle: types.RATE_INFO_RECORD):
    return not is_green_candle(candle)
