import unittest
from unittest.mock import Mock
import datetime
from xapitrader.utils import time

class TimeTests(unittest.TestCase):


    def test_delta_miliseconds(self):
        from_date = datetime.datetime(year=2010, month=5, day=4)
        to_date = datetime.datetime(year=2010, month=4, day=6)
        from_date_miliseconds = 1272963600000
        to_date_miliseconds = 1270544400000
        delta = time.delta_miliseconds(from_date, to_date)
        self.assertEqual(delta, from_date_miliseconds-to_date_miliseconds)

    def test_datetime_from_now(self):
        time.now=Mock(return_value=datetime.datetime(year=2010, month=4, day=10))
        date = time.datetime_from_now(days=5, hours=4)
        self.assertEqual(date,datetime.datetime(year=2010, month=4, day=4, hour=20))

    def test_miliseconds_from_initial(self):
        to_date = datetime.datetime(year=2010, month=5, day=4)
        ms_from_initial= time.miliseconds_from_initial(to_date)
        expected_miliseconds = 1272931200000
        self.assertEqual(ms_from_initial, expected_miliseconds)



if __name__ == '__main__':
    unittest.main()