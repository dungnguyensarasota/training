import numpy as np
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Button
from bokeh.plotting import ColumnDataSource, figure, output_file, show, curdoc
from models.economics import Economics
from bokeh.models.widgets import DataTable, TableColumn, Div

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
    "cash":{"data":econ.cash, "name":"Cash Flow", "neg_val":True},
    "cash_cum":{"data":econ.cash_cum, "name":"Cash Cummulative", "neg_val":True},
    "revenue":{"data":econ.revenue, "name":"Revenue", "neg_val":False},
    "income":{"data":econ.income, "name":"Income", "neg_val":False},
    "cost":{"data":econ.cost, "name":"Cost", "neg_val":False}
}

for k in plot_dict.keys():
    plot_info = plot_dict[k]
    plot_data = plot_info["data"]
    plot_name = plot_info["name"]
    neg_val = plot_info["neg_val"]
    if neg_val:
        min_plot = np.min(plot_data) * 1.1
    else:
        min_plot = np.min(plot_data) * 0.9
    source = ColumnDataSource(data=dict(y=plot_data, x=range(1, project_length + 1)))
    plot_dict[k]["source"] = source

    plot = figure(plot_height=300, plot_width=300, title=plot_name,
                       tools="crosshair,pan,reset,save,wheel_zoom",
                       y_range=[min_plot, np.max(plot_data) * 1.1], x_range=[1, project_length + 1])
    plot.left[0].formatter.use_scientific = False
    plot.sizing_mode = 'scale_width'
    plot_dict[k]["plot"] = plot

plot_dict["cash"]["plot"].line('x', 'y', source=plot_dict["cash"]["source"], line_width=3, line_alpha=0.6)
plot_dict["cash_cum"]["plot"].line('x', 'y', source=plot_dict["cash_cum"]["source"], line_width=3, line_alpha=0.6)
plot_dict["revenue"]["plot"].line('x', 'y', source=plot_dict["revenue"]["source"], line_width=3, line_alpha=0.6)
plot_dict["income"]["plot"].line('x', 'y', source=plot_dict["income"]["source"], line_width=3, line_alpha=0.6)
plot_dict["cost"]["plot"].line('x', 'y', source=plot_dict["cost"]["source"], line_width=3, line_alpha=0.6)

# Attributes table

attributes = ['NPV', 'IRR', 'Payout', 'Profitability', 'DPI']
vals = [econ.present_value, econ.irr, econ.payout, econ.profitability, econ.dpi]
vals = [np.round(a,2) for a in vals]
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
    plot_dict["cost"]["data"] = econ.cost

    for k in plot_dict.keys():
        plot_info = plot_dict[k]
        plot_data = plot_info["data"]
        plot_info["source"].data = dict(y=plot_data, x=range(1, project_length + 1))

    vals = [econ.present_value, econ.irr, econ.payout, econ.profitability, econ.dpi]
    vals = [np.round(a,2) for a in vals]
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
layout = column(
    row(column(gas_slider, gas_growth_slider, opex_slider, opex_growth_slider, button), column(investment_slider,
           tax_slider, royalty_slider, discount_slider)),
    row(data_table),
    row(plot_dict["cash"]["plot"], plot_dict["cash_cum"]["plot"], plot_dict["revenue"]["plot"],
        plot_dict["income"]["plot"], plot_dict["cost"]["plot"]), style
)

# layout = column(layout, button)

curdoc().add_root(layout)

# output_file("econ.html", title="Economic Project Example")
#
# show(layout)
