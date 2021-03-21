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
    n_sce = 20000
    econ.generate_scenario(n_sce, sim_params, params, True)
    stat_dict = {
        'npv': econ.present_value,
        'irr': econ.irr,
        'payout': econ.payout,
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
        self.assertAlmostEqual(self.quantile_dict['npv_mean'], 171695.33815042512, places=5)

    def test_npv_std(self):
        self.assertAlmostEqual(self.quantile_dict['npv_std'], 1283.8104749951965, places=5)

    def test_npv_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_10pct'], 170054.80835718813, places=5)

    def test_npv_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_20pct'], 170613.2642337701, places=5)

    def test_npv_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_30pct'], 171019.73564451802, places=5)

    def test_npv_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_40pct'], 171360.66215903906, places=5)

    def test_npv_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_50pct'], 171702.9924632768, places=5)

    def test_npv_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_60pct'], 172026.95216426408, places=5)

    def test_npv_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_70pct'], 172375.6955345097, places=5)

    def test_npv_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_80pct'], 172782.0038455745, places=5)

    def test_npv_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['npv_90pct'], 173335.79902466634, places=5)

    def test_irr_mean(self):
        self.assertAlmostEqual(self.quantile_dict['irr_mean'], 27.710503036071792, places=5)

    def test_irr_std(self):
        self.assertAlmostEqual(self.quantile_dict['irr_std'], 0.15755767379764843, places=5)

    def test_irr_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_10pct'], 27.50932695802674, places=5)

    def test_irr_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_20pct'], 27.577624548052114, places=5)

    def test_irr_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_30pct'], 27.627396958584267, places=5)

    def test_irr_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_40pct'], 27.669183833011676, places=5)

    def test_irr_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_50pct'], 27.711179955907173, places=5)

    def test_irr_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_60pct'], 27.750956804206695, places=5)

    def test_irr_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_70pct'], 27.79381410658703, places=5)

    def test_irr_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_80pct'], 27.8437946460462, places=5)

    def test_irr_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['irr_90pct'], 27.912002942064348, places=5)

    def test_payout_mean(self):
        self.assertAlmostEqual(self.quantile_dict['payout_mean'], 4.031346751829448, places=5)

    def test_payout_std(self):
        self.assertAlmostEqual(self.quantile_dict['payout_std'], 0.017364992655847428, places=5)

    def test_payout_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_10pct'], 4.009123409815844, places=5)

    def test_payout_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_20pct'], 4.016586165516934, places=5)

    def test_payout_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_30pct'], 4.022072860227629, places=5)

    def test_payout_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_40pct'], 4.026789942959285, places=5)

    def test_payout_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_50pct'], 4.031178217267232, places=5)

    def test_payout_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_60pct'], 4.035822063023453, places=5)

    def test_payout_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_70pct'], 4.040453751938987, places=5)

    def test_payout_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_80pct'], 4.0459849092251305, places=5)

    def test_payout_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['payout_90pct'], 4.0536002449225315, places=5)

    def test_dpi_mean(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_mean'], 0.5723177938347505, places=5)

    def test_dpi_std(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_std'], 0.004279368249983987, places=5)

    def test_dpi_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_10pct'], 0.566849361190627, places=5)

    def test_dpi_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_20pct'], 0.5687108807792337, places=5)

    def test_dpi_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_30pct'], 0.5700657854817267, places=5)

    def test_dpi_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_40pct'], 0.5712022071967968, places=5)

    def test_dpi_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_50pct'], 0.5723433082109227, places=5)

    def test_dpi_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_60pct'], 0.5734231738808802, places=5)

    def test_dpi_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_70pct'], 0.5745856517816991, places=5)

    def test_dpi_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_80pct'], 0.5759400128185818, places=5)

    def test_dpi_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['dpi_90pct'], 0.5777859967488878, places=5)

    def test_profit_mean(self):
        self.assertAlmostEqual(self.quantile_dict['profit_mean'], 2.8012241318323143, places=5)

    def test_profit_std(self):
        self.assertAlmostEqual(self.quantile_dict['profit_std'], 0.008325158923804248, places=5)

    def test_profit_10pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_10pct'], 2.7905857459381775, places=5)

    def test_profit_20pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_20pct'], 2.7942071791754275, places=5)

    def test_profit_30pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_30pct'], 2.796843034824193, places=5)

    def test_profit_40pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_40pct'], 2.7990538497926067, places=5)

    def test_profit_50pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_50pct'], 2.8012737679524307, places=5)

    def test_profit_60pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_60pct'], 2.803374557787189, places=5)

    def test_profit_70pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_70pct'], 2.8056360629216823, places=5)

    def test_profit_80pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_80pct'], 2.8082708609137224, places=5)

    def test_profit_90pct(self):
        self.assertAlmostEqual(self.quantile_dict['profit_90pct'], 2.81186207080566, places=5)


if __name__ == '__main__':
    unittest.main()
