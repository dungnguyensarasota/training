import numpy as np
# we will use this later, so import it now

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
# output_notebook()
import bokeh.sampledata

bokeh.sampledata.download()

from bokeh.sampledata.autompg import autompg as df  # run df.head() to inspect

# Take first 10 rows
df1 = df.iloc[0:11, ]
# # print(df.head())
p = figure(plot_width=400, plot_height=400)
#
# # add a square renderer with a size, color, alpha, and sizes
p.square(df1['mpg'], df1['displ'], size=df1['accel'], color="firebrick", alpha=0.6)
show(p)

# EXERCISE: Look at the AAPL data from bokeh_utils.sampledata.stocks and create a line plot using it
from bokeh.sampledata.stocks import AAPL

# AAPL.keys()
# dict_keys(['date', 'open', 'high', 'low', 'close', 'volume', 'adj_close'])
# print(AAPL)
dates = np.array(AAPL['date'], dtype=np.datetime64)  # convert date strings to real datetimes
close = np.array(AAPL['close'], dtype=np.float_)
p = figure(x_axis_type="datetime", title="AAPL Close Price", plot_height=350, plot_width=800)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.5
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Close Price'

p.line(dates, close)

show(p)
