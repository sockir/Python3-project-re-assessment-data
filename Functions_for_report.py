"""This program contains the functions that are used by Fairfax_County_Assess_main.py.  Each function
extracts and formats data to be returned to the user."""

#Functions_for_report.py

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


def assessment_data_summed_zone():
    print("\nAssessment Totals and Parcel Counts by Zone\n")
    pd.set_option("max_columns", 8)
    pd.set_option("max_rows", 25)

    df_assessment_data = pd.read_csv("re_taxable_assess_short_zone.csv")
    column_names = ['ZONE', 'APRLAND', 'APRBLDG', 'APRTOT', 'PRILAND', 'PRIBLDG', 'PRITOT', 'PARID', 'ZONING_DESC']

    # reindex columns
    df_assessment_data = df_assessment_data.reindex(columns = column_names)
    df_assessment_data.set_index('ZONE', inplace=True)

    # get totals of each column
    df_assess_tot = df_assessment_data.groupby(df_assessment_data.index)['APRLAND', 'APRBLDG', 'APRTOT', 'PRITOT'].sum()
    df_assess_count = df_assessment_data.groupby(df_assessment_data.index)['APRLAND'].count()

    df_assess_tot.to_csv('re_assess_tot_by_zone.csv')
    df_assess_count.to_csv('re_assess_count_by_zone.csv')

    # merge data for report
    df_assess_totals = pd.read_csv('re_assess_tot_by_zone.csv')
    df_merged = df_assess_tot.merge(df_assess_count, on='ZONE')

    # save all data to another file
    df_merged.to_csv('re_assess_tot_by_zone_ct.csv')

    # read in to report
    df_assess = pd.read_csv('re_assess_tot_by_zone_ct.csv')

    # change column names for print out out totals

    df_assess.rename(columns=lambda x: x.replace('APRLAND_y', 'PARCEL COUNT'), inplace='True')
    df_assess.rename(columns=lambda x: x.replace('APRLAND_x', '2021 LAND'), inplace='True')
    df_assess.rename(columns=lambda x: x.replace('APR', '2021 '), inplace='True')
    df_assess.rename(columns=lambda x: x.replace('PRI', '2020 '), inplace='True')


    df_assess.set_index('ZONE', inplace = True)

    # print out
    print(df_assess)

def top_25_owners():
    print("\nThe Top 25 Real Estate Owners in Fairfax County\n")
    # import file with assessment data
    df_assessment_data = pd.read_csv("re_assess_owner_data_for_ALL.csv")

    # pull 25 largest owners
    df_top_25 = pd.read_csv('re_assess_owner_data_for_ALL.csv', index_col = 0)

    df_top_25 = (df_top_25.nlargest(25, 'APRTOT'))
    df_top_25.rename(columns=lambda x: x.replace('APRTOT', '2021_ASSESSMENT'), inplace='True')
    print(df_top_25)


def assessment_SF_city_totals():
    print("\nAssessment Totals for Single-Family Dwellings by City\n")
    df_assessment_data = pd.read_csv("re_SF_final_data.csv")

    # rename columns to indicate assessment year
    df_assessment_data.rename(columns=lambda x: x.replace('APR', '2021_'), inplace='True')
    df_assessment_data.rename(columns=lambda x: x.replace('PRI', '2020_'), inplace = 'True')

    # total assessment data for each city
    df_city_tots = df_assessment_data.groupby(['CITYNAME'])['2021_LAND', '2021_BLDG','2021_TOT', '2020_TOT'].agg('sum')

    df_city_tots['% CHANGE'] = ((df_city_tots['2021_TOT'] - df_city_tots['2020_TOT']) / df_city_tots['2021_TOT'] * 100)
    print(df_city_tots)

    # save to file
    df_city_tots.to_csv('re_SF_city_totals.csv')



def residential_parcels_tots():
    print("\nAssessment Totals for Residential Zones:\n")
    # import assessments with zoning info
    df_zones = pd.read_csv('re_taxable_zoning_totals.csv')

    # rename columns to signify the assessment year
    df_zones.rename(columns=lambda x: x.replace('APR', '2021_'), inplace='True')

    # extract only the residential zones
    df_res_zones = df_zones[df_zones['ZONING_DESC'].str.match("R-") | df_zones['ZONING_DESC'].str.match("RES")]
    df_res_zones.set_index('ZONING_DESC', inplace=True)

    print(df_res_zones)

def commercial_parcels_tots():
    print("\nCommerical Real Estate Assessments")
    # import assessment data with zoning information
    df_zones = pd.read_csv('re_taxable_zoning_totals.csv')

    # rename columns to signify the assessment year
    df_zones.rename(columns=lambda x: x.replace('APR', '2021_'), inplace='True')

    # extract only the commerical zones
    df_comm_zones = df_zones[df_zones['ZONING_DESC'].str.match("C-") | df_zones['ZONING_DESC'].str.match("COM")]
    df_comm_zones.set_index('ZONING_DESC', inplace = True)

    print(df_comm_zones)

def create_bar_chart():

    df_sales = pd.read_csv('re_res_sales_totals.csv', usecols =['YEAR', 'TOTAL(MILLIONS)'])
    df_sales.plot(kind='bar', x='YEAR', y='TOTAL(MILLIONS)', color = 'blue')
    plt.title("Residential Sales Totals by Year")
    plt.ylabel('Million Dollars')
    plt.legend()
    plt.show()

def assess_lookup_alexandria():
    df_parcel_info = pd.read_csv('re_legal_ALEXANDRIA.csv', usecols=('PARID', 'ADDRESS', 'CITYNAME', 'ACRES', 'SQFT','APRLAND','APRBLDG','APRTOT', 'LUC_DESC', 'OWNER_FULL_NAME'))
    df_parcel_info = df_parcel_info[['PARID', 'OWNER_FULL_NAME', 'ADDRESS', 'CITYNAME', 'ACRES', 'SQFT','APRLAND','APRBLDG', 'APRTOT', 'LUC_DESC']]

    df_parcel_info.rename(columns=lambda x: x.replace('APR', '2021 '), inplace='True')

    df_parcel_info.set_index('PARID', inplace = True)

    pd.set_option("max_columns", None)
    pd.set_option("max_rows", None)

    user_input = input("Please enter street name for which you want assessment data: ").upper()
    #df_parcel_filter = df_parcel_info[df_parcel_info["ADDRESS"].str.contains(user_input)]

    if df_parcel_info['ADDRESS'].str.contains(user_input).any():
        df_parcel_filter = df_parcel_info[df_parcel_info["ADDRESS"].str.contains(user_input)]
        df_parcel_filter.to_html('parcel_info.html')
        # open file in web browser
        webbrowser.open_new_tab('parcel_info.html')

    else:
        print("Invalid input, try again.")


def get_median_house_sales():
    # get median sales of houses by year

    print("The median price of a home in Fairfax County by year\n")
    df_sales_indiv = pd.read_csv('re_res_sales_since_2010.csv', usecols=['PARID', 'PRICE', 'YEAR'])
    df_sales_indiv['PRICE'] = df_sales_indiv['PRICE'].apply(np.int64)

    df_sales_med = df_sales_indiv.groupby(['YEAR'], as_index = False)['PRICE'].agg(np.median)
    print(df_sales_med)

