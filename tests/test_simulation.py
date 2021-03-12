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
    npv_mean = econ.present_value_mean
    npv_std = econ.present_value_std
    npv_10pct = econ.present_value_10pct
    npv_20pct = econ.present_value_20pct
    npv_30pct = econ.present_value_30pct
    npv_40pct = econ.present_value_40pct
    npv_50pct = econ.present_value_50pct
    npv_60pct = econ.present_value_60pct
    npv_70pct = econ.present_value_70pct
    npv_80pct = econ.present_value_80pct
    npv_90pct = econ.present_value_90pct
    irr_mean = econ.irr_mean
    irr_std = econ.irr_std
    irr_10pct = econ.irr_10pct
    irr_20pct = econ.irr_20pct
    irr_30pct = econ.irr_30pct
    irr_40pct = econ.irr_40pct
    irr_50pct = econ.irr_50pct
    irr_60pct = econ.irr_60pct
    irr_70pct = econ.irr_70pct
    irr_80pct = econ.irr_80pct
    irr_90pct = econ.irr_90pct
    payout_mean = econ.payout_mean
    payout_std = econ.payout_std
    payout_10pct = econ.payout_10pct
    payout_20pct = econ.payout_20pct
    payout_30pct = econ.payout_30pct
    payout_40pct = econ.payout_40pct
    payout_50pct = econ.payout_50pct
    payout_60pct = econ.payout_60pct
    payout_70pct = econ.payout_70pct
    payout_80pct = econ.payout_80pct
    payout_90pct = econ.payout_90pct
    dpi_mean = econ.dpi_mean
    dpi_std = econ.dpi_std
    dpi_10pct = econ.dpi_10pct
    dpi_20pct = econ.dpi_20pct
    dpi_30pct = econ.dpi_30pct
    dpi_40pct = econ.dpi_40pct
    dpi_50pct = econ.dpi_50pct
    dpi_60pct = econ.dpi_60pct
    dpi_70pct = econ.dpi_70pct
    dpi_80pct = econ.dpi_80pct
    dpi_90pct = econ.dpi_90pct
    profit_mean = econ.profit_mean
    profit_std = econ.profit_std
    profit_10pct = econ.profit_10pct
    profit_20pct = econ.profit_20pct
    profit_30pct = econ.profit_30pct
    profit_40pct = econ.profit_40pct
    profit_50pct = econ.profit_50pct
    profit_60pct = econ.profit_60pct
    profit_70pct = econ.profit_70pct
    profit_80pct = econ.profit_80pct
    profit_90pct = econ.profit_90pct

    def test_npv_mean(self):
        self.assertAlmostEqual(self.npv_mean, 471430.3309935001, places=5)

    def test_npv_std(self):
        self.assertAlmostEqual(self.npv_std, 1321.046990502022, places=5)

    def test_npv_10pct(self):
        self.assertAlmostEqual(self.npv_10pct, 469741.69671674154, places=5)

    def test_npv_20pct(self):
        self.assertAlmostEqual(self.npv_20pct, 470315.5571092581, places=5)

    def test_npv_30pct(self):
        self.assertAlmostEqual(self.npv_30pct, 470737.2970048548, places=5)

    def test_npv_40pct(self):
        self.assertAlmostEqual(self.npv_40pct, 471091.66899171594, places=5)

    def test_npv_50pct(self):
        self.assertAlmostEqual(self.npv_50pct, 471431.79874771356, places=5)

    def test_npv_60pct(self):
        self.assertAlmostEqual(self.npv_60pct, 471765.6879716476, places=5)

    def test_npv_70pct(self):
        self.assertAlmostEqual(self.npv_70pct, 472118.8386020648, places=5)

    def test_npv_80pct(self):
        self.assertAlmostEqual(self.npv_80pct, 472540.5546165076, places=5)

    def test_npv_90pct(self):
        self.assertAlmostEqual(self.npv_90pct, 473130.80943846214, places=5)

    def test_irr_mean(self):
        self.assertAlmostEqual(self.irr_mean, 29.422077271906165, places=5)

    def test_irr_std(self):
        self.assertAlmostEqual(self.irr_std, 0.16811053814909888, places=5)

    def test_irr_10pct(self):
        self.assertAlmostEqual(self.irr_10pct, 29.207382421399195, places=5)

    def test_irr_20pct(self):
        self.assertAlmostEqual(self.irr_20pct, 29.280133335053634, places=5)

    def test_irr_30pct(self):
        self.assertAlmostEqual(self.irr_30pct, 29.333670625494534, places=5)

    def test_irr_40pct(self):
        self.assertAlmostEqual(self.irr_40pct, 29.378702843305827, places=5)

    def test_irr_50pct(self):
        self.assertAlmostEqual(self.irr_50pct, 29.421965546180786, places=5)

    def test_irr_60pct(self):
        self.assertAlmostEqual(self.irr_60pct, 29.46447297880492, places=5)

    def test_irr_70pct(self):
        self.assertAlmostEqual(self.irr_70pct, 29.50947415303444, places=5)

    def test_irr_80pct(self):
        self.assertAlmostEqual(self.irr_80pct, 29.563268552406168, places=5)

    def test_irr_90pct(self):
        self.assertAlmostEqual(self.irr_90pct, 29.638664661606246, places=5)

    def test_payout_mean(self):
        self.assertAlmostEqual(self.payout_mean, 3.861414903319256, places=5)

    def test_payout_std(self):
        self.assertAlmostEqual(self.payout_std, 0.015716198265822108, places=5)

    def test_payout_10pct(self):
        self.assertAlmostEqual(self.payout_10pct, 3.841213115540685, places=5)

    def test_payout_20pct(self):
        self.assertAlmostEqual(self.payout_20pct, 3.8481942631310924, places=5)

    def test_payout_30pct(self):
        self.assertAlmostEqual(self.payout_30pct, 3.8531925293866585, places=5)

    def test_payout_40pct(self):
        self.assertAlmostEqual(self.payout_40pct, 3.8573848867553306, places=5)

    def test_payout_50pct(self):
        self.assertAlmostEqual(self.payout_50pct, 3.8613542513042436, places=5)

    def test_payout_60pct(self):
        self.assertAlmostEqual(self.payout_60pct, 3.8654034787182345, places=5)

    def test_payout_70pct(self):
        self.assertAlmostEqual(self.payout_70pct, 3.8696283631782706, places=5)

    def test_payout_80pct(self):
        self.assertAlmostEqual(self.payout_80pct, 3.8746645565088143, places=5)

    def test_payout_90pct(self):
        self.assertAlmostEqual(self.payout_90pct, 3.8815315349815616, places=5)

    def test_dpi_mean(self):
        self.assertAlmostEqual(self.dpi_mean, 1.571434436645, places=5)

    def test_dpi_std(self):
        self.assertAlmostEqual(self.dpi_std, 0.004403489968340074, places=5)

    def test_dpi_10pct(self):
        self.assertAlmostEqual(self.dpi_10pct, 1.5658056557224718, places=5)

    def test_dpi_20pct(self):
        self.assertAlmostEqual(self.dpi_20pct, 1.567718523697527, places=5)

    def test_dpi_30pct(self):
        self.assertAlmostEqual(self.dpi_30pct, 1.569124323349516, places=5)

    def test_dpi_40pct(self):
        self.assertAlmostEqual(self.dpi_40pct, 1.57030556330572, places=5)

    def test_dpi_50pct(self):
        self.assertAlmostEqual(self.dpi_50pct, 1.5714393291590452, places=5)

    def test_dpi_60pct(self):
        self.assertAlmostEqual(self.dpi_60pct, 1.5725522932388254, places=5)

    def test_dpi_70pct(self):
        self.assertAlmostEqual(self.dpi_70pct, 1.5737294620068827, places=5)

    def test_dpi_80pct(self):
        self.assertAlmostEqual(self.dpi_80pct, 1.5751351820550252, places=5)

    def test_dpi_90pct(self):
        self.assertAlmostEqual(self.dpi_90pct, 1.5771026981282072, places=5)

    def test_profit_mean(self):
        self.assertAlmostEqual(self.profit_mean, 2.8900401185950084, places=5)

    def test_profit_std(self):
        self.assertAlmostEqual(self.profit_std, 0.00856662751702802, places=5)

    def test_profit_10pct(self):
        self.assertAlmostEqual(self.profit_10pct, 2.8790897883149484, places=5)

    def test_profit_20pct(self):
        self.assertAlmostEqual(self.profit_20pct, 2.8828111156142886, places=5)

    def test_profit_30pct(self):
        self.assertAlmostEqual(self.profit_30pct, 2.8855459832008488, places=5)

    def test_profit_40pct(self):
        self.assertAlmostEqual(self.profit_40pct, 2.8878439883707894, places=5)

    def test_profit_50pct(self):
        self.assertAlmostEqual(self.profit_50pct, 2.8900496365786417, places=5)

    def test_profit_60pct(self):
        self.assertAlmostEqual(self.profit_60pct, 2.8922148166471455, places=5)

    def test_profit_70pct(self):
        self.assertAlmostEqual(self.profit_70pct, 2.8945049016554303, places=5)

    def test_profit_80pct(self):
        self.assertAlmostEqual(self.profit_80pct, 2.8972396143792563, places=5)

    def test_profit_90pct(self):
        self.assertAlmostEqual(self.profit_90pct, 2.90106725505833, places=5)


if __name__ == '__main__':
    unittest.main()
