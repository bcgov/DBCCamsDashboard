import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import shutil

from stqdm import stqdm
from utils import load_data
from PIL import Image
from pathlib import Path

TEST = False

favicon = Image.open("frontend/images/favicon.png")
st.set_page_config(
    page_title="DriveBC Camera Dashboard",
    page_icon=favicon
)

with open('frontend/css/style.css') as stylesheet:
    st.markdown(f"<style>{stylesheet.read()}</style>", unsafe_allow_html=True)
        
st.title("Camera API Dashboard")

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
