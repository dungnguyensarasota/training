import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider
from bokeh.plotting import ColumnDataSource, figure, output_file, show
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
x = np.linspace(0, 10, 500)
y = np.sin(x)


gas_slider = Slider(start=2.0, end=10, value=4.15, step=.1, title="Gas Price")
gas_growth_slider = Slider(start=0.01, end=0.2, value=0.05, step=.01, title="Gas Price Growth Rate")
opex_slider = Slider(start=1000, end=20000, value=6000, step=500, title="Operating Cost")
opex_growth_slider = Slider(start=0.01, end=0.2, value=0.05, step=.01, title="Operating Cost Growth Rate")
investment_slider = Slider(start=100000, end=2000000, value=300000, step=20000, title="Investment")
tax_slider = Slider(start=0.01, end=0.2, value=0.025, step=.005, title="Mineral Tax Rate")
royalty_slider = Slider(start=0.05, end=0.3, value=0.15625, step=.00005, title="Royalty Rate")
discount_slider = Slider(start=0.01, end=0.3, value=0.1, step=.05, title="Discount Rate")
# callback = CustomJS(args=dict(source=source, amp=amp_slider, freq=freq_slider, phase=phase_slider, offset=offset_slider),
#                     code="""
#     const data = source.data;
#     const A = amp.value;
#     const k = freq.value;
#     const phi = phase.value;
#     const B = offset.value;
#     const x = data['x']
#     const y = data['y']
#     for (var i = 0; i < x.length; i++) {
#         y[i] = B + A*Math.sin(k*x[i]+phi);
#     }
#     source.change.emit();
# """)

# amp_slider.js_on_change('value', callback)
# freq_slider.js_on_change('value', callback)
# phase_slider.js_on_change('value', callback)
# offset_slider.js_on_change('value', callback)

layout = row(
    # plot,
    column(gas_slider, gas_growth_slider, opex_slider, opex_growth_slider, investment_slider,
           tax_slider, royalty_slider, discount_slider),
)

output_file("econ.html", title="Economic Project Example")

show(layout)