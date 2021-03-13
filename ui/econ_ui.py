import numpy as np
from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Button
from bokeh.plotting import ColumnDataSource, figure, output_file, show, curdoc
from models.economics import Economics

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

source = ColumnDataSource(data=dict(y=econ.cash, x=range(1, project_length + 1)))
# Set up plot
plot = figure(plot_height=400, plot_width=400, title="Cash Flow",
              tools="crosshair,pan,reset,save,wheel_zoom",
              y_range=[0, np.max(econ.cash)*1.1], x_range=[1, project_length + 1])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

gas_slider = Slider(start=2.0, end=10, value=4.15, step=.1, title="Gas Price")
gas_growth_slider = Slider(start=0.01, end=0.2, value=0.05, step=.01, title="Gas Price Growth Rate")
opex_slider = Slider(start=1000, end=20000, value=6000, step=500, title="Operating Cost")
opex_growth_slider = Slider(start=0.01, end=0.2, value=0.05, step=.01, title="Operating Cost Growth Rate")
investment_slider = Slider(start=100000, end=2000000, value=300000, step=20000, title="Investment")
tax_slider = Slider(start=0.01, end=0.2, value=0.025, step=.005, title="Mineral Tax Rate")
royalty_slider = Slider(start=0.05, end=0.3, value=0.15625, step=.00005, title="Royalty Rate")
discount_slider = Slider(start=0.01, end=0.3, value=0.1, step=.05, title="Discount Rate")
button = Button(label="Update Changes", button_type="success")


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
    source.data = dict(y=econ.cash, x=range(1, project_length + 1))
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


button.on_click(update_data)

layout = row(
    plot,
    column(gas_slider, gas_growth_slider, opex_slider, opex_growth_slider, investment_slider,
           tax_slider, royalty_slider, discount_slider)
)

layout = column(layout, button)

curdoc().add_root(layout)

output_file("econ.html", title="Economic Project Example")

show(layout)
