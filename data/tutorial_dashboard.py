""" Demo dashboard"""
import sys

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
from bokeh.palettes import Category10, Cividis
from bokeh.plotting import figure
from bokeh.transform import cumsum, transform

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
    # define the initial number of carriers to display
    initial_carriers = 10

    # read date from the demo data set
    source = ColumnDataSource(data.get_biggest_airlines_by_passengers())

    # set up tooltips
    TOOLTIPS = [
        ("Position", "@position"),
        ("Carrier", "@unique_carrier_name"),
        ("Passengers", "@passengers{(0,0)}"),
    ]

    # set up the figure
    largest_carriers_plot = figure(
        x_range=source.data["unique_carrier_name"][:initial_carriers],  # initially, display the top 10 carriers as the plot's x_range
        title=f"Top {initial_carriers} carriers by passengers (domestic routes)",  # initially, display 10 as the number of carriers in the title
        height=300,
        sizing_mode="stretch_width",
        tooltips=TOOLTIPS,
        tools="tap, hover",
        toolbar_location=None,
    )

    # add a vbar renderer
    carriers_vbar = largest_carriers_plot.vbar(
        x="unique_carrier_name",
        top="passengers",
        nonselection_alpha=0.8,
        source=source,
        legend_label="Passengers",
        width=0.6,
    )

    largest_carriers_plot.xgrid.grid_line_color = None  # remove grid lines
    largest_carriers_plot.yaxis.formatter = NumeralTickFormatter(format="0,0")  # format y axis ticks
    largest_carriers_plot.xaxis.major_label_orientation = 0.8  # rotate labels by roughly pi/4

    # Add TapTool to look up airline IATA code
    url = "https://www.iata.org/en/publications/directories/code-search/?airline.search=@unique_carrier"
    taptool = largest_carriers_plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    # Set up Slider widget
    number_slider = Slider(
        start=1,
        end=25,
        value=len(largest_carriers_plot.x_range.factors),
        title="Number of airlines to consider",
    )

    # Set up CustomJS callback
    custom_js = CustomJS(
        args={  # the args parameter is a dictionary of the variables that will be accessible in the JavaScript code
            "largest_carriers_plot": largest_carriers_plot,  # the first variable will be called "largest_carriers_plot" and links to the largest_carriers_plot Python object
            "carriers": source.data["unique_carrier_name"],  # the second variable will be called "carriers" and links to list of carrier names in the source ColumnDataSource
        },
        code="""
        largest_carriers_plot.title.text = "Top " + this.value + " carriers by passenger (domestic routes)"  // update the plot title using the slider's value (this.value)
        largest_carriers_plot.x_range.factors = carriers.slice(0,this.value)  // update the plot's x_range using data from the list of carrier names and the slider's value (this.value)
        """,
    )

    # Add callback to slider widget
    number_slider.js_on_change("value", custom_js)

    # assemble the layout
    largest_carriers_layout = column(number_slider, largest_carriers_plot)

    return largest_carriers_layout


def largest_carriers_development_plot():
    """Development of passengers, freight, and mail for the top 10 carriers"""
    plot_title = "Development of domestic passengers, freight, and mail for the top 10 carriers"

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
    """Scatter plot printing all available routes and their distance"""
    # define a list of markers to use for the scatter plot
    MARKERS = ["circle", "square", "triangle"]

    source = ColumnDataSource(data.get_distance_df())

    # set up the tooltips
    TOOLTIPS = [
        ("Distance", "@distance{(0,0)} miles"),
        ("Route", "@origin, @dest"),
        ("Amount", "$y{(0,0)}"),
    ]

    # set up the figure
    distance_plot = figure(
        title="Distance flown vs number of passengers, freight, and mail",
        height=300,
        sizing_mode="stretch_width",  # use the full width of the parent element
        tooltips=TOOLTIPS,
        output_backend="webgl",  # use webgl to speed up rendering
        tools="pan,box_zoom,reset,save",
        active_drag="box_zoom",  # enable box zoom by default
    )

    # loop through the three measurements ("passengers", "freight", "mail") and plot them
    i = 0
    for measurement in data.measurements:
        distance_plot.scatter(  # use the scatter method to use different markers
            "distance",
            measurement,
            source=source,
            legend_label=measurement.capitalize(),
            color=Category10[3][i],  # assign a different color to each measurement
            marker=MARKERS[i],  # assign a different marker to each measurement
            alpha=0.5,
        )
        i += 1

    distance_plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
    distance_plot.xaxis.axis_label = "Distance (miles)"
    distance_plot.legend.click_policy = "hide"  # set the legend click policy to hide

    return distance_plot


def departures_map():
    # read the geojson file containing the state shapes
    states_gdf = gpd.read_file("../data/us-states.geojson")
    # read the pre-processed data frame from the demo data set and join it to the state shapes
    states_gdf = states_gdf.join(data.get_states_routes_df(), on=states_gdf["Name"])
    # create the GeoJSONDataSource
    geo_source = GeoJSONDataSource(geojson=states_gdf.to_json())

    # set up the tooltips
    TOOLTIPS = [
        ("State", "@Name"),
        ("# of routes departing from here", "@origin{(0,0)}"),
    ]

    # set up the figure
    map_plot = figure(
        height=300,
        width=500,
        sizing_mode="scale_both",
        tooltips=TOOLTIPS,
        title="Number of routes with a state as its origin (all domestic carriers)",
        x_axis_location=None,  # deactivate x axis
        y_axis_location=None,  # deactivate y axis
        toolbar_location=None,  # deactivate toolbar
    )
    map_plot.grid.grid_line_color = None  # make grid lines invisible

    # set up a color mapper based on the 356-color version of Cividis
    mapper = LinearColorMapper(
        palette=Cividis[256],
        low=states_gdf["origin"].min(),
        high=states_gdf["origin"].max(),
    )

    map_plot.patches(  # use the patches method to draw the polygons of all states
        xs="xs",
        ys="ys",
        fill_color=transform(field_name="origin", transform=mapper),  # color the states by mapping the number of routes to color values from the color mapper
        source=geo_source,
        line_color="darkgrey",
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
        [departures_map(), shares_by_carrier_plot()],
    ],
    sizing_mode="stretch_width",
)

if __name__ == "__main__":
    from bokeh.plotting import show

    show(dashboard_layout)
