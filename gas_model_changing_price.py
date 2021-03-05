import numpy as np
import numpy_financial as npf
def compute_economic(project_length, mineral_tax, royalty_rate,\
                     investment, operating_cost_start, opex_increase,\
                     gas_price_start, gas_price_increase, discount_rate,\
                     production_arr):
    """
    This function calculate IRR, Payout, NPV, Profitability
    :param production_arr: numpy array with length = project_length, dtype = float
    :param discount_rate: float, example discount_rate = 0.1
    :param gas_price_increase: float, growth rate of gas price, example gas_price_increase = 0.05
    :param gas_price_start: float, starting gas price, example gas_price = 4.15
    :param opex_increase: float, growth rate of operating cost, example, opex_increase = 0.05
    :param operating_cost_start: float, example operating_cost = 6000
    :param investment: float, example investment = 300000
    :param royalty_rate: float, example royalty_rate = 0.1265
    :param project_length: int, length of project (years), for example project_length = 20
    :type mineral_tax: float, example mineral_tax = 0.025
    :return:
        present_value, profitability, irr, payout: float

    """
    present_value, profitablity, irr, payout = (0, 0, 0, 0)
    investment_arr = np.zeros(project_length)
    investment_arr[0] = investment
    year_arr = np.arange(1, project_length + 1, 1)
    def value_by_year(y,start_value,growth_rate):
        """
        :param start_value: float, example start_value = 4.15
        :param growth_rate: float, example growth_rate = 0.05
        :param y: int, year number, example y = 3
        :return: current_value: float
        """
        current_value = start_value * (1 + growth_rate) ** (y - 1)
        return current_value

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

    def discount_by_year(y, d_rate):
        """

        :param d_rate: float, for example discount_rate = 0.1
        :param y: int, year number, example y = 7
        :return: discount: float
        """
        discount = (1 + d_rate) ** (y - 0.5)
        return discount

    discount_by_year_v = np.vectorize(discount_by_year)
    discount_arr = discount_by_year_v(year_arr, discount_rate)
    discounted_net_operating_income_arr = net_operating_income_arr / discount_arr
    present_value = discounted_net_operating_income_arr.sum()
    profitablity = net_operating_income_arr.sum() / investment
    def IRR(cash_flow_arr):
        """

        :param cash_flow_arr: numpy array of cash flow, dtype = float
        :return: IRR: float
        """
        neg_npv = 100
        neg_rate_guess = 0
        while neg_npv > 0:
            d_arr = discount_by_year_v(year_arr, neg_rate_guess)
            discounted_income_arr = cash_flow_arr / d_arr
            neg_npv = discounted_income_arr.sum()
            neg_rate_guess +=0.1
        pos_npv = -100
        pos_rate_guess = 0
        while pos_npv < 0:
            d_arr = discount_by_year_v(year_arr, pos_rate_guess)
            discounted_income_arr = cash_flow_arr / d_arr
            pos_npv = discounted_income_arr.sum()
            pos_rate_guess -= 0.1
        rate_low = pos_rate_guess
        rate_high = neg_rate_guess
        rate_guess = (rate_low + rate_high)/2
        eps = pow(10,-10)
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
            rate_guess = (rate_low + rate_high)/2
        irr = rate_guess * 100
        return irr

    irr = IRR(net_cash_flow_arr)
    return present_value, profitablity, irr, payout
if __name__ == "__main__":
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
    present_value, profitablity, irr, payout = compute_economic(project_length, mineral_tax, royalty_rate,\
                     investment, operating_cost_start, opex_increase,\
                     gas_price_start, gas_price_increase, discount_rate, production_arr)
    print(present_value, profitablity, irr, payout)