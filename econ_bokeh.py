import numpy as np
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Button, BasicTickFormatter, LinearAxis, Range1d
from bokeh.plotting import ColumnDataSource, figure, output_file, show, curdoc
from models.economics import Economics
from bokeh.models.widgets import DataTable, TableColumn, Div, Dropdown, Select
from bokeh.palettes import Spectral4, Spectral3
from bokeh.core.properties import value

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
econ.compute(**params)
plot_dict = {
    "cash": {"data": econ.cash, "name": "Cash Flow", "neg_val": True},
    "cash_cum": {"data": econ.cash_cum, "name": "Cash Cummulative", "neg_val": True},
    "revenue": {"data": econ.revenue, "name": "Revenue", "neg_val": False},
    "income": {"data": econ.income, "name": "Income", "neg_val": False},
    "cost": {"data": econ.cost * -1, "name": "Cost", "neg_val": True},
    "tax": {"data": econ.tax * -1, "name": "Tax", "neg_val": True},
    "royalty": {"data": econ.royalty * -1, "name": "Royalty", "neg_val": True}
}

for k in plot_dict.keys():
    plot_info = plot_dict[k]
    plot_data = plot_info["data"]
    plot_name = plot_info["name"]
    neg_val = plot_info["neg_val"]
    source = ColumnDataSource(data=dict(y=plot_data, x=range(1, project_length + 1)))
    min_val = np.min(plot_data)
    if neg_val:
        min_val = 1.1 * min_val
    else:
        min_val = 0.9 * min_val
    max_val = np.max(plot_data)
    plot_dict[k]["source"] = source
    plot_dict[k]["min"] = min_val
    plot_dict[k]["max"] = max_val * 1.1

print(plot_dict["cost"]["data"])
# Plot cash
stack_data = {
    'x': range(1, project_length + 1),
    'Cash Flow': plot_dict["cash"]["data"],
    'Cost': plot_dict["cost"]["data"],
    'Tax': plot_dict["tax"]["data"],
    'Royalty': plot_dict["royalty"]["data"],
}
stack_var = ["Cost", "Tax", "Royalty"]
cash_plot = figure(plot_height=300, plot_width=700, title="Cash Flow and Cash Cummulative".upper(),
                   tools="crosshair,pan,reset,save,wheel_zoom",
                   y_range=[plot_dict["cash_cum"]["min"], plot_dict["cash_cum"]["max"]],
                   x_range=[0, project_length + 1])
cash_plot.title.text_font_size = "15pt"
cash_plot.left[0].formatter.use_scientific = False
cash_plot.line('x', 'y', source=plot_dict["cash_cum"]["source"], line_width=3, line_alpha=0.6, color="green",
               legend="Cash Cummulative")

cash_plot.extra_y_ranges = {"y2": Range1d(start=plot_dict["cash"]["min"], end=plot_dict["cash"]["max"])}
cash_plot.add_layout(LinearAxis(y_range_name="y2"), 'right')
cash_plot.vbar(x='x', top='y', source=plot_dict["cash"]["source"], width=0.70, color="blue", y_range_name="y2",
               legend="Cash Flow")

cash_plot.right[0].formatter.use_scientific = False
cash_plot.legend.location = 'bottom_right'
cash_plot.legend.orientation = "horizontal"
# plot revenue, income and cost
min_income = plot_dict["cost"]["min"] + plot_dict["tax"]["min"] + plot_dict["royalty"]["min"]
max_income = max(plot_dict["income"]["max"], plot_dict["revenue"]["max"])
rev_plot = figure(plot_height=300, plot_width=700, title="Revenue, Income and Cost".upper(),
                  tools="crosshair,pan,reset,save,wheel_zoom",
                  y_range=[min_income * 1.1, max_income * 1.1], x_range=[0, project_length + 1])
rev_plot.title.text_font_size = "15pt"
rev_plot.left[0].formatter.use_scientific = False
rev_plot.vbar(x='x', top='y', source=plot_dict["income"]["source"], width=0.70, color="blue", legend="Income")
rev_plot.extra_y_ranges = {"y2": Range1d(start=plot_dict["cost"]["min"] + plot_dict["tax"]["min"]
                                               + plot_dict["royalty"]["min"], end=50000)}
rev_plot.add_layout(LinearAxis(y_range_name="y2"), 'right')
rev_plot.right[0].formatter.use_scientific = False
rev_plot.line('x', 'y', source=plot_dict["revenue"]["source"], line_width=3, line_alpha=0.6, color="green",
              legend="Revenue")
rev_plot.vbar_stack(stack_var, x='x', width=0.7, color=Spectral3,
                    source=stack_data,
                    # y_range_name="y2",
                    legend=[value(x) for x in stack_var]
                    )
rev_plot.legend.location = 'top_right'
rev_plot.legend.orientation = "horizontal"
# Attributes table

attributes = ['NPV', 'IRR', 'Payout', 'Profitability', 'DPI']
vals = [econ.present_value, econ.irr, econ.payout, econ.profitability, econ.dpi]
vals = [np.round(a, 2) for a in vals]
table_source = ColumnDataSource(data=dict(attributes=attributes, vals=vals))

columns = [
    TableColumn(field="attributes", title="Attributes"),
    TableColumn(field="vals", title="Values")
]
data_table = DataTable(source=table_source, columns=columns, width=400, height=180, index_position=None,
                       css_classes=["my_table"])

# Slider Control
gas_slider = Slider(start=2.0, end=6, value=4.15, step=.1, title="Gas Price")
gas_growth_slider = Slider(start=0.01, end=0.1, value=0.05, step=.01, title="Gas Price Growth Rate")
opex_slider = Slider(start=1000, end=10000, value=6000, step=500, title="Operating Cost")
opex_growth_slider = Slider(start=0.01, end=0.1, value=0.05, step=.01, title="Operating Cost Growth Rate")
investment_slider = Slider(start=200000, end=400000, value=300000, step=20000, title="Investment")
tax_slider = Slider(start=0.015, end=0.035, value=0.025, step=.005, title="Mineral Tax Rate")
royalty_slider = Slider(start=0.1, end=0.2, value=0.15625, step=.00005, title="Royalty Rate")
discount_slider = Slider(start=0.05, end=0.15, value=0.1, step=.01, title="Discount Rate")
button = Button(label="Update Changes", button_type="success", width=125)


def update_data():
    # Get the current slider values
    gas_price_start = gas_slider.value
    gas_price_increase = gas_growth_slider.value
    royalty_rate = royalty_slider.value
    opex_increase = opex_growth_slider.value
    operating_cost_start = opex_slider.value
    discount_rate = discount_slider.value
    investment = investment_slider.value
    mineral_tax = tax_slider.value

    params = {
        'project_length': project_length, 'mineral_tax': mineral_tax,
        'gas_price': gas_price_increase, 'royalty_rate': royalty_rate,
        'opex_increase': opex_increase, 'cost_of_capital': cost_of_capital,
        'discount_rate': discount_rate, 'gas_price_start': gas_price_start,
        'operating_cost_start': operating_cost_start, 'investment': investment,
        'production_arr': production_arr, 'gas_price_increase': gas_price_increase
    }

    econ = Economics()
    econ.compute(**params)
    plot_dict["cash"]["data"] = econ.cash
    plot_dict["cash_cum"]["data"] = econ.cash_cum
    plot_dict["revenue"]["data"] = econ.revenue
    plot_dict["income"]["data"] = econ.income
    plot_dict["cost"]["data"] = econ.cost * -1
    plot_dict["tax"]["data"] = econ.tax * -1
    plot_dict["royalty"]["data"] = econ.royalty * -1

    for k in plot_dict.keys():
        plot_info = plot_dict[k]
        plot_data = plot_info["data"]
        plot_info["source"].data = dict(y=plot_data, x=range(1, project_length + 1))

    stack_data["Cash Flow"] = plot_dict["cash"]["data"]
    stack_data["Cost"] = plot_dict["cost"]["data"]
    stack_data["Tax"] = plot_dict["tax"]["data"]
    stack_data["Royalty"] = plot_dict["royalty"]["data"]

    rev_plot.vbar_stack(stack_var, x='x', width=0.7, color=Spectral3,
                        source=stack_data,
                        # y_range_name="y2",
                        # legend=[value(x) for x in stack_var]
                        )
    # print(stack_data["Cost"])
    # Update table
    vals = [econ.present_value, econ.irr, econ.payout, econ.profitability, econ.dpi]
    vals = [np.round(a, 2) for a in vals]
    table_source.data = dict(attributes=attributes, vals=vals)


button.on_click(update_data)

# styles
style = Div(text="""
<style>
  .my_table{
    vertical-align: bottom; 
    font-size: 20px;
    margin-top: 200px;
    margin-lef:50px;
  }
  .my_table .bk{
    font-size: 16px;
    height:30px;  
  }
  .my_table .slick-header-column{
    font-weight:bold !important;
    vertical-align: bottom;
    font-size: 20px  
  }
  .my_table div.slick-cell{
    height: 30px  
  }
</style>

""")

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
sim_dict = {
    "Gas Price": {"loc_min": 3, "loc_max": 5, "loc_step": 0.1, "scale_min": 0.01,
                  "scale_max": 0.05, "scale_step": 0.01, "value": "gas_price_start",
                  "scale_val": 0.01, "loc_val": 4.15},
    "Gas Price Growth Rate": {
        "loc_min": 0.01, "loc_max": 0.1, "loc_step": 0.01, "scale_min": 0.001,
        "scale_max": 0.01, "scale_step": 0.001, "value": "gas_price_increase",
        "scale_val": 0.005, "loc_val": 0.05
    },
    "Operating Cost": {
        "loc_min": 1000, "loc_max": 10000, "loc_step": 1000, "scale_min": 100,
        "scale_max": 1000, "scale_step": 100, "value": "operating_cost_start",
        "scale_val": 300, "loc_val": 6000
    },
    "Operating Cost Growth": {
        "loc_min": 0.01, "loc_max": 0.1, "loc_step": 0.01, "scale_min": 0.001,
        "scale_max": 0.01, "scale_step": 0.001, "value": "opex_increase",
        "scale_val": 0.005, "loc_val": 0.05
    },
    "Investment": {
        "loc_min": 200000, "loc_max": 400000, "loc_step": 10000, "scale_min": 1000,
        "scale_max": 10000, "scale_step": 500, "value": "investment",
        "scale_val": 5000, "loc_val": 300000
    },
    "Mineral Tax": {
        "loc_min": 0.005, "loc_max": 0.05, "loc_step": 0.005, "scale_min": 0.001,
        "scale_max": 0.005, "scale_step": 0.001, "value": "mineral_tax",
        "scale_val": 0.002, "loc_val": 0.025
    },
    "Royalty Rate": {
        "loc_min": 0.05, "loc_max": 0.3, "loc_step": 0.05, "scale_min": 0.01,
        "scale_max": 0.1, "scale_step": 0.01, "value": "royalty_rate",
        "scale_val": 0.05, "loc_val": 0.16
    },
    "Discount Rate": {
        "loc_min": 0.05, "loc_max": 0.2, "loc_step": 0.05, "scale_min": 0.01,
        "scale_max": 0.1, "scale_step": 0.01, "value": "discount_rate",
        "scale_val": 0.05, "loc_val": 0.1
    }
}


# Update control
def update_slider(attr, old, new):
    active_var = dropdown.value
    for k in sim_dict.keys():
        sim_dict[k]["Slider"].visible = False
    sim_dict[active_var]["Slider"].visible = True


# Simulation
nce_slider = Slider(start=1000, end=1000000, value=10000, step=1000, title="Number of Scenario")
dropdown_menu = [x for x in sim_dict.keys()]
dropdown = Select(title="Variable:", value="Gas Price", options=dropdown_menu)
type_dropdown = Select(title="Distribution:", value="Norma;", options=["Nomal", "Log Normal"])
dropdown.on_change("value", update_slider)

for k in sim_dict.keys():
    slider_info = sim_dict[k]
    loc_slider = Slider(start=slider_info["loc_min"], end=slider_info["loc_max"], value=slider_info["loc_val"],
                        step=slider_info["loc_step"],
                        title=k + " Mean")
    scale_slider = Slider(start=slider_info["scale_min"], end=slider_info["scale_max"],
                          value=slider_info["scale_val"], step=slider_info["scale_step"],
                          title=k + " Standard Deviation")
    k_slider = row(row(loc_slider, scale_slider))
    if k == "Gas Price":
        k_slider.visible = True
    else:
        k_slider.visible = False
    sim_dict[k]["Slider"] = k_slider
    sim_dict[k]["loc_slider"] = loc_slider
    sim_dict[k]["scale_slider"] = scale_slider

sim_params = {'gas_price_start': {'type': 'normal', 'loc': 4.15, 'scale': 0.01}}
n_sce = 100000
econ.generate_scenario(n_sce, sim_params, params)

hist_dict = {
    "Input": {"data": econ.sim_arr},
    "Present Value": {"data": econ.present_value_sim},
    # "Internal Rate of Returns": {"data": econ.irr_sim},
    # "Payout": {"data": econ.payout_sim},
    "Profitability": {"data": econ.profitability_sim},
    "DPI": {"data": econ.dpi_sim},
}

for k in hist_dict.keys():
    if k == "Input":
        figure_title = "Input Distribution"
    else:
        figure_title = k + " Distribution"
    hist, edges = np.histogram(hist_dict[k]["data"], density=True, bins=50)
    fig = figure(plot_height=300, plot_width=500, title=figure_title.upper(),
                 tools="crosshair, pan,reset,save,wheel_zoom")
    fig.title.text_font_size = "15pt"
    fig.xaxis.formatter = BasicTickFormatter(use_scientific=False)
    fig.yaxis.formatter = BasicTickFormatter(use_scientific=False)
    fig.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white")
    hist_dict[k]["figure"] = fig

sim_button = Button(label="Run Simulation", button_type="success", width=125)


def run_simulation():
    n_sce = nce_slider.value
    active_var = dropdown.value
    sim_var = sim_dict[active_var]["value"]
    sim_loc = sim_dict[active_var]["loc_slider"].value
    sim_scale = sim_dict[active_var]["scale_slider"].value
    sim_type = type_dropdown.value
    if sim_type == "Normal":
        sim_type = "normal"
    else:
        sim_type = "log"
    sim_params = {sim_var: {'type': sim_type, 'loc': sim_loc, 'scale': sim_scale}}
    econ.generate_scenario(n_sce, sim_params, params)
    hist_dict["Input"]["data"] = econ.sim_arr
    hist_dict["Present Value"]["data"] = econ.present_value_sim
    # hist_dict["Internal Rate of Returns"]["data"] = econ.irr_sim
    # hist_dict["Payout"]["data"] = econ.payout_sim
    hist_dict["Profitability"]["data"] = econ.profitability_sim
    hist_dict["DPI"]["data"] = econ.dpi_sim
    for k in hist_dict.keys():
        if k == "Input":
            figure_title = "Input Distribution"
        else:
            figure_title = k + " Distribution"
        hist, edges = np.histogram(hist_dict[k]["data"], density=True, bins=50)
        fig = figure(plot_height=300, plot_width=500, title=figure_title.upper(),
                     tools="crosshair, pan,reset,save,wheel_zoom")
        fig.title.text_font_size = "15pt"
        fig.xaxis.formatter = BasicTickFormatter(use_scientific=False)
        fig.yaxis.formatter = BasicTickFormatter(use_scientific=False)
        fig.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white")
        hist_dict[k]["figure"] = fig
    hist1_row.children[0] = hist_dict["Input"]["figure"]
    hist1_row.children[1] = hist_dict["Present Value"]["figure"]
    hist3_row.children[0] = hist_dict["Profitability"]["figure"]
    hist3_row.children[1] = hist_dict["DPI"]["figure"]

sim_button.on_click(run_simulation)
hist1_row = row(hist_dict["Input"]["figure"], hist_dict["Present Value"]["figure"])
hist3_row = row(hist_dict["Profitability"]["figure"], hist_dict["DPI"]["figure"])
layout = column(
    row(column(gas_slider, gas_growth_slider, opex_slider, opex_growth_slider, button), column(investment_slider,
                                                                                               tax_slider,
                                                                                               royalty_slider,
                                                                                               discount_slider)),
    row(data_table), row(cash_plot), row(rev_plot),
    row(nce_slider), row(dropdown), row(type_dropdown),
    sim_dict["Gas Price"]["Slider"],
    sim_dict["Gas Price Growth Rate"]["Slider"],
    sim_dict["Operating Cost"]["Slider"],
    sim_dict["Operating Cost Growth"]["Slider"],
    sim_dict["Investment"]["Slider"], sim_dict["Mineral Tax"]["Slider"],
    sim_dict["Royalty Rate"]["Slider"], sim_dict["Discount Rate"]["Slider"],
    row(Div(text='<div style="background-color: clear; width: 100px; height: 25px;"></div>')),
    row(sim_button),
    hist1_row,
    # row(hist_dict["Internal Rate of Returns"]["figure"], hist_dict["Payout"]["figure"]),
    hist3_row,
    style
)

# layout = column(layout, button)

curdoc().add_root(layout)
# output_file("econ.html", title="Economic Project Example")
#
# show(layout)
