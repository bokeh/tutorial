""" Demo dashboard"""
import copy
import sys
from math import pi

import geopandas as gpd
from bokeh.layouts import column, layout
from bokeh.models import (
    ColumnDataSource,
    CustomJS,
    Div,
    GeoJSONDataSource,
    LinearColorMapper,
    NumeralTickFormatter,
    OpenURL,
    TabPanel,
    Slider,
    Tabs,
    TapTool,
)
from bokeh.palettes import Category10, Cividis11, Viridis
from bokeh.plotting import figure
from bokeh.transform import cumsum

# Load data set object
sys.path.append("../data")
from carriers_data import CarrierDataSet

data = CarrierDataSet()


def header():
    """Header with title and data source"""
    header_div = Div(
        text="""
    <h1>US domestic air carriers</h1>
    <p>Data: Bureau of Transportation Statistics, <a href="https://transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FIL&QO_fu146_anzr=Nv4%20Pn44vr45" target="_blank">Air Carriers: T-100 Domestic Market (U.S. Carriers)</a></p>
    """,
        sizing_mode="stretch_width",
        height_policy="auto",
    )

    return header_div


def biggest_carriers_plot():
    """Top N carriers by passengers"""
    initial_carriers = 10

    source = ColumnDataSource(data.get_biggest_airlines_by_passengers())

    TOOLTIPS = [
        ("Position", "@position"),
        ("Carrier", "@unique_carrier_name"),
        ("Passengers", "@passengers{(0,0)}"),
    ]

    largest_carriers_plot = figure(
        x_range=source.data["unique_carrier_name"][:initial_carriers],
        title=f"Top {initial_carriers} carriers by passengers (domestic routes)",
        height=300,
        sizing_mode="stretch_width",
        tooltips=TOOLTIPS,
    )
    carriers_vbar = largest_carriers_plot.vbar(
        x="unique_carrier_name",
        top="passengers",
        nonselection_alpha=1,
        source=source,
        legend_label="Passengers",
        width=0.6,
    )

    largest_carriers_plot.xgrid.grid_line_color = None
    largest_carriers_plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    largest_carriers_plot.xaxis.major_label_orientation = 0.8  # rotate labels by roughly pi/4

    # Add TapTool to look up airline IATA code
    largest_carriers_plot.add_tools(TapTool())
    url = "https://www.iata.org/en/publications/directories/code-search/?airline.search=@unique_carrier"
    taptool = largest_carriers_plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    # Set up MultiSelect
    number_slider = Slider(
        start=1,
        end=25,
        value=len(largest_carriers_plot.x_range.factors),
        title="Number of airlines to consider",
    )

    # Set up callback
    custom_js = CustomJS(
        args={
            "largest_carriers_plot": largest_carriers_plot,
            "carriers": source.data["unique_carrier_name"],
        },
        code="""
        largest_carriers_plot.title.text = "Top " + this.value + " carriers by passenger (domestic routes)"
        largest_carriers_plot.x_range.factors = carriers.slice(0,this.value)
        """,
    )

    number_slider.js_on_change("value", custom_js)

    largest_carriers_layout = column(number_slider, largest_carriers_plot)

    return largest_carriers_layout


def largest_carriers_development_plot():
    """Development of passengers, freight, and mail for the top 10 carriers"""
    plot_title = f"Development of domestic passengers, freight, and mail for the top 10 carriers"

    source = ColumnDataSource(data.get_monthly_values())

    TOOLTIPS = "$name: $y{(0,0)}"  # simplest way: just one line, one string

    largest_carriers_development_plot = figure(
        title=plot_title,
        x_range=source.data["month_name"],
        height=300,
        sizing_mode="stretch_both",
        tooltips=TOOLTIPS,
    )

    # Configure HoverTool
    largest_carriers_development_plot.hover.anchor = "center"
    largest_carriers_development_plot.hover.mode = "vline"

    color = 0
    for measurement in data.measurements:
        largest_carriers_development_plot.line(
            x="month_name",
            y=measurement,
            legend_label=measurement.capitalize(),
            source=source,
            width=2,
            color=Category10[3][color],
            alpha=1,
            muted_alpha=0.2,
            name=measurement,
        )
        color += 1

    largest_carriers_development_plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    largest_carriers_development_plot.xaxis.axis_label = "Month"  # TBD: x axis ticks display months, optimally month names
    largest_carriers_development_plot.legend.click_policy = "mute"

    return largest_carriers_development_plot


