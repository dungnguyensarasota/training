from bokeh.layouts import column
from bokeh.models import CustomJS, TextInput, Button, Paragraph
from bokeh.plotting import figure, show

inptxt = TextInput()
displaytxt = Paragraph()
button = Button()

p = figure(plot_width=400, plot_height=400,
           # Note that without setting the initial label,
           # setting it with the button will not make it
           # visible unless you interact with the plot, e.g.
           # by panning it. I've created
           # https://github.com/bokeh/bokeh/issues/10362
           # for this.
           x_axis_label='hello')
p.circle(0, 0)  # To avoid having a blank plot.


def myfunc():
    displaytxt.text = inptxt.value
    p.xaxis.axis_label = inptxt.value


button.js_on_click(CustomJS(args=dict(inptxt=inptxt,
                                      displaytxt=displaytxt,
                                      # Need `[0]` because `p.xaxis` is actually
                                      # a "splattable list" that BokehJS doesn't support.
                                      xaxis=p.xaxis[0]),
                            code="""\
                                displaytxt.text = inptxt.value;
                                xaxis.axis_label = inptxt.value;
                            """))
show(column(inptxt, displaytxt, button, p))