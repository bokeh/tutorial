"""Data set operations"""

import os

import pandas as pd

# Data set source: https://transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FIL&QO_fu146_anzr=Nv4%20Pn44vr45
# Description: "This table contains domestic market data reported by U.S. air carriers, including carrier, origin, destination, and service class for enplaned passengers, freight (in lbs) and mail (in lbs) when both origin and destination airports are located within the boundaries of the United States and its territories.""
# Each row of the table represents a route that was served in the specific month (there is no information about how many times that route was served in each month).


FILENAME = "T_T100D_MARKET_US_CARRIER_ONLY_20220506_205137.zip"
input_file = os.path.join(os.path.dirname(__file__), FILENAME)


class CarrierDataSet:
    def __init__(self, file=input_file):
        self.metrics = ["passengers", "freight", "mail"]
        self.full_data_set_df = self.get_full_data_set_df(file)
        self.biggest_carriers_df = self.get_biggest_airlines_by_passengers()

    def get_full_data_set_df(self, file=input_file):
        """Full raw data set imported from CSV file"""
        get_full_data_set_df = pd.read_csv(
            file,
            compression="zip",
            usecols=range(22),
            dtype={
                "PASSENGERS": "int64",
                "FREIGHT": "int64",
                "MAIL": "int64",
                "DISTANCE": "int64",
            },
        )
        get_full_data_set_df.columns = map(str.lower, get_full_data_set_df.columns)
        return get_full_data_set_df

    def get_biggest_airlines_by_passengers(self):
        """The 25 airlines with the most passengers"""
        biggest_carriers_df = self.full_data_set_df.groupby(["unique_carrier_name", "unique_carrier"])["passengers"].sum().reset_index()
        biggest_carriers_df = biggest_carriers_df.sort_values(by="passengers", ascending=False)[:25]
        biggest_carriers_df["position"] = range(1, len(biggest_carriers_df) + 1)  # add position column for tooltip
        biggest_carriers_df.reset_index(drop=True, inplace=True)

        # Truncate long airline names to max_len
        def truncate_names(airline_name, max_len=25):
            if len(airline_name) > max_len:
                airline_name = airline_name[: max_len - 3] + "..."
            return airline_name

        biggest_carriers_df["unique_carrier_name"] = biggest_carriers_df["unique_carrier_name"].apply(truncate_names)

        return biggest_carriers_df

    def get_quarters_df(self):
        """get quarterly values for all metrics"""
        quarters_df = self.full_data_set_df.groupby(["quarter"]).agg({"distance": "sum", "passengers": "sum", "freight": "sum", "mail": "sum"})
        quarters_df.index = quarters_df.index.map(lambda x: f"Q{x}")
        return quarters_df

    def get_monthly_values(self):
        """Monthly values for all metrics"""

        import calendar

        dimensions = [metric for metric in self.metrics]  # create list of dimensions to create sums for

        df_monthly = pd.DataFrame()
        for carrier in self.biggest_carriers_df["unique_carrier_name"]:
            df = self.full_data_set_df[self.full_data_set_df["unique_carrier_name"] == carrier].groupby(["month"])[dimensions].sum()
            df_monthly = pd.concat([df, df_monthly], axis=0)

        df_monthly = df_monthly.groupby(["month"]).sum()
        df_monthly["month_name"] = df_monthly.index.to_series().apply(lambda x: calendar.month_name[x])

        return df_monthly

    def get_distance_df(self):
        """Distance for all metrics for the biggest carriers"""

        distance_df = self.full_data_set_df[self.full_data_set_df["unique_carrier_name"].isin(self.biggest_carriers_df["unique_carrier_name"])]  # Only consider top N carriers (instead of all)
        distance_df = distance_df.sort_values(by=["distance"], ascending=True).reset_index(drop=True)  # Sort by distance

        return distance_df

    def get_states_routes_df(self):
        """Domestic routes between states"""

        # Create a list of all states mentioned as either origin or destination
        states = set(list(self.full_data_set_df["origin_state_nm"]) + list(self.full_data_set_df["dest_state_nm"]))

        # Create df of arrivals and departure per state
        # This includes all departures/arrivals per state, i.e. passengers + mail + freight
        states_routes_df = pd.DataFrame(index=["origin", "dest"])
        for state in states:
            states_routes_df[state] = [
                self.full_data_set_df["origin_state_nm"].value_counts()[state],
                self.full_data_set_df["dest_state_nm"].value_counts()[state],
            ]
        states_routes_df = states_routes_df.transpose()
        states_routes_df.rename(columns={"dest": "destination"}, inplace=True)

        return states_routes_df

    def get_carriers_df(self):
        carriers_df = self.full_data_set_df.groupby("unique_carrier_name").agg({"passengers": "sum", "freight": "sum", "mail": "sum"})
        carriers_df.reset_index(inplace=True)
        return carriers_df

    def get_top_carriers_by_metrics(self, metric):
        """Top 10 carriers by metric"""

        import copy
        from math import pi
        from bokeh.palettes import Viridis

        def truncate_names(airline_name, max_len=25):
            """Truncate long airline names to max_len"""
            if len(airline_name) > max_len:
                airline_name = airline_name[: max_len - 3] + "..."
            return airline_name

        # get data for all carriers and all metrics
        top_carrier_df = self.get_carriers_df()
        # sort by target metric
        top_carrier_df = top_carrier_df.sort_values(metric, ascending=False)
        # reset index based on new sort order
        top_carrier_df.reset_index(inplace=True, drop=True)
        # remove rows that are not the current metric
        remove_columns = copy.deepcopy(self.metrics)
        remove_columns.remove(metric)
        top_carrier_df.drop(columns=remove_columns, inplace=True)
        # sum values for "others" (all carriers not in top 10)
        top_ten_by_metric = top_carrier_df.iloc[:10]["unique_carrier_name"]
        other_sum = top_carrier_df[~top_carrier_df["unique_carrier_name"].isin(top_ten_by_metric)][metric].sum()
        # create dataframe for top 10 of current metric plus others
        top_carrier_df = top_carrier_df[top_carrier_df["unique_carrier_name"].isin(top_ten_by_metric)]
        top_carrier_df.loc[len(top_carrier_df.index)] = ["Others", other_sum]

        # add column with annular wedge angles
        top_carrier_df["angle"] = top_carrier_df[metric] / top_carrier_df[metric].sum() * 2 * pi

        # generate list of 10 colors plus grey for "others"
        colors = list(Viridis[10])
        colors.append("#808080")
        top_carrier_df["color"] = colors

        # truncate long carrier names
        top_carrier_df["unique_carrier_name"] = top_carrier_df["unique_carrier_name"].apply(truncate_names, args=(25,))

        return top_carrier_df
