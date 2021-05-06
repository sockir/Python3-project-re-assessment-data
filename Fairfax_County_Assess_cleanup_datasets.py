'''
This program calls functions from ALL_clean_up_functions.py which clean up and transform the original datasets into
datasets that will be used by the main program.  The main program interacts with the user to display data from the data
sets.  The data is real estate assessment data provided by Fairfax County, VA.
'''
# Fairfax_County_Assess_main.py
__author__ = "Kirsten Cherry"
__copyright__ = "Kirsten Cherry, Caribou ME, 2021"
__credits__ = "data.gov and Fairfax County Real Estate Assessor's Office"
__version__ = "1.0"
__email__ = "kirsten.cherry@maine.edu"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
style.use('ggplot')
import webbrowser
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# import report functions from ALL_clean_up_functions.py
from ALL_clean_up_functions import *

def main():
    # Call all functions used to clean up the data

    data_prep_legal_step1()
    data_prep_legal_step2()
    data_prep_legal_step3()
    data_prep_legal_step4()
    prep_parcels()
    get_single_family_parcels()
    import_manage_assess_data()
    clean_up_taxable()
    import_parcel_owners()
    merge_assess_prop_owners()
    merge_SF_assess_prop_owners_parcels()
    merge_SF_assess_prop_legal_info()
    extract_city_datasets()
    prep_assess_for_zone_merge()
    merge_assess_zone_info()
    merge_assess_full_zone()
    get_totals_zoning()
    get_sales()
    get_res_parcels()
    get_housing_sales()

main()