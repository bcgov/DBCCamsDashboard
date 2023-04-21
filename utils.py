import pandas as pd
import requests
import streamlit as st


@st.cache_data(ttl=180)
def load_data() -> pd.DataFrame:
    api_url = "https://images.drivebc.ca/webcam/api/v1/webcams?fields=id,camName,caption,location,imageStats"
    response = requests.get(api_url)
    df = parse_data(response.json())

    df.reset_index(drop=True, inplace=True)
    df['Status'] = 'Active'
    df.loc[df['Marked Stale'], 'Status'] = 'Stale'
    df.loc[df['Marked Delayed'], 'Status'] = 'Delayed'

    df['Response Time Z-Score'] = (df['Last Attempt Response Time'] - df['Update Period Mean']) / (df['Update Period Standard Deviation'] + 1)
    df['Camera Id'] = df.groupby(['Latitude', 'Longitude'], sort=False).ngroup() + 1
    return df


def parse_data(data: dict) -> pd.DataFrame:
    records = []
    for record in data['webcams']:
        row_data = {'Camera View ID': record['id'],
                    'Camera Name': record['camName'],
                    'Caption': record['caption'],
                    'Latitude': record['location']['latitude'],
                    'Longitude': record['location']['longitude'],
                    'Last Attempt Time': record['imageStats']['lastAttempt']['time'],
                    'Last Attempt Response Time': record['imageStats']['lastAttempt']['seconds'],
                    'Update Period Mean': record['imageStats']['updatePeriodMean'],
                    'Update Period Standard Deviation': record['imageStats']['updatePeriodStdDev'],
                    'Marked Stale': record['imageStats']['markedStale'],
                    'Marked Delayed': record['imageStats']['markedDelayed']}

        records.append(row_data)

    return pd.DataFrame.from_records(records)
