'''
This program uses real estate assessment datasets produced by Fairfax County, VA to create a series of data
exports to produce assessment data in different subsets.  Please note that there is a lot of data checks along the way
that print out the dataframes and their info, I have commented many of them out, but left them in for troubleshooting.
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

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
style.use('ggplot')
import webbrowser
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def data_prep_legal_step1():
    """ This step reads in the entire file and then reimports to only include the desired columns.
    This is easier than importing and then deleting unwanted columns.  """

    # read the original data from the downloaded csv file to review columns
    df_legal = pd.read_csv('FF-Legal_Data.csv')
    # print the top file rows and column names
    print(df_legal.head(50))
    print(df_legal.columns)

    # read in only the columns to be used from the original data
    df_legal = pd.read_csv('FF-Legal_Data.csv', usecols=['PARID', 'ADRNO', 'ADRADD', 'ADRDIR','ADRSTR', 'ADRSUF', 'ADRSUF2',
                                                         'CITYNAME', 'ZIP1', 'ACRES', 'SQFT', 'LEGAL1', 'TAXDIST_DESC'])
    # print the top file rows and column names for review
    print(df_legal.head(50))
    print(df_legal.columns)


    # write back to a new file to be used by program
    # print("\nWriting to a new file\n")
    df_legal.to_csv('re_legal_for_ALL.csv', index=False)

def data_prep_legal_step2():
    """Step 2 removes blank cities.  Some functions will not work with blank cells."""

    # read data in for next step
    df_legal_strip_city = pd.read_csv('re_legal_for_ALL.csv', index_col = 0)
    print('Count of parcels before removing blank cities: ', df_legal_strip_city.shape[0])

    # remove rows without cities
    df_legal_strip_city.drop(df_legal_strip_city[df_legal_strip_city['CITYNAME'].isna()].index, inplace = True)
    print('Count of parcels after removing blank cities: ', df_legal_strip_city.shape[0])

    # save results to file
    df_legal_strip_city.to_csv('re_legal_for_ALL.csv')

def data_prep_legal_step3():
    """ This step will replace null values in the data with -- for string, a 0 for ints and 0.0 for floats.
    Once replaced, it will read it back in and assign the data types as it reads in.  This will keep the number fields
    in the correct format."""
    # import file from step one and review default data types
    df_legal = pd.read_csv('re_legal_for_ALL.csv')

    # Uncomment items below for data check
    #print(df_legal.head())
    #print(df_legal.columns)
    #datatypes = df_legal.dtypes
    #print(datatypes)

    # replace na vals - it will not allow you to manipulate certain things if some cells are null
    df_legal['ADRNO'].fillna(value=0, inplace=True)
    df_legal['ADRADD'].fillna(value='--', inplace=True)
    df_legal['ADRDIR'].fillna(value='--', inplace=True)
    df_legal['ADRSTR'].fillna(value='--', inplace=True)
    df_legal['ADRSUF'].fillna(value='--', inplace=True)
    df_legal['ADRSUF2'].fillna(value='--', inplace=True)
    df_legal['ZIP1'].fillna(value=0, inplace=True)
    df_legal['ACRES'].fillna(value=0.0, inplace=True)
    df_legal['SQFT'].fillna(value=0.0, inplace=True)

    # write back to review
    df_legal.to_csv('re_legal_for_ALL.csv', index=False)

    # read back in with the desired data types
    df_legal2 = pd.read_csv('re_legal_for_ALL.csv',
                            usecols=['PARID', 'ADRNO', 'ADRADD', 'ADRDIR', 'ADRSTR', 'ADRSUF', 'ADRSUF2', 'CITYNAME',
                                     'ZIP1',
                                     'ACRES', 'SQFT', 'LEGAL1', 'TAXDIST_DESC'],
                            dtype={'PARID': object, 'ADRNO': int, 'ADRDIR': object, 'ADRADD': object, 'ADRSTR': object,
                                   'ADRSUF': object, 'ADRSUF2': object, 'CITYNAME': object, 'ZIP1': int, 'ACRES': float,
                                   'SQFT': int, 'LEGAL1': object, 'TAXDIST_DESC': object})
    # confirm changes to datatypes
    # print(df_legal2.head())
    datatypes = df_legal2.dtypes
    print(datatypes)

    # write out to file to use in next step
    df_legal2.to_csv('re_legal_for_ALL.csv', index = False)

def data_prep_legal_step4():
    """ In Step 4, the program will combine all of the street address fields into one field.  Not every street
    has each data type which will make it look odd when it is printed out on report.
    df_rep_str_addr = pd.read_csv('re_legal_for_ALL.csv') """

    # read in file
    df_rep_str_addr = pd.read_csv('re_legal_for_ALL.csv')

    # data checks - uncomment to run
    # print(df_rep_str_addr.head())
    #datatypes = df_rep_str_addr.dtypes
    #print(datatypes)

    # Concatenate the street address fields into one string called ADDRESS
    df_rep_str_addr['ADDRESS'] = df_rep_str_addr['ADRNO'].map(str) + ' ' + df_rep_str_addr['ADRADD'].str.strip('--') + ' ' + \
                                 df_rep_str_addr['ADRDIR'].str.strip('--') + ' ' + df_rep_str_addr['ADRSTR'].str.strip('--') +\
                                 ' ' + df_rep_str_addr['ADRSUF'].str.strip('--') + ' ' + df_rep_str_addr['ADRSUF2'].str.strip('--')

    # data checks - uncomment to use
    #print(df_rep_str_addr.head())
    #datatypes = df_rep_str_addr.dtypes
    #print(datatypes)

    # write back to file
    df_rep_str_addr.to_csv('re_legal_for_ALL_str.csv', index = False)

    # import new file leaving out the combined address fields
    df_legal_final = pd.read_csv('re_legal_for_ALL_str.csv',
                            usecols=['PARID', 'ADDRESS', 'CITYNAME', 'ZIP1', 'ACRES', 'SQFT', 'LEGAL1', 'TAXDIST_DESC'])

    # data checks - uncomment to use
    #print(df_legal_final.head())
    #print("\nFinal cols:", df_legal_final.columns)
    #datatypes = df_legal_final.dtypes
    #print("\nFinal datatypes:")
    #print(datatypes)

    # Write final file out
    df_legal_final.to_csv('re_legal_for_ALL_final.csv', index = False)

def prep_parcels():
    # Read in the parcel file
    df_parcels = pd.read_csv('FF-Parcels_Data.csv')

    # data checks uncomment to use
    #print(df_parcels.head(25))
    #print(df_parcels.columns)

    # Read in only the columns to be used
    df_parcels = pd.read_csv('FF-Parcels_Data.csv', usecols = ['PARID', 'LOCATION_DESC', 'LUC_DESC', 'ZONING_DESC'])

    # data checks uncomment to use
    #print(df_parcels.head())
    #print(df_parcels.columns)

    # set PARID as index
    df_parcels.set_index('PARID', inplace = True)

    # Drop any row with no data in LUC_DESC because you cannot extract single fam data with empty cells
    df_parcels.drop(df_parcels[df_parcels['LUC_DESC'].isna()].index, inplace = True)
    df_parcels.to_csv('re_parcel_for_ALL.csv')


    df_parcels = pd.read_csv('re_parcel_for_ALL.csv', index_col = 0)

    # data checks uncomment to use
    # print(df_parcels.head())
    #print(df_parcels.columns)

def get_single_family_parcels():

    df_parcels_all = pd.read_csv('re_parcel_for_ALL.csv')
    print(df_parcels_all.columns)
    print("\nInitial number of parcels: ", df_parcels_all.shape[0])

    # df_filtered = df[df['LUC_DESC'].str.contains('Single-family') & df['ZONING_DESC'].str.contains('R-')]
    df_filtered = df_parcels_all[df_parcels_all['LUC_DESC'].str.contains('Single-family')]

    # print(df_filtered.head())
    print("\nFiltered number of parcels: ", df_filtered.shape[0])
    df_filtered.to_csv('re_parcels_SF_final.csv', index = False)

def import_manage_assess_data():
    # import the assessment file
    df_assess = pd.read_csv('FF-Assessed_Values.csv')

    # data check uncomment to use
    #print(df_assess.head())

    # delete tax exempt parcels
    df_assess.drop(df_assess[df_assess['FLAG4_DESC'].str.contains('Tax Exempt')].index,
                           inplace=True)

    # data check uncomment to use
    #print(df_assess.head(25))

    df_assess.to_csv('re_taxable_assess_for_ALL.csv', index = False)

def clean_up_taxable():
    # This will fill in blank cells with data for processing
    df_assess_taxable = pd.read_csv('re_taxable_assess_for_ALL.csv')

    # data checks uncomment to use
    #print(df_assess_taxable.head())
    print("\noriginal columns:", df_assess_taxable.columns)
    print("Number of rows: ", df_assess_taxable.shape[0])

    # remove unwanted columns
    del df_assess_taxable['OBJECTID']
    del df_assess_taxable['FLAG4_DESC']
    del df_assess_taxable['TAXYR']

    print("\nNew columns: ", df_assess_taxable.columns)

    # replace null values with 0

    df_assess_taxable['PRILAND'] = df_assess_taxable['PRILAND'].fillna(0)
    df_assess_taxable['PRIBLDG'] = df_assess_taxable['PRIBLDG'].fillna(0)
    df_assess_taxable['PRITOT'] = df_assess_taxable['PRITOT'].fillna(0)

    # change float data types to int
    df_assess_taxable['PRIBLDG'] = df_assess_taxable['PRIBLDG'].apply(np.int64)
    df_assess_taxable['PRILAND'] = df_assess_taxable['PRILAND'].apply(np.int64)
    df_assess_taxable['PRITOT'] = df_assess_taxable['PRITOT'].apply(np.int64)

    # double-check changes
    print(df_assess_taxable.dtypes)

    # write back to file
    df_assess_taxable.to_csv('re_taxable_assess_for_ALL.csv', index = False)

def import_parcel_owners():

    # import the original file for review
    df_owners = pd.read_csv('FF-Property_Owner_Addresses.csv')
    print(df_owners.head())
    print(df_owners.columns)

    # import only the columns needed
    df_owners_for_use = pd.read_csv('FF-Property_Owner_Addresses.csv', usecols=['PARID', 'OWNER_FULL_NAME'])
    print(df_owners_for_use.head())
    print(df_owners_for_use.columns)

    df_owners_for_use.to_csv('re_owners_for_ALL.csv', index = False)

def merge_assess_prop_owners():
    # Begin merging files to create one dataset
    # Read in the assessment file and the owner file
    df_tax_assess = pd.read_csv('re_taxable_assess_for_ALL.csv')
    df_owners = pd.read_csv('re_owners_for_ALL.csv')

    print("Assessment data cols: ", df_tax_assess.columns)
    print("Owners data cols: ", df_owners.columns)

    # Merge the two files for the report
    df_merged = df_tax_assess.merge(df_owners, on=['PARID'])

    # Check counts to confirm no data lost & columns are as desired
    print("\nData checks on final product\n")
    print("\nMerged data:\n")
    print(df_merged.head())
    print(df_merged.columns)
    print("\nNumber of rows in parcel file: ", df_owners.shape[0])
    print("Number of rows in assessment file: ", df_tax_assess.shape[0])
    print("Number of rows in merged file: ", df_merged.shape[0])

    print("\nThe numbers of the three dataframes may not match because properties added after assessment date")
    print("are not assessed for the tax year and some properties have multiple zoning.")

    df_merged.reset_index(drop=True, inplace=True)

    # data checks uncomment to use
    #print(df_merged.head())
    #print(df_merged.columns)

    df_merged.to_csv('re_assess_owner_data_for_ALL.csv', index=False)

def merge_SF_assess_prop_owners_parcels():
    # Read in the file created above and the parcel file
    df_tax_assess = pd.read_csv('re_assess_owner_data_for_ALL.csv')
    df_parcel_zoning = pd.read_csv('re_parcels_SF_final.csv')

    print("Assessment data cols: ", df_tax_assess.columns)
    print("Parcel data cols: ", df_parcel_zoning.columns)


    # Merge the two files for the report
    df_merged = df_tax_assess.merge(df_parcel_zoning, on=['PARID'])

    # Check counts to confirm no data lost & columns are as desired
    print("\nData checks on final product-asess-prop owners\n")
    print("\nMerged data:\n")
    print(df_merged.head())
    print(df_merged.columns)
    print("\nNumber of rows in parcel file: ", df_parcel_zoning.shape[0])
    print("Number of rows in assessment file: ", df_tax_assess.shape[0])
    print("Number of rows in merged file: ", df_merged.shape[0])

    print("\nThe numbers of the three dataframes may not match because properties added after assessment date")
    print("are not assessed for the tax year and some properties have multiple zoning.\n")

    df_merged.reset_index(drop = True, inplace = True)

    # data checks uncomment to use
    #print(df_merged.head())
    #print(df_merged.columns)

    # save results to file
    df_merged.to_csv('re_assess_data_for_SF.csv', index = False)

def merge_SF_assess_prop_legal_info():
    # Read in the merged assessment & parcel data and the single-family legal data files
    df_SF_legal = pd.read_csv('re_legal_for_ALL_final.csv')
    df_SF_tax_assess = pd.read_csv('re_assess_data_for_SF.csv')


    # Merge the two files for the report
    df_merged = df_SF_legal.merge(df_SF_tax_assess, on=['PARID'])

    # Check counts to confirm no data lost & columns are as desired
    print("\nData checks on final product-assess, prop owners, legal\n")
    print("\nMerged data:\n")
    print(df_merged.head())
    print(df_merged.columns)
    print("\nNumber of rows in assessment file: ", df_SF_tax_assess.shape[0])
    print("Number of rows in assessment file: ", df_SF_legal.shape[0])
    print("Number of rows in merged file: ", df_merged.shape[0])

    print("\nThe numbers of the three dataframes may not match because properties added after assessment date")
    print("are not assessed for the tax year and some properties have multiple zoning.\n")

    df_merged.reset_index(drop = True, inplace = True)

    # data checks uncomment to use
    #print(df_merged.head())
    #print(df_merged.columns)

    # save to file
    df_merged.to_csv('re_SF_final_data.csv', index = False)

def extract_city_datasets():
    """ This step creates datasets that can be used individually for single-family real estate assessment data.
    Only one dataset will be used to demonstrate. """
    df_legal_city = pd.read_csv('re_SF_final_data.csv')

    #data check uncomment to use
    #print(df_legal_city.head())
    #print(df_legal_city.columns)

    #  discover city names
    city_names = df_legal_city['CITYNAME'].unique().tolist()
    print(city_names)

    # clean up cities that should have same name like Ft Belvoir to Fort Belvoir
    df_legal_city['CITYNAME'] = df_legal_city['CITYNAME'].replace(['FT BELVOIR'], 'FORT BELVOIR')
    df_legal_city['CITYNAME'] = df_legal_city['CITYNAME'].replace(['FAIRFAX STA'], 'FAIRFAX STATION')
    df_legal_city['CITYNAME'] = df_legal_city['CITYNAME'].replace(['FALLS CHURCH '], 'FALLS CHURCH')

    # get final set of city names
    city_names = df_legal_city['CITYNAME'].unique().tolist()
    print("City Names after replacement: ", city_names)

    # create datasets for each city
    for x in city_names:
        x_df = df_legal_city.loc[df_legal_city['CITYNAME'] == x]
        x_df.to_csv('re_legal_' + x + '.csv', index = False)

def prep_assess_for_zone_merge():
    # function will condense the zoning column to only use the information before the "(" to try and shorten for use

    df_parcels = pd.read_csv('re_parcel_for_ALL.csv')
    print(df_parcels.columns)

    # data checks uncomment to use
    #print(df_parcels.head(25))
    #print(df_parcels.columns)

    df_parcels['ZONE'] = df_parcels['ZONING_DESC'].str.split('(').str[0]

    # data checks uncomment to use
    #print(df_parcels.head(25))
    #print(df_parcels.columns)

    # save to file
    df_parcels.to_csv('re_short_zone_parcels.csv', index = False)

def merge_assess_zone_info():
    # program merges the shortened zone with taxable assessessments by parcel id
    df_tax_assess = pd.read_csv('re_taxable_assess_for_ALL.csv')
    df_parcel_zoning = pd.read_csv('re_short_zone_parcels.csv')

    df_merged = df_parcel_zoning.merge(df_tax_assess, on = 'PARID')

    # data checks uncomment to use
    #print(df_merged.head())
    #print(df_merged.columns)
    #print(df_merged.dtypes)

    # save to file
    df_merged.to_csv('re_taxable_assess_short_zone.csv', index = False)

def merge_assess_full_zone():
    # merge assessment info with full zone name for reporting
    df_tax_assess = pd.read_csv('re_taxable_assess_for_ALL.csv')
    df_parcel_zoning = pd.read_csv('re_parcel_for_ALL.csv')

    df_merged = df_parcel_zoning.merge(df_tax_assess, on = 'PARID')

    # save to file
    df_merged.to_csv('re_taxable_assess_full_zone.csv', index = False)

def get_totals_zoning():
    # totals all assessments based on zone
    # read in new file
    df_assessment_data = pd.read_csv('re_taxable_assess_full_zone.csv', index_col = 0)
    df_zoning_tots: object = df_assessment_data.groupby(['ZONING_DESC'])['APRLAND', 'APRBLDG','APRTOT'].agg('sum')

    # save to file
    df_zoning_tots.to_csv('re_taxable_zoning_totals.csv')

def get_sales():
    # extract sales date and keep only the year of the SALEDT field
    df_sales = pd.read_csv('FF-Sales_Data.csv', usecols=['OBJECTID', 'PARID', 'SALEDT', 'PRICE', 'SALEVAL_DESC'])
    df_sales['YEAR']=df_sales['SALEDT'].astype(str).str[0:4]

    # save to file with year as date
    df_sales.to_csv('re_sales_w_year.csv')

    # extract sales from 2010 to 2021
    df_sales_year = pd.read_csv('re_sales_w_year.csv', usecols=['OBJECTID', 'PARID', 'PRICE', 'SALEVAL_DESC', 'YEAR'])
    df_last_ten = df_sales_year[df_sales_year['YEAR'] >= 2010]

    # save to file
    df_last_ten.to_csv('re_sales_since_2010.csv', index = False)

    # read file in
    df_rem = pd.read_csv('re_sales_since_2010.csv')

    # filter further by only taking sales marked as Valid and verified
    df_rem2 = df_rem[df_rem['SALEVAL_DESC'] == ("Valid and verified sale")]
    df_rem2.to_csv('re_sales_valid_since_2010.csv', index = False)

def get_res_parcels():

    # extract parcels zoned as residential to be used to get residential sales
    df_parcels = pd.read_csv('FF-Parcels_Data.csv', usecols=['PARID', 'ZONING_DESC'])
    df_parcels_res = df_parcels[df_parcels['ZONING_DESC'].str.match("R-") | df_parcels['ZONING_DESC'].str.match("RES")]

    # save to file
    df_parcels_res.to_csv('re_res_parcels_for_sales.csv', index = False)

def get_housing_sales():
    # merge sales and residential parcels
    df_res_parcels = pd.read_csv('re_res_parcels_for_sales.csv')
    df_sales = pd.read_csv('re_sales_valid_since_2010.csv')

    df_merged = df_sales.merge(df_res_parcels, on='PARID')

    # save to file
    df_merged.to_csv('re_res_sales_since_2010.csv', index = False)

    # get total sales by year and shorten price to show 1.5 million
    df_sales_indiv = pd.read_csv('re_res_sales_since_2010.csv', usecols=['PARID', 'PRICE', 'YEAR'])
    df_sales_indiv['PRICE'] = df_sales_indiv['PRICE'].apply(np.int64)
    df_sales_tots = df_sales_indiv.groupby(['YEAR'], as_index = False)['PRICE'].agg('sum')
    df_sales_tots['TOTAL(MILLIONS)'] = (df_sales_tots['PRICE'] / 1000000000)

    # save to file to be used for graph in main program
    df_sales_tots.to_csv('re_res_sales_totals.csv')
