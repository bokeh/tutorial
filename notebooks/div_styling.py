from bokeh.models import Div
from bokeh.plotting import show

div1 = Div(
    text="test",
    style = {"padding": "10px", "border": "1px solid red"},
    )

show(div1)
