import pandas as pd
import requests
import streamlit as st


@st.cache_data(ttl=180)
def load_data() -> pd.DataFrame:
    api_url = "https://images.drivebc.ca/webcam/api/v1/webcams?fields=id,camName,caption,location,imageStats"
    response = requests.get(api_url)
    df = parse_data(response.json())

    df.reset_index(drop=True, inplace=True)
    df['status'] = 'Active'
    df.loc[df['markedStale'], 'status'] = 'Stale'
    df.loc[df['markedDelayed'], 'status'] = 'Delayed'

    df['responseTimeZScore'] = (df['lastAttemptResponseTime'] - df['updatePeriodMean']) / (df['updatePeriodStdDev'] + 1)
    df['cameraId'] = df.groupby(['latitude', 'longitude'], sort=False).ngroup() + 1
    return df


def parse_data(data: dict) -> pd.DataFrame:
    records = []
    for record in data['webcams']:
        row_data = {'camID': record['id'],
                    'camName': record['camName'],
                    'caption': record['caption'],
                    'latitude': record['location']['latitude'],
                    'longitude': record['location']['longitude'],
                    'lastAttemptTime': record['imageStats']['lastAttempt']['time'],
                    'lastAttemptResponseTime': record['imageStats']['lastAttempt']['seconds'],
                    'updatePeriodMean': record['imageStats']['updatePeriodMean'],
                    'updatePeriodStdDev': record['imageStats']['updatePeriodStdDev'],
                    'markedStale': record['imageStats']['markedStale'],
                    'markedDelayed': record['imageStats']['markedDelayed']}

        records.append(row_data)

    return pd.DataFrame.from_records(records)
