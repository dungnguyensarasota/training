from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

def value_by_year(y, start_value, growth_rate):
    """
    :param start_value: float, example start_value = 4.15
    :param growth_rate: float, example growth_rate = 0.05
    :param y: int, year number, example y = 3
    :return: current_value: float
    """
    current_value = start_value * (1 + growth_rate) ** (y - 1)
    return current_value


def discount_by_year(y, d_rate):
    """

    :param d_rate: float, for example discount_rate = 0.1
    :param y: int, year number, example y = 7
    :return: discount: float
    """
    discount = (1 + d_rate) ** (y - 0.5)
    return discount


def IRR(cash_flow_arr, year_arr):
    """
    :param year_arr: numpy array, dtype = int
    :param cash_flow_arr: numpy array of cash flow, dtype = float
    :return: IRR: float
    """
    discount_by_year_v = np.vectorize(discount_by_year)
    #guess a rate that makes the NPV negative
    neg_npv = 100
    neg_rate_guess = 0

    while neg_npv > 0:
        d_arr = discount_by_year_v(year_arr, neg_rate_guess)
        discounted_income_arr = cash_flow_arr / d_arr
        neg_npv = discounted_income_arr.sum()
        neg_rate_guess += 0.1

    #Guess a rate that makes the NPV positive
    pos_npv = -100
    pos_rate_guess = 0

    while pos_npv < 0:
        d_arr = discount_by_year_v(year_arr, pos_rate_guess)
        discounted_income_arr = cash_flow_arr / d_arr
        pos_npv = discounted_income_arr.sum()
        pos_rate_guess -= 0.1

    #Now we have high rate and low rate
    #Execute bi-section search

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

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def compute(self):
        project_length = self.project_length
        mineral_tax = self.mineral_tax
        royalty_rate = self.royalty_rate
        investment = self.investment
        operating_cost_start = self.operating_cost_start
        opex_increase = self.opex_increase
        gas_price_start = self.gas_price_start
        gas_price_increase = self.gas_price_increase
        discount_rate = self.discount_rate
        production_arr = self.production_arr

        present_value, profitablity, irr, payout, dpi,\
            cash, cash_cum, revenue, income, cost= (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        investment_arr = np.zeros(project_length)
        investment_arr[0] = investment
        year_arr = np.arange(1, project_length + 1, 1)

        value_by_year_v = np.vectorize(value_by_year)
        gas_price_arr = value_by_year_v(year_arr, gas_price_start, gas_price_increase)
        operating_cost_arr = value_by_year_v(year_arr, operating_cost_start, opex_increase)
        gross_income_arr = gas_price_arr * production_arr
        royalty_arr = gross_income_arr * royalty_rate
        gross_income_after_royalty_arr = gross_income_arr - royalty_arr
        mineral_tax_arr = gross_income_after_royalty_arr * mineral_tax
        net_operating_income_arr = gross_income_after_royalty_arr - mineral_tax_arr - operating_cost_arr
        net_cash_flow_arr = net_operating_income_arr - investment_arr
        net_cash_flow_cum_arr = np.cumsum(net_cash_flow_arr)
        profit_year_arr = np.where(net_cash_flow_cum_arr > 0)
        profit_year = profit_year_arr[0][0]
        cash_before = net_cash_flow_cum_arr[profit_year - 1]
        cash_after = net_cash_flow_cum_arr[profit_year]
        slope, payout, r_value, p_value, std_err = linregress([cash_before, cash_after], [profit_year, profit_year + 1])

        discount_by_year_v = np.vectorize(discount_by_year)
        discount_arr = discount_by_year_v(year_arr, discount_rate)
        discounted_net_operating_income_arr = net_operating_income_arr / discount_arr
        present_value = discounted_net_operating_income_arr.sum()
        profitablity = net_operating_income_arr.sum() / investment

        irr = IRR(net_cash_flow_arr, year_arr)
        dpi = present_value / investment
        cash = net_cash_flow_arr
        cash_cum = net_cash_flow_cum_arr
        revenue = gross_income_arr
        income = net_operating_income_arr
        cost = operating_cost_arr
        return present_value, profitablity, irr, payout, dpi, cash, cash_cum, revenue, income, cost

    def plot(self):
        present_value, profitablity, irr, payout, dpi, \
        cash, cash_cum, revenue, income, cost = self.compute()
        fig, axs = plt.subplots(2, 2)
        cash_ax = axs[0,0]
        cash_ax.plot(cash)
        cash_ax.axhline(0, color='black', linewidth = 1)
        cash_ax.xaxis.set_minor_locator(MultipleLocator(1))
        cash_ax.xaxis.set_major_locator(MultipleLocator(5))
        cash_ax.set_title('Cash Flow')
        cash_cum_ax = axs[0,1]
        cash_cum_ax.plot(cash_cum, 'tab:orange')
        cash_cum_ax.axhline(0, color='black', linewidth = 1)
        cash_cum_ax.xaxis.set_minor_locator(MultipleLocator(1))
        cash_cum_ax.xaxis.set_major_locator(MultipleLocator(5))
        cash_cum_ax.set_title('Cummulative Cash Flow')
        revenue_ax = axs[1,0]
        revenue_ax.plot(revenue, 'tab:green')
        revenue_ax.xaxis.set_minor_locator(MultipleLocator(1))
        revenue_ax.xaxis.set_major_locator(MultipleLocator(5))
        revenue_ax.set_title('Revenue')
        income_ax = axs[1,1]
        income_ax.plot(income, 'tab:green')
        income_ax.xaxis.set_minor_locator(MultipleLocator(1))
        income_ax.xaxis.set_major_locator(MultipleLocator(5))
        income_ax.set_title('Net Income')
        plt.show()


if __name__ == "__main__":
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
    econ = Economics(**params)
    econ.plot()
    #present_value, profitablity, irr, payout, dpi,\
    #cash, cash_cum, revenue, income, cost = econ.compute()
    #print(present_value, profitablity, irr, payout, dpi, cash, cash_cum, revenue, income, cost)