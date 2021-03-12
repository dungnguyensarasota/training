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
    sim_params = {'gas_price_start': {'type': 'normal', 'loc': 4.15, 'scale': 0.01}}
    n_sce = 100000
    econ.generate_scenario(n_sce, sim_params, params)
    stat_dict = {
        'npv': econ.present_value_sim,
        'irr': econ.irr_sim,
        'payout': econ.payout_sim,
        'dpi': econ.dpi_sim,
        'profit': econ.profitability_sim
    }
    quantile_dict = {}
    for k in stat_dict.keys():
        stat_data = stat_dict[k]
        quantile_dict[k + "_mean"] = np.mean(stat_data)
        quantile_dict[k + "_std"] = np.std(stat_data)
        for i in range(10, 100, 10):
            quantile_dict[k + "_" + str(i) + "pct"] = np.quantile(stat_data, i / 100)

    def test_npv_mean(self):
        self.assertAlmostEqual(self.quantile_dict['npv_mean'], 471430.3309935001, places=5)

    def test_npv_std(self):
        self.assertAlmostEqual(self.quantile_dict['npv_std'], 1321.046990502022, places=5)

    def test_npv_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_10pct'], 469741.69671674154, places=5)

    def test_npv_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_20pct'], 470315.5571092581, places=5)

    def test_npv_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_30pct'], 470737.2970048548, places=5)

    def test_npv_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_40pct'], 471091.66899171594, places=5)

    def test_npv_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_50pct'], 471431.79874771356, places=5)

    def test_npv_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_60pct'], 471765.6879716476, places=5)

    def test_npv_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_70pct'], 472118.8386020648, places=5)

    def test_npv_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_80pct'], 472540.5546165076, places=5)

    def test_npv_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_90pct'], 473130.80943846214, places=5)

    def test_irr_mean(self):
        self.assertAlmostEqual(self.quantile_dict['irr_mean'], 29.422077271906165, places=5)

    def test_irr_std(self):
        self.assertAlmostEqual(self.quantile_dict['irr_std'], 0.16811053814909888, places=5)

    def test_irr_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_10pct'], 29.207382421399195, places=5)

    def test_irr_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_20pct'], 29.280133335053634, places=5)

    def test_irr_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_30pct'], 29.333670625494534, places=5)

    def test_irr_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_40pct'], 29.378702843305827, places=5)

    def test_irr_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_50pct'], 29.421965546180786, places=5)

    def test_irr_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_60pct'], 29.46447297880492, places=5)

    def test_irr_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_70pct'], 29.50947415303444, places=5)

    def test_irr_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_80pct'], 29.563268552406168, places=5)

    def test_irr_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_90pct'], 29.638664661606246, places=5)

    def test_payout_mean(self):
        self.assertAlmostEqual(self.quantile_dict['payout_mean'], 3.861414903319256, places=5)

    def test_payout_std(self):
        self.assertAlmostEqual(self.quantile_dict['payout_std'], 0.015716198265822108, places=5)

    def test_payout_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_10pct'], 3.841213115540685, places=5)

    def test_payout_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_20pct'], 3.8481942631310924, places=5)

    def test_payout_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_30pct'], 3.8531925293866585, places=5)

    def test_payout_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_40pct'], 3.8573848867553306, places=5)

    def test_payout_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_50pct'], 3.8613542513042436, places=5)

    def test_payout_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_60pct'], 3.8654034787182345, places=5)

    def test_payout_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_70pct'], 3.8696283631782706, places=5)

    def test_payout_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_80pct'], 3.8746645565088143, places=5)

    def test_payout_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_90pct'], 3.8815315349815616, places=5)

    def test_dpi_mean(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_mean'], 1.571434436645, places=5)

    def test_dpi_std(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_std'], 0.004403489968340074, places=5)

    def test_dpi_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_10pct'], 1.5658056557224718, places=5)

    def test_dpi_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_20pct'], 1.567718523697527, places=5)

    def test_dpi_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_30pct'], 1.569124323349516, places=5)

    def test_dpi_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_40pct'], 1.57030556330572, places=5)

    def test_dpi_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_50pct'], 1.5714393291590452, places=5)

    def test_dpi_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_60pct'], 1.5725522932388254, places=5)

    def test_dpi_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_70pct'], 1.5737294620068827, places=5)

    def test_dpi_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_80pct'], 1.5751351820550252, places=5)

    def test_dpi_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_90pct'], 1.5771026981282072, places=5)

    def test_profit_mean(self):
        self.assertAlmostEqual(self.quantile_dict['profit_mean'], 2.8900401185950084, places=5)

    def test_profit_std(self):
        self.assertAlmostEqual(self.quantile_dict['profit_std'], 0.00856662751702802, places=5)

    def test_profit_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_10pct'], 2.8790897883149484, places=5)

    def test_profit_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_20pct'], 2.8828111156142886, places=5)

    def test_profit_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_30pct'], 2.8855459832008488, places=5)

    def test_profit_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_40pct'], 2.8878439883707894, places=5)

    def test_profit_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_50pct'], 2.8900496365786417, places=5)

    def test_profit_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_60pct'], 2.8922148166471455, places=5)

    def test_profit_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_70pct'], 2.8945049016554303, places=5)

    def test_profit_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_80pct'], 2.8972396143792563, places=5)

    def test_profit_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_90pct'], 2.90106725505833, places=5)


if __name__ == '__main__':
    unittest.main()