def distance_plot():
    MARKERS = ["circle", "square", "triangle"]

    plot_title = f"Distance flown vs number of passengers, freight, and mail"

    source = ColumnDataSource(data.get_distance_df())

    TOOLTIPS = [
        ("Distance", "@distance"),
        ("Route", "@origin, @dest"),
        ("Amount", "$y{(0,0)}"),
    ]

    # Use webgl output where available
    distance_plot = figure(
        title=plot_title,
        height=300,
        sizing_mode="stretch_width",
        tooltips=TOOLTIPS,
        output_backend="webgl",
    )

    i = 0
    for measurement in data.measurements:
        distance_plot.scatter(
            "distance",
            measurement,
            source=source,
            legend_label=measurement.capitalize(),
            color=Category10[3][i],
            marker=MARKERS[i],
            alpha=0.5,
        )
        i += 1

    distance_plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    distance_plot.xaxis.axis_label = "Distance (miles)"
    distance_plot.legend.click_policy = "hide"

    return distance_plot


def departures_arrivals_map():
    states_gdf = gpd.read_file("../data/us-states.geojson")
    states_gdf = states_gdf.join(data.get_states_routes_df(), on=states_gdf["Name"])

    MAP_SELECTIONS = ["origin", "destination"]
    selected_map = MAP_SELECTIONS[0]  # render map either based on origin or destination

    TOOLTIPS = [("State", "@Name")]
    TOOLTIPS.append(("# of routes departing from here", "@origin{(0,0)}"))

    map_plot = figure(
        height=300,
        width=500,
        sizing_mode="scale_both",
        tooltips=TOOLTIPS,
        title=f"Number of routes with a state as its origin (all domestic carriers)",
        x_axis_location=None,
        y_axis_location=None,
        toolbar_location=None,
    )

    map_plot.grid.grid_line_color = None

    mapper = LinearColorMapper(
        palette=list(Cividis11),
        low=states_gdf[selected_map].min(),
        high=states_gdf[selected_map].max(),
    )

    geo_source = GeoJSONDataSource(geojson=states_gdf.to_json())

    map_plot.patches(
        xs="xs",
        ys="ys",
        fill_color=dict(field=selected_map, transform=mapper),
        source=geo_source,
        line_color="#333344",
        line_width=1,
    )

    return map_plot


def shares_by_carrier_plot():
    """Shares of passengers, freight, and mail by carrier"""

    # Function to create annular wedge plots for passengers, freight, or mail
    def create_annular_wedge(measurement):

        TOOLTIPS = [
            ("Carrier", "@unique_carrier_name"),
            (measurement.capitalize(), f"@{measurement}{{(0,0)}}"),
        ]

        annular_plot = figure(
            height=300,
            toolbar_location=None,
            outline_line_color=None,
            sizing_mode="scale_width",
            name="region",
            x_range=(-0.66, 1),
            title=f"Top ten carriers by {measurement}",
            tooltips=TOOLTIPS,
        )

        source = ColumnDataSource(data.get_top_carriers_by_measurements(measurement))

        annular_plot.annular_wedge(
            x=0,
            y=0,
            inner_radius=0.2,
            outer_radius=0.4,
            start_angle=cumsum("angle", include_zero=True),
            end_angle=cumsum("angle"),
            line_color="white",
            fill_color="color",
            legend_field="unique_carrier_name",
            source=source,
        )

        annular_plot.axis.visible = False
        annular_plot.grid.grid_line_color = None
        annular_plot.legend.spacing = 1
        annular_plot.legend.label_text_font_size = "0.8em"

        return annular_plot

    # list of measurements to consider
    measurements = data.measurements

    # create dataframes for each category
    # dfs = create_dfs(data.get_carriers_df(), categories)

    # create tabs with annular wedges for each measurement
    tabs = []
    for measurement in measurements:
        tabs.append(TabPanel(child=create_annular_wedge(measurement), title=measurement.capitalize()))

    # display all plots as tabs
    annular_wedge_tabs = Tabs(tabs=tabs, sizing_mode="scale_both")

    return annular_wedge_tabs


dashboard_layout = layout(
    [
        [header()],
        [biggest_carriers_plot(), largest_carriers_development_plot()],
        [distance_plot()],
        [departures_arrivals_map(), shares_by_carrier_plot()],
    ],
    sizing_mode="stretch_width",
)

if __name__ == "__main__":
    from bokeh.plotting import save, show

    show(dashboard_layout)
