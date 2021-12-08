import math
from typing import List
from xapitrader.types import types

def mov_average(candles: List[types.RATE_INFO_RECORD], period: int) -> float:
    if len(candles) < period:
        raise ValueError("Number of candles is lower than period!")
    avg = 0
    array = candles[-period:]
    for candle in array:
        avg += candle.close
    return avg/period

def sma50(candles: List[types.RATE_INFO_RECORD]) -> float:
    return mov_average(candles, 50)

def sma200(candles: List[types.RATE_INFO_RECORD]) -> float:
    return mov_average(candles, 200)

def sma(candles: List[types.RATE_INFO_RECORD], period: int) -> float:
    return mov_average(candles, period)

def standard_deviation(candles:  List[types.RATE_INFO_RECORD], period: int):
    avg = mov_average(candles, period)
    deviations_sum = 0
    if len(candles) < period:
        raise ValueError("Number of candles is lower than period!")
    array = candles[-period:]
    for candle in array:
        closePrice = candle.close
        deviation_from_mean = closePrice-avg
        deviation = pow(deviation_from_mean,2)
        deviations_sum += deviation
    variation = deviations_sum/period
    standard_devation = math.sqrt(variation)
    return standard_devation

def bollinger_bands(candles: List[types.RATE_INFO_RECORD], period: int):
    digits = 4
    moving_avarage = sma(candles, period)
    standard_devation = standard_deviation(candles, period)
    middle_band = round(moving_avarage,digits)
    lower_band = round(moving_avarage-(2*standard_devation),digits)
    upper_band = round(moving_avarage+(2*standard_devation),digits)
    return lower_band, middle_band, upper_band