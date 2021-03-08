import unittest
from gas_model_changing_price import compute_economic
import numpy as np

class TestEconomicMethods(unittest.TestCase):
    # parameter values
    project_length = 20
    mineral_tax = 2.5 / 100
    gas_price_increase = 5 / 100
    royalty_rate = 15.625 / 100
    opex_increase = 5 / 100
    cost_of_capital = 9 / 100
    discount_rate = 10 / 100
    gas_price_start = 4.15
    operating_cost_start = 6000
    investment = 300000
    # Some input arrays
    production_arr = np.array([36500, 21900, 17520, 14016, 12614, 11353, \
                               10218, 9196, 8736, 8299, 7884, 7490, 7116, \
                               6760, 6422, 6101, 5796, 5506, 5231, 4969], dtype=float)
    present_value, profitablity, irr, payout = compute_economic(project_length, mineral_tax, royalty_rate, \
                                                                investment, operating_cost_start, opex_increase, \
                                                                gas_price_start, gas_price_increase, discount_rate,
                                                                production_arr)
    def test_npv(self):
        self.assertAlmostEqual(self.present_value, 457740.5772208976, places=5)

    def test_profitability(self):
        self.assertAlmostEqual(self.profitablity, 2.801266038055139, places=5)

    def test_irr(self):
        self.assertAlmostEqual(self.irr, 27.71103365798545, places=5)

    def test_payout(self):
        self.assertAlmostEqual(self.payout, 4.031194375432525, places=5)

if __name__ == '__main__':
    unittest.main()