import streamlit as st

st.title('Camera API Overview')

df = st.session_state['data'].copy()
count_stale = df[df['status'] == 'Stale'].shape[0]
count_delayed = df[df['status'] == 'Delayed'].shape[0]

count_near_stale = df[df['responseTimeZScore'] >= 1.75].shape[0]
count_near_delayed = df[df['responseTimeZScore'] >= 4].shape[0]

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Count of Stale Cameras', value=count_stale)
        st.metric('Count of Cameras Near Stale Threshold', value=count_near_stale)

    with col2:
        st.metric('Count of Delayed Cameras', value=count_delayed)
        st.metric('Count of Cameras Near Delayed Threshold', value=count_delayed)
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Cameras in Stale or Delayed Status")
        st.dataframe(df.loc[df['status'].isin(['Stale', 'Delayed']), ['camID', 'status']].reset_index(drop=True),
                     use_container_width=True)

    with col4:
        st.subheader("Cameras Near Stale Threshold")
        st.dataframe(df.loc[df['responseTimeZScore'] >= 1.75, ['camID', 'lastAttemptResponseTime', 'updatePeriodMean',
                                                               'updatePeriodStdDev', 'responseTimeZScore']].reset_index(drop=True),
                     use_container_width=True)
