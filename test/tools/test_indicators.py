import unittest
from xapitrader.tools import indicators
from xapitrader.types import types
from xapitrader.tools.indicators import standard_deviation

class IndicatorsTests(unittest.TestCase):

    def setUp(self):
        self.candles = [
            self.get_rate_info_record(3.0, 5.0),
            self.get_rate_info_record(5.0, 6.0),
            self.get_rate_info_record(6.0, 2.0),
            self.get_rate_info_record(2.0, 3.0)
        ]

    def get_rate_info_record(self, open: float, close: float):
        return types.RATE_INFO_RECORD(close, 0, '0', close+2.0, open-1.0, open, 20)

    def test_mov_average(self):
        period = 4
        expected_avg = 4.0
        avg = indicators.mov_average(self.candles, period)
        self.assertEqual(avg, expected_avg)

    def test_standard_deviation(self):
        period = 4
        expected_standard_deviation =  1.5811
        standard_deviation = round(indicators.standard_deviation(self.candles, period),4)
        self.assertEqual(standard_deviation, expected_standard_deviation)

    def test_bollinger_bands(self):
        period = 4
        expected_avg = 4.0
        expected_standard_deviation =  1.5811
        expected_lower_band = 0.8377
        expected_higher_band = 7.1623
        l,m,h = indicators.bollinger_bands(self.candles, period)
        self.assertEqual(l, expected_lower_band)
        self.assertEqual(m, expected_avg)
        self.assertEqual(h, expected_higher_band)

    def test_calculate_bollinger_bands_for_period_only(self):
        period = 3
        l,m,h = indicators.bollinger_bands(self.candles, period)
        self.assertEqual(l, 32426.13)
        self.assertEqual(m, 5.5)
        self.assertEqual(h, 32551.49)

    def test_raise_value_exception_if_period_greater_than_response(self):
        period = 5
        with self.assertRaises(ValueError):
            l,m,h = indicators.bollinger_bands(self.candles, period)

if __name__ == '__main__':
    unittest.main()