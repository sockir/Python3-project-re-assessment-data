'''
This program uses real estate assessment data produced by Fairfax County, VA to create a series of data
exports to produce assessment data in different subsets.
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
import time

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# import report functions from Functions_for_report.py
from Functions_for_report import *


def menu():

    menu_op = ''

    print()
    print("\nPlease choose an item from the menu below to retrieve the information.  Press 'q' to quit.")
    print("MENU:\n"
          "1 - Show assessment totals by all zoning\n"
          "2 - Show the Top 25 Tax Payers in Fairfax County\n"
          "3 - Show commercial assessment totals\n"
          "4 - Show residential assessment totals\n"
          "5 - Show single-family assessment totals by city\n"
          "6 - Show assessments on a particular street in Alexandra, VA\n"
          "7 - Show total amount of residential sales in Fairfax County from 2010 to 2021\n"
          "8 - Show median sale price of a home in Fairfax County from 2010 to 2021\n"
          "Q - Quit\n"
    )
    menu_op = input("Choice: ").upper().strip()
    return menu_op



def main():

    print("Welcome to Fairfax County, VA Real Estate Assessments")

    # call functions for menu options
    while True:
        choice = menu()
        if choice == "1":
            # show assessment totals by zone
            assessment_data_summed_zone()
            time.sleep(3)
            continue

        elif choice == "2":
            # show top 25 owners
            top_25_owners()
            time.sleep(3)
            continue

        elif choice == "3":
            # show commerical parcels assessment totals
            commercial_parcels_tots()
            time.sleep(3)
            continue

        elif choice == "4":
            # show residential parcels assessment totals
            residential_parcels_tots()
            time.sleep(3)
            continue

        elif choice == "5":
            # show single-family assessment totals by city
            assessment_SF_city_totals()
            time.sleep(3)
            continue

        elif choice == '6':
            # prompt user for street name and pull up assessments
            assess_lookup_alexandria()
            time.sleep(3)
            continue

        elif choice == '7':
            # print bar chart
            create_bar_chart()
            #time.sleep(3)
            continue


        elif choice == '8':
            # get the median house sale price
            get_median_house_sales()
            time.sleep(3)
            continue

        elif choice not in ("1", "2", "3", "4", "5", "6", "Q"):
            print("Invalid selection, please try again.")
            continue

        elif choice == "Q":
            break



main()