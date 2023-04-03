import streamlit as st
import plotly.express as px
import pydeck as pdk

from Introduction import load_data

if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

st.title("Camera API Map View")

df = st.session_state['data'].copy()
px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='status',
                        color_discrete_map={'Active': 'green', 'Stale': 'yellow', 'Delayed': 'red'},
                        zoom=5, hover_name='camID'
                        )
st.plotly_chart(fig, use_container_width=True)
