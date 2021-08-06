import unittest
from main import Instrument


class MyTestCase(unittest.TestCase):
    instrument = Instrument('aaa')

    def test_one_trade_time_gap(self):
        self.instrument.add_trade(3910487, 184, 19)
        self.assertEqual(self.instrument.instrument_dict['MaxTimeGap'], 0)

    def test_volume_increase(self):
        self.instrument.add_trade(3910487, 184, 19)
        vol1 = self.instrument.instrument_dict['Volume']
        self.instrument.add_trade(3910487, 101, 11)
        self.assertEqual(self.instrument.instrument_dict['Volume'] - vol1, 101)

    def test_weighted_price(self):
        self.instrument = Instrument('aaa')
        self.instrument.add_trade(3910487, 20, 18)
        self.instrument.add_trade(3910487, 5, 7)
        self.assertEqual(int(self.instrument.instrument_dict['WeightedAveragePrice']), 15)

    def test_total_cost(self):
        self.instrument = Instrument('aaa')
        self.instrument.add_trade(3910487, 20, 18)
        self.instrument.add_trade(3910487, 5, 7)
        self.assertEqual(self.instrument.cost_of_all_trades, 395)


if __name__ == '__main__':
    unittest.main()
