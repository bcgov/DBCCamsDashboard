import streamlit as st
import plotly.express as px
import pydeck as pdk
from utils import load_data
from PIL import Image

favicon = Image.open("frontend/images/favicon.png")
st.set_page_config(
    page_title="DriveBC Camera Dashboard - Map View",
    page_icon=favicon
)

with open("frontend/css/style.css") as stylesheet:
    st.markdown(f'<style>{stylesheet.read()}</style>', unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state['version'] = "0.5.0"    
    st.session_state['data'] = load_data()


st.title("Camera API Map View")

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
<nav class="navbar">
    <div class="banner">
        <a href="https://gov.bc.ca">
            <img src="https://developer.gov.bc.ca/static/BCID_H_rgb_rev-20eebe74aef7d92e02732a18b6aa6bbb.svg" alt="Government of British Columbia" class="navbar_logo">
        </a>
    </div>
    <h2 class="navbar_title">DriveBC Camera Dashboard</h2>
</nav>
""", unsafe_allow_html=True)

px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_mapbox(st.session_state['data'], lat='Latitude', lon='Longitude', color='Status',
                        color_discrete_map={'Active': 'green', 'Stale': 'yellow', 'Delayed': 'red'},
                        zoom=5, hover_name='Camera Name', hover_data=['Caption', 'Last Attempt Time']
                        )
st.plotly_chart(fig, use_container_width=True)
