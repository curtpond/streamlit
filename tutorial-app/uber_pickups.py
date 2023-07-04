import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data # This function will be cached
def load_data(nrows): # This function will be called once (unless the code is changed)
    data = pd.read_csv(DATA_URL, nrows=nrows) # read the data
    lowercase = lambda x: str(x).lower() # create a lambda function to lowercase all column names
    data.rename(lowercase, axis='columns', inplace=True) # lowercase all column names
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) # convert the date column from text to datetime
    return data

data_load_state = st.text('Loading data...') # display text while the data is loading
data = load_data(10000) # load 10,000 rows of data into the dataframe
data_load_state.text("Done! (using st.cache_data)") # display text when the data is done loading

if st.checkbox('Show raw data'): # create a checkbox to show the raw data
    st.subheader('Raw data') # display the text "Raw data" in a smaller font
    st.write(data) # display the raw data

st.subheader('Number of pickups by hour') # display the text "Number of pickups by hour" in a smaller font
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] # create a histogram of the number of pickups by hour
st.bar_chart(hist_values) # display the histogram

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17) # create a slider to filter the data by hour
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] # filter the data by the hour selected on the slider

st.subheader('Map of all pickups at %s:00' % hour_to_filter) # display the text "Map of all pickups at {hour}:00" in a smaller font
st.map(filtered_data) # display a map of the filtered data