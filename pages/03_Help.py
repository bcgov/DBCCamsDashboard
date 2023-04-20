import streamlit as st
import numpy as np
import plotly.express as px
from PIL import Image



favicon = Image.open("frontend/images/favicon.png")
st.set_page_config(
    page_title="DriveBC Camera Dashboard - Map View",
    page_icon=favicon
)

with open("frontend/css/style.css") as stylesheet:
    st.markdown(f'<style>{stylesheet.read()}</style>', unsafe_allow_html=True)

st.title("Help")

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

st.markdown(

    """
    ## Introduction to Statistical Methods
 

    ### Mean

    The arithmetic mean is the most commonly thought of average. 

    ### Standard Deviation

    The standard deviation can be thought of as the average amount that individual data points vary from the mean

    ### Z-score

    The number of standard deviations from the mean that a given value is. 

    ### General Note

    
    The above statistical concepts do presume that the data is roughly bell curve shaped, called a Normal Distribution.
    So the visualizations below will assume a standard normal distribution. (A normal distribution where the mean is zero and the standard deviation is 1)
    
    """
)

rng = np.random.default_rng()
example = rng.standard_normal(10000)
mean = example.mean()
std = example.std()

st.plotly_chart(
    px.histogram(x=example)
)

st.markdown(

    """
    The above is our example normally distributed dataset. You can see that it follows roughly a normal distribution and that the highest part of the curve is around 0,
    and the range of values is shown to about 4.

    """

)

fig = px.histogram(x=example)
fig.add_vline(x=mean)
fig.add_vline(x=mean-std)
fig.add_vline(x=mean+std)


st.plotly_chart(

    fig
)

st.markdown(
    """
    
    """
)
