from gas_model_changing_price import compute_economic
import numpy as np

class Economics:

    def __init__(self, project_length, mineral_tax, royalty_rate,
                       investment, operating_cost_start, opex_increase,
                       gas_price_start, gas_price_increase, discount_rate,
                       production_arr):
        self.project_length = project_length
        self.mineral_tax = mineral_tax
        self.royalty_rate = royalty_rate
        self.investment = investment
        self.operating_cost_start = operating_cost_start
        self.opex_increase = opex_increase
        self.gas_price_start = gas_price_start
        self.gas_price_increase = gas_price_increase
        self.discount_rate = discount_rate
        self.production_arr = production_arr

    def compute(self):
        present_value, profitablity, irr, payout, dpi = compute_economic(self.project_length, self.mineral_tax,
                                                                    self.royalty_rate, self.investment,
                                                                    self.operating_cost_start, self.opex_increase,
                                                                    self.gas_price_start, self.gas_price_increase,
                                                                    self.discount_rate, self.production_arr)
        return present_value, profitablity, irr, payout, dpi


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
x = Economics(project_length, mineral_tax, royalty_rate,
                       investment, operating_cost_start, opex_increase,
                       gas_price_start, gas_price_increase, discount_rate,
                       production_arr)
y1, y2, y3, y4, y5 = x.compute()
print(y1, y2, y3, y4, y5)