from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import scipy as sp
import numpy_financial as npf
from scipy import stats


def payout_cal(net_cash_flow_cum_arr):
    payout = None
    profit_year_arr = np.where(net_cash_flow_cum_arr > 0)
    if len(profit_year_arr[0]) > 0:
        profit_year = profit_year_arr[0][0]
        cash_before = net_cash_flow_cum_arr[profit_year - 1]
        cash_after = net_cash_flow_cum_arr[profit_year]
        slope, payout, r_value, p_value, std_err = linregress([cash_before, cash_after], [profit_year, profit_year + 1])
    return payout


def IRR(cash_flow_arr, year_arr):
    # TODO: Speed up execution
    """
    :param year_arr: numpy array, dtype = int
    :param cash_flow_arr: numpy array of cash flow, dtype = float
    :return: IRR: float
    """
    discount_by_year_v = np.vectorize(discount_by_year)

    # guess a rate that makes the NPV negative
    neg_npv = 100
    neg_rate_guess = 27.71 / 100

    while neg_npv > 0:
        d_arr = discount_by_year_v(year_arr, neg_rate_guess)
        discounted_income_arr = cash_flow_arr / d_arr
        neg_npv = discounted_income_arr.sum()
        neg_rate_guess += 0.1

    # Guess a rate that makes the NPV positive
    pos_npv = -100
    pos_rate_guess = 27.71 / 100

    while pos_npv < 0:
        d_arr = discount_by_year_v(year_arr, pos_rate_guess)
        discounted_income_arr = cash_flow_arr / d_arr
        pos_npv = discounted_income_arr.sum()
        pos_rate_guess -= 0.1

    # Now we have high rate and low rate
    # Execute bi-section search

    rate_low = pos_rate_guess
    rate_high = neg_rate_guess
    rate_guess = (rate_low + rate_high) / 2
    eps = pow(10, -10)
    diff = 100
    while abs(diff) > eps:
        d_arr = discount_by_year_v(year_arr, rate_guess)
        discounted_income_arr = cash_flow_arr / d_arr
        temp_npv = discounted_income_arr.sum()
        diff = temp_npv - 0
        if diff > 0:
            rate_low = rate_guess
        else:
            rate_high = rate_guess
        rate_guess = (rate_low + rate_high) / 2
    irr = rate_guess * 100
    return irr


class Economics:

    def __init__(self):
        self.present_value = None
        self.irr = None
        self.payout = None
        self.dpi = None
        self.profitability = None
        self.cash = None
        self.cash_cum = None
        self.revenue = None
        self.income = None
        self.cost = None
        self.sim_arr = None
        self.sim_var = None
        self.tax = None
        self.royalty = None
        self.investment = None
        self.investment_pv = None
        self.sale_pv = None
        self.opex_pv = None
        self.tax_pv = None
        self.royalty_pv = None


    def compute(self, params, runIRR):
        """
        compute_vectorize computes economics for arrays of input
        :param : a dictionary with following keys:
        production_arr: float numpy array dim = n_sce * project_length
        investment_arr: float numpy array dim = n_sce * project_length
        gas_price_arr: float numpy array dim = n_sce * project_length
        operating_cost_arr: float numpy array dim = n_sce * project_length
        discount_arr: float numpy array dim = n_sce * project_length
        mineral_tax_arr: float numpy array dim = n_sce * 1
        royalty_arr: float numpy array dim = n_sce * 1
        sim_arr: float numpy array dim = n_sce
        sim_var: string, name of the simulation variable
        :return: Update self attributes present_value, irr, payout, dpi, profitability,
        cash, cash_cum, revenue, income, cost
        """
        production_arr = params['production_arr']
        investment_arr = params['investment_arr']
        gas_price_arr = params['gas_price_arr']
        operating_cost_arr = params['operrating_cost_arr']
        discount_arr = params['discount_arr']
        mineral_tax_arr = params['mineral_tax_arr']
        royalty_arr = params['royalty_arr']
        sim_arr = params['sim_arr']
        sim_var = params['sim_var']

        gross_income_arr = gas_price_arr * production_arr
        # print(gross_income_arr)
        royalty_arr = gross_income_arr * royalty_arr
        # print(royalty_arr)
        gross_income_after_royalty_arr = gross_income_arr - royalty_arr
        mineral_tax_arr = gross_income_after_royalty_arr * mineral_tax_arr
        # print(mineral_tax_arr)
        net_operating_income_arr = gross_income_after_royalty_arr - mineral_tax_arr - operating_cost_arr
        net_cash_flow_arr = net_operating_income_arr - investment_arr
        net_cash_flow_cum_arr = np.cumsum(net_cash_flow_arr, axis=1)
        discounted_net_cash_flow_arr = net_cash_flow_arr / discount_arr
        # print(discounted_net_operating_income_arr)
        present_value = np.sum(discounted_net_cash_flow_arr, axis=1)
        dpi = present_value / investment_arr[:, 0]
        profitability = np.sum(net_operating_income_arr, axis=1) / investment_arr[:, 0]
        cash = net_cash_flow_arr
        cash_cum = net_cash_flow_cum_arr
        revenue = gross_income_arr
        income = net_operating_income_arr
        cost = operating_cost_arr
        if runIRR:
            irr = [npf.irr(x) * 100 for x in net_cash_flow_arr]
            payout = [payout_cal(x) for x in net_cash_flow_cum_arr]
            self.irr = irr
            self.payout = payout
        self.present_value = present_value
        self.dpi = dpi
        self.profitability = profitability
        self.cash = cash
        self.cash_cum = cash_cum
        self.revenue = revenue
        self.income = income
        self.cost = cost
        self.sim_arr = sim_arr
        self.sim_var = sim_var
        self.tax = mineral_tax_arr
        self.royalty = royalty_arr
        self.investment = investment_arr
        self.tax_pv = np.sum(mineral_tax_arr/discount_arr, axis=1)
        self.royalty_pv = np.sum(royalty_arr/discount_arr, axis=1)
        self.investment_pv = np.sum(investment_arr/discount_arr, axis=1)
        self.sale_pv = np.sum(gross_income_arr/discount_arr, axis=1)
        self.opex_pv = np.sum(cost/discount_arr, axis=1)

    def plot(self):
        fig, axs = plt.subplots(2, 2)
        cash_ax = axs[0, 0]
        cash_ax.plot(self.cash[0])
        cash_ax.axhline(0, color='black', linewidth=1)
        cash_ax.xaxis.set_minor_locator(MultipleLocator(1))
        cash_ax.xaxis.set_major_locator(MultipleLocator(5))
        cash_ax.set_title('Cash Flow')
        cash_cum_ax = axs[0, 1]
        cash_cum_ax.plot(self.cash_cum[0], 'tab:orange')
        cash_cum_ax.axhline(0, color='black', linewidth=1)
        cash_cum_ax.xaxis.set_minor_locator(MultipleLocator(1))
        cash_cum_ax.xaxis.set_major_locator(MultipleLocator(5))
        cash_cum_ax.set_title('Cumulative Cash Flow')
        revenue_ax = axs[1, 0]
        revenue_ax.plot(self.revenue[0], 'tab:green')
        revenue_ax.xaxis.set_minor_locator(MultipleLocator(1))
        revenue_ax.xaxis.set_major_locator(MultipleLocator(5))
        revenue_ax.set_title('Revenue')
        income_ax = axs[1, 1]
        income_ax.plot(self.income[0], 'tab:green')
        income_ax.xaxis.set_minor_locator(MultipleLocator(1))
        income_ax.xaxis.set_major_locator(MultipleLocator(5))
        income_ax.set_title('Net Income')
        plt.show()

    def plot_scenario(self, show=False):
        fig, axs = plt.subplots(2, 3)
        sim_ax = axs[0, 0]
        sim_ax.hist(self.sim_arr)
        sim_ax.set_title(self.sim_var.capitalize() + " Input")
        npv_ax = axs[0, 1]
        npv_ax.hist(self.present_value)
        npv_ax.set_title('Present Value')
        irr_ax = axs[0, 2]
        # irr_ax.hist(self.irr)
        irr_ax.set_title('IRR')
        payout_ax = axs[1, 0]
        # payout_ax.hist(self.payout)
        payout_ax.set_title('Payout')
        dpi_ax = axs[1, 1]
        dpi_ax.hist(self.dpi)
        dpi_ax.set_title('DPI')
        profit_ax = axs[1, 2]
        profit_ax.hist(self.profitability)
        profit_ax.set_title('Profitability')
        if show:
            plt.show()

    def generate_scenario(self, n_sce, sim_params, params, runIRR = False):
        """

        :param n_sce: Number of scenarios,int, n_sce = 1000,
        :param sim_params: a dictionary with key is the name of the simulated variable, ex. gas_price_start
        :param params: base parameters dictionary where the base output is computed
        :return: a dictionary with following keys:
        production_arr: float numpy array dim = n_sce * project_length
        investment_arr: float numpy array dim = n_sce * project_length
        gas_price_arr: float numpy array dim = n_sce * project_length
        operating_cost_arr: float numpy array dim = n_sce * project_length
        discount_arr: float numpy array dim = n_sce * project_length
        mineral_tax_arr: float numpy array dim = n_sce * 1
        royalty_arr: float numpy array dim = n_sce * 1
        sim_arr: float numpy array dim = n_sce
        sim_var: string, name of the simulation variable
        """
        # Default seed
        sp.random.seed(12345)

        # Get default values
        project_length = params['project_length']
        mineral_tax_arr = np.tile([params['mineral_tax']], (n_sce, 1))
        royalty_arr = np.tile([params['royalty_rate']], (n_sce, 1))
        investment_arr = np.tile([0], (n_sce, project_length))
        investment_arr[:, 0] = params['investment']
        operating_cost_start = np.tile([params['operating_cost_start']], project_length)
        opex_increase = np.tile([params['opex_increase']], project_length)
        gas_price_start = np.tile([params['gas_price_start']], project_length)
        gas_price_increase = np.tile([params['gas_price_increase']], project_length)
        discount_rate = np.tile([params['discount_rate']], project_length)
        production_arr = np.tile([params['production_arr']], (n_sce, 1))

        # Initialize default 2-dim array
        year_arr = np.arange(1, project_length + 1, 1)

        # Cost
        operating_cost_arr = np.tile(np.power(opex_increase+1, year_arr - 1), (n_sce, 1)) * operating_cost_start

        # Gas Price
        gas_price_arr = np.tile(np.power(gas_price_increase+1, year_arr - 1), (n_sce, 1)) * gas_price_start

        # discount array
        discount_arr = np.tile(np.power(discount_rate + 1, year_arr - 0.5), (n_sce, 1))
        # Processing simulation info
        sim_var = list(sim_params.keys())[0]
        sim_info = list(sim_params.values())[0]
        sim_scale = sim_info['scale']
        sim_type = sim_info['type']
        sim_loc = sim_info['loc']

        if sim_type == 'normal':
            sim_arr = np.random.normal(sim_loc, sim_scale, n_sce)
        elif sim_type == 'log':
            sim_arr = np.random.lognormal(sim_loc, sim_scale, n_sce)
            print("log normal")

        # Create 2-dim array for vectorization
        sim_arr = sim_arr.reshape(n_sce, 1)
        if sim_var == 'gas_price_start':
            gas_price_arr = np.tile(np.power(gas_price_increase+1, year_arr - 1), (n_sce, 1)) * sim_arr
        elif sim_var == 'gas_price_increase':
            gas_price_arr = np.power(np.tile(1 + sim_arr, (1, project_length)), year_arr - 1) * gas_price_start
        elif sim_var == 'operating_cost_start':
            operating_cost_arr = np.tile(np.power(opex_increase+1, year_arr - 1), (n_sce, 1)) * sim_arr
        elif sim_var == 'opex_increase':
            operating_cost_arr = np.power(np.tile(1 + sim_arr, (1, project_length)), year_arr - 1) \
                                 * operating_cost_start
        elif sim_var == 'mineral_tax':
            mineral_tax_arr = sim_arr
        elif sim_var == 'royalty_rate':
            royalty_arr = sim_arr
        elif sim_var == 'discount_rate':
            discount_arr[:, ] = np.power(1 + sim_arr, year_arr - 0.5)
        elif sim_var == 'investment':
            investment_arr[:, 0] = sim_arr.reshape(1, n_sce)
        elif sim_var == 'production_array':
            production_arr = sim_info['production_arr']

        sce_params = {
            'production_arr': production_arr,
            'investment_arr': investment_arr,
            'gas_price_arr': gas_price_arr,
            'operrating_cost_arr': operating_cost_arr,
            'discount_arr': discount_arr,
            'mineral_tax_arr': mineral_tax_arr,
            'royalty_arr': royalty_arr,
            'sim_arr': sim_arr,
            'sim_var': sim_var

        }
        self.compute(sce_params, runIRR)


if __name__ == "__main__":
    sp.random.seed(12345)
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
    # econ.compute(**params)
    # sim_params = {'operating_cost_start': {'type': 'log', 'loc': 600000, 'scale': 500}}
    n_sce = 20000
    # sim_params = {'gas_price_start':{'type': 'log', 'loc': 4.7, 'scale': 0.05}}
    sim_params = {'gas_price_start': {'type': 'log', 'loc': 4.15, 'scale': 0.5}}
    econ.generate_scenario(n_sce, sim_params, params, True)
    print(econ.present_value, econ.dpi, econ.payout, econ.irr, econ.profitability)
    # print(econ.cash)
    econ.plot_scenario(True)
