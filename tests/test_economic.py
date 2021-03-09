import unittest
from models.economics import Economics
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
    params = {
        'project_length': project_length, 'mineral_tax': mineral_tax,
        'gas_price': gas_price_increase, 'royalty_rate': royalty_rate,
        'opex_increase': opex_increase, 'cost_of_capital': cost_of_capital,
        'discount_rate': discount_rate, 'gas_price_start': gas_price_start,
        'operating_cost_start': operating_cost_start, 'investment': investment,
        'production_arr': production_arr, 'gas_price_increase': gas_price_increase
    }
    econ = Economics()
    present_value, profitability, irr, payout, dpi, \
    cash, cash_cum, revenue, income, cost = econ.compute(**params)

    def test_npv(self):
        self.assertAlmostEqual(self.present_value, 457740.5772208976, places=5)

    def test_profitability(self):
        self.assertAlmostEqual(self.profitability, 2.801266038055139, places=5)

    def test_irr(self):
        self.assertAlmostEqual(self.irr, 27.71103365798545, places=5)

    def test_payout(self):
        self.assertAlmostEqual(self.payout, 4.031194375432525, places=5)

    def test_dpi(self):
        self.assertAlmostEqual(self.dpi, 1.5258019240696588, places=5)

if __name__ == '__main__':
    unittest.main()