#Imports
import os
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta

#directory_path is the directory/path that contains the data files
directory_path = "csse_covid_19_daily_reports_us/"


#creates a "zipped" mapping between the dated data (.csv) files
#and their corresponding datetime objects
def map_filename_to_datetime():
    #directory_path = "csse_covid_19_daily_reports_us/"
    directory_contents_list = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f[-3:] == "csv"]
    directory_contents_list_sorted = sorted(directory_contents_list)
    f_list = [f[0:10] for f in directory_contents_list]
    f_datetimes_list = [datetime.strptime(f, '%m-%d-%Y') for f in f_list]
    f_datetimes_list_sorted = sorted(f_datetimes_list)
    directory_contents_f_datetimes_zipped_dict = dict(zip(directory_contents_list_sorted, f_datetimes_list_sorted))

    return directory_contents_f_datetimes_zipped_dict

#previous_nth_day_data is used to obtain the nth previous day's data.
#the function takes as parameters the zipped mapped dictionary object and the number "n". For example if 2 is
#supplied then 2 days before the latest day will be returned so if the
#latest is the 30th then the 28th will be returned.
@st.cache
def previous_nth_day_df(zipped_dict_mapping, n):
    latest_data_filename = max(zipped_dict_mapping)
    latest_data_date = zipped_dict_mapping[latest_data_filename]
    difference = timedelta(n)
    date_of_interest_date = latest_data_date - difference
    date_of_interest_filename = list(zipped_dict_mapping.keys())[list(zipped_dict_mapping.values()).index(date_of_interest_date)]

    return [str(date_of_interest_date)[:10], pd.read_csv(directory_path + date_of_interest_filename)]

#TODO: build-out alternate theme support
#Alternate Theme
#It will take a lot of work to get the alternate
#theme working as it seems that streamlit does not
#have good support for color/format changes yet
#st.markdown('<style>body{background-color: black;}</style>',unsafe_allow_html=True)
#st.markdown('<style>body{color: white;}</style>',unsafe_allow_html=True)

#maps filenames to datetimes
filename_to_datetime_map = map_filename_to_datetime()

previous_day_data_0 = previous_nth_day_df(filename_to_datetime_map, 0)
current_total_number_of_deaths = pd.Series(previous_day_data_0[1]['Deaths'].sum(), index = ['Deaths'])
current_total_number_of_deaths_string = str(current_total_number_of_deaths[0])
previous_day_data_0_top_10_deaths = previous_day_data_0[1].nlargest(10, ['Deaths'])

previous_day_data_1 = previous_nth_day_df(filename_to_datetime_map, 1)
previous_day_total_number_of_deaths_1 = pd.Series(previous_day_data_1[1]['Deaths'].sum(), index = ['Deaths'])
previous_day_total_number_of_deaths_string_1 = str(previous_day_total_number_of_deaths_1[0])
previous_day_data_1_top_10_deaths = previous_day_data_1[1].nlargest(10, ['Deaths'])

previous_day_data_2 = previous_nth_day_df(filename_to_datetime_map, 2)
previous_day_total_number_of_deaths_2 = pd.Series(previous_day_data_2[1]['Deaths'].sum(), index = ['Deaths'])
previous_day_total_number_of_deaths_string_2 = str(previous_day_total_number_of_deaths_2[0])
previous_day_data_2_top_10_deaths = previous_day_data_2[1].nlargest(10, ['Deaths'])

previous_day_data_3 = previous_nth_day_df(filename_to_datetime_map, 3)
previous_day_total_number_of_deaths_3 = pd.Series(previous_day_data_3[1]['Deaths'].sum(), index = ['Deaths'])
previous_day_total_number_of_deaths_string_3 = str(previous_day_total_number_of_deaths_3[0])
previous_day_data_3_top_10_deaths = previous_day_data_3[1].nlargest(10, ['Deaths'])

previous_day_data_4 = previous_nth_day_df(filename_to_datetime_map, 4)
previous_day_total_number_of_deaths_4 = pd.Series(previous_day_data_4[1]['Deaths'].sum(), index = ['Deaths'])
previous_day_total_number_of_deaths_string_4 = str(previous_day_total_number_of_deaths_4[0])
previous_day_data_4_top_10_deaths = previous_day_data_4[1].nlargest(10, ['Deaths'])

previous_day_data_5 = previous_nth_day_df(filename_to_datetime_map, 5)
previous_day_total_number_of_deaths_5 = pd.Series(previous_day_data_5[1]['Deaths'].sum(), index = ['Deaths'])
previous_day_total_number_of_deaths_string_5 = str(previous_day_total_number_of_deaths_5[0])
previous_day_data_5_top_10_deaths = previous_day_data_5[1].nlargest(10, ['Deaths'])

total_deaths_daily_data = {'Date': [previous_day_data_5[0], previous_day_data_4[0], previous_day_data_3[0], previous_day_data_2[0], previous_day_data_1[0], previous_day_data_0[0]],
                           'Number of Deaths': [previous_day_total_number_of_deaths_string_5, previous_day_total_number_of_deaths_string_4, previous_day_total_number_of_deaths_string_3, previous_day_total_number_of_deaths_string_2, previous_day_total_number_of_deaths_string_1, current_total_number_of_deaths_string]}

total_deaths_daily_data_dataframe = pd.DataFrame(total_deaths_daily_data, columns = ['Date', 'Number of Deaths'])

#Page Title
st.title('Coronavirus (COVID-19) Dashboard')

st.vega_lite_chart(total_deaths_daily_data_dataframe, {
    "width": 675,
    "height": 400,
    "mark": {"type": "line", "color": "blue", "Tooltip": True},
    #"selection": {
        #"grid": {
            #"type": "interval", "bind": "scales"
        #}
    #},
    'encoding': {
        "tooltip": [
            {"field": "Date", "type": "temporal"},
            {"field": "Number of Deaths", "type": "quantitative"}
        ],
        'y': {'field': 'Date', 'type': 'temporal'},
        'x': {'field': 'Number of Deaths', 'type': 'quantitative', "scale": {"domain": [255500,264000]}},
    },
})

st.header('Latest')
st.subheader(previous_day_data_0[0])
st.markdown('Total Number of Deaths: <span style="color:red">' + current_total_number_of_deaths_string + '</span>', unsafe_allow_html=True)
st.dataframe(previous_day_data_0_top_10_deaths)
st.markdown("---")

#Previous 5-Day Analysis
#Page Header "Previous 5 Days Data" 
st.header('Previous 5 Days Data')
st.markdown('Note: Lists of daily top 10 are based on the number of deaths indicated in the "Deaths" column. Number of deaths listed by source appears to be total sum of all deaths and not total number of deaths per day.')

st.header('Previous - 1 Day')
st.subheader(previous_day_data_1[0])
st.markdown('Total Number of Deaths: <span style="color:red">' + previous_day_total_number_of_deaths_string_1 + '</span>', unsafe_allow_html=True)
st.dataframe(previous_day_data_1_top_10_deaths)
st.markdown("---")

st.header('Previous - 2 Days')
st.subheader(previous_day_data_2[0])
st.markdown('Total Number of Deaths: <span style="color:red">' + previous_day_total_number_of_deaths_string_2 + '</span>', unsafe_allow_html=True)
st.dataframe(previous_day_data_2_top_10_deaths)
st.markdown("---")

st.header('Previous - 3 Days')
st.subheader(previous_day_data_3[0])
st.markdown('Total Number of Deaths: <span style="color:red">' + previous_day_total_number_of_deaths_string_3 + '</span>', unsafe_allow_html=True)
st.dataframe(previous_day_data_3_top_10_deaths)
st.markdown("---")

st.header('Previous - 4 Days')
st.subheader(previous_day_data_4[0])
st.markdown('Total Number of Deaths: <span style="color:red">' + previous_day_total_number_of_deaths_string_4 + '</span>', unsafe_allow_html=True)
st.dataframe(previous_day_data_4_top_10_deaths)
st.markdown("---")

st.header('Previous - 5 Days')
st.subheader(previous_day_data_5[0])
st.markdown('Total Number of Deaths: <span style="color:red">' + previous_day_total_number_of_deaths_string_5 + '</span>', unsafe_allow_html=True)
st.dataframe(previous_day_data_5_top_10_deaths)
st.markdown("---")
