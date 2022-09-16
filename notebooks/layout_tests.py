from bokeh.models import Div, Row, Column
from bokeh.plotting import figure, show

# div_text = """
# <div style="border: 1px solid green">test</div>
# """

div_text = "test"

div1 = Div(
    text=div_text,
    # width=900,
    # height=400,
    # sizing_mode="stretch_width",
    # width_policy="max",
    # height_policy = "auto",
    style = {"padding": "10px", "border": "1px solid red"},
    )

plot = figure(sizing_mode="stretch_width")
plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5])

# show(Row(div1, plot, sizing_mode="stretch_width"))
show(Column(div1, plot, sizing_mode='scale_width'))
# show(div1)
