import numpy as np
import numpy_financial as npf
# parameter values
project_length = 20
mineral_tax = 2.5/100
gas_price_increase = 5/100
royalities_total = 15.625/100
opex_increase = 5/100
cost_of_capital = 9/100
discount_rate = 10/100
gas_price_start = 4.15
operating_cost_start = 6000
investment = 300000
#Some input arrays
investment_arr = np.zeros(project_length)
investment_arr[0] = investment
year_arr = np.arange(1,project_length+1,1)
gas_production_arr = np.array([36500, 21900, 17520, 14016, 12614, 11353,\
                               10218, 9196, 8736, 8299, 7884, 7490, 7116,\
                               6760, 6422, 6101, 5796, 5506, 5231, 4969], dtype=float)
# this function take input of year number
# it returns the gas price of the year given
# gas price % increase by year and starting gas price
def gas_price_by_year(y):
    return gas_price_start*(1+gas_price_increase)**(y-1)
gas_price_by_year_v = np.vectorize(gas_price_by_year)
gas_price_arr = gas_price_by_year_v(year_arr)
# this function take input of year number
# it returns the operating cost of the year given
# cost % increase by year and starting operating cost
def cost_by_year(y):
    return operating_cost_start*(1+opex_increase)**(y-1)
cost_by_year_v = np.vectorize(cost_by_year)
operating_cost_arr = cost_by_year_v(year_arr)
gross_income_arr = gas_price_arr * gas_production_arr
royalty_arr = gross_income_arr * royalities_total
gross_income_after_royalty_arr = gross_income_arr - royalty_arr
mineral_tax_arr = gross_income_after_royalty_arr * mineral_tax
net_operating_income_arr = gross_income_after_royalty_arr - mineral_tax_arr - operating_cost_arr
net_cash_flow_arr = net_operating_income_arr - investment_arr
net_cash_flow_cum_arr = np.cumsum(net_cash_flow_arr)
# this function take input of year number
# it returns the discounted factor of the year given
# discount rate
def discount_by_year(y):
    return (1+discount_rate)**(y-0.5)
discount_by_year_v = np.vectorize(discount_by_year)
discount_arr = discount_by_year_v(year_arr)
discounted_net_operating_income_arr = net_operating_income_arr/discount_arr
present_value = discounted_net_operating_income_arr.sum()
profitability = net_operating_income_arr.sum()/investment
irr = npf.irr(net_cash_flow_arr)*100









