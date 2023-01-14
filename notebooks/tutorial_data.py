""" Shortcut for loading data from the ../data folder """

import sys

# Load data set object
sys.path.append("../data")
from carriers_data import CarrierDataSet

data = CarrierDataSet()
