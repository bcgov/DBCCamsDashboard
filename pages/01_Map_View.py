import streamlit as st
import plotly.express as px
import pydeck as pdk

from utils import load_data

if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

st.title("Camera API Map View")


px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_mapbox(st.session_state['data'], lat='latitude', lon='longitude', color='status',
                        color_discrete_map={'Active': 'green', 'Stale': 'yellow', 'Delayed': 'red'},
                        zoom=5, hover_name='camName', hover_data=['caption', 'responseTimeZScore']
                        )
st.plotly_chart(fig, use_container_width=True)
