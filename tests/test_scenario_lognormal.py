import unittest
from models.economics import Economics
import numpy as np


class TestEconomicMethods(unittest.TestCase):
    # Parameters
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
    production_arr = np.array([36500, 21900, 17520, 14016, 12614, 11353,
                               10218, 9196, 8736, 8299, 7884, 7490, 7116,
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
    sim_params = {'gas_price_start': {'type': 'log', 'loc': 4.15, 'scale': 0.5}}
    n_sce = 20000
    econ.generate_scenario(n_sce, sim_params, params)
    stat_dict = {
        'npv': econ.present_value,
        'dpi': econ.dpi,
        'profit': econ.profitability
    }

    quantile_dict = {}
    for k in stat_dict.keys():
        stat_data = stat_dict[k]
        quantile_dict[k + "_mean"] = np.mean(stat_data)
        quantile_dict[k + "_std"] = np.std(stat_data)
        for i in range(10, 100, 10):
            quantile_dict[k + "_" + str(i) + "pct"] = np.quantile(stat_data, i / 100)

    print(quantile_dict)
    def test_npv_mean(self):
        self.assertAlmostEqual(self.quantile_dict['npv_mean'], 8853361.4546165, places=5)

    def test_npv_std(self):
        self.assertAlmostEqual(self.quantile_dict['npv_std'], 4860718.099686915, places=5)

    def test_npv_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_10pct'], 3941234.293121923, places=5)

    def test_npv_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_20pct'], 4984262.904610216, places=5)

    def test_npv_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_30pct'], 5899138.250303973, places=5)

    def test_npv_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_40pct'], 6786146.786967376, places=5)

    def test_npv_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_50pct'], 7803264.903366704, places=5)

    def test_npv_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_60pct'], 8898754.567258656, places=5)

    def test_npv_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_70pct'], 10242863.879081653, places=5)

    def test_npv_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_80pct'], 12056782.828475988, places=5)

    def test_npv_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_90pct'], 15038840.843021862, places=5)

    def test_dpi_mean(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_mean'], 29.51120484872167, places=5)

    def test_dpi_std(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_std'], 16.20239366562305, places=5)

    def test_dpi_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_10pct'], 13.137447643739744, places=5)

    def test_dpi_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_20pct'], 16.614209682034055, places=5)

    def test_dpi_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_30pct'], 19.66379416767991, places=5)

    def test_dpi_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_40pct'], 22.620489289891253, places=5)

    def test_dpi_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_50pct'], 26.010883011222347, places=5)

    def test_dpi_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_60pct'], 29.66251522419552, places=5)

    def test_dpi_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_70pct'], 34.14287959693885, places=5)

    def test_dpi_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_80pct'], 40.18927609491996, places=5)

    def test_dpi_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_90pct'], 50.12946947673954, places=5)

    def test_profit_mean(self):
        self.assertAlmostEqual(self.quantile_dict['profit_mean'], 59.09944848091856, places=5)

    def test_profit_std(self):
        self.assertAlmostEqual(self.quantile_dict['profit_std'], 31.52042412168102, places=5)

    def test_profit_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_10pct'], 27.24565068920726, places=5)

    def test_profit_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_20pct'], 34.00940524787559, places=5)

    def test_profit_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_30pct'], 39.94212101606511, places=5)

    def test_profit_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_40pct'], 45.69412816846159, places=5)

    def test_profit_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_50pct'], 52.28986027084727, places=5)

    def test_profit_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_60pct'], 59.393810370116825, places=5)

    def test_profit_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_70pct'], 68.1099907174796, places=5)

    def test_profit_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_80pct'], 79.87275774792026, places=5)

    def test_profit_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_90pct'], 99.2105863251419, places=5)


if __name__ == '__main__':
    unittest.main()
