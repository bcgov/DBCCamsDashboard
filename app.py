import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from stqdm import stqdm

TEST = False

def parse_data(data: dict) -> pd.DataFrame:
    data = {'camID': data['id'],
            'latitude': data['location']['latitude'],
            'longitude': data['location']['longitude'],
            'lastAttemptTime': data['imageStats']['lastAttempt']['time'],
            'lastAttemptResponseTime': data['imageStats']['lastAttempt']['seconds'],
            'updatePeriodMean': data['imageStats']['updatePeriodMean'],
            'updatePeriodStdDev': data['imageStats']['updatePeriodStdDev'],
            'markedStale': data['imageStats']['markedStale'],
            'markedDelayed': data['imageStats']['markedDelayed']}
    return pd.DataFrame([data])


@st.cache(suppress_st_warning=True)
def load_data() -> pd.DataFrame:
    df = pd.DataFrame()
    for i in stqdm(range(2, 1018)):
        api_url = f"http://dev-images.drivebc.ca/webcam/api/v1/webcams/{i}"
        response = requests.get(api_url)
        if response.status_code != 200:
            continue
        else:
            row = parse_data(response.json())
            df = pd.concat([df, row])

    df.reset_index(drop=True, inplace=True)
    df['status'] = 'Active'
    df.loc[df['markedStale'], 'status'] = 'Stale'
    df.loc[df['markedDelayed'], 'status'] = 'Delayed'

    df['responseTimeZScore'] = np.abs((df['lastAttemptResponseTime'] - df['updatePeriodMean'])/(df['updatePeriodStdDev'] + 1))
    return df


st.title("Camera API Dashboard")

st.markdown("""
## Introduction

This is a small proof of concept web app which shows some basic stats related to the BC Highway Cam Data
in order to assist the team with parts of their job.

## Pages

There are two pages so far not counting this introductory page

1) The Map View

    This view plots the data on a map which should allow the team to see where trouble cameras are at a glance

2) Overview Statistics

    This view shows 4 major details:
    1) How many Cameras are currently Stale
    2) How many Cameras are currently Delayed
    3) Which Cameras are currently Stale or Delayed
    4) Which Cameras are near their Stale or Delayed Threshold 

""")

if 'data' not in st.session_state:
    if not TEST:
        st.session_state['data'] = load_data()
    else:
        st.session_state['data'] = pd.read_pickle('data.pkl')
