# frontend/streamlit_app.py

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
from streamlit_autorefresh import st_autorefresh
import datetime
import random

API_URL = "http://backend:8000"

st.title("Energy Data Visualization and Analysis")

regions_response = requests.get(f"{API_URL}/regions/")
if regions_response.status_code == 200:
    regions = regions_response.json()
else:
    st.error("Failed to fetch regions")
    st.stop()

metrics_response = requests.get(f"{API_URL}/metrics/")
if metrics_response.status_code == 200:
    metrics = metrics_response.json()
else:
    st.error("Failed to fetch metrics")
    st.stop()

st.sidebar.subheader('Data Filters')
selected_regions = st.sidebar.multiselect('Select Regions', regions, default=regions[:3])
selected_metrics = st.sidebar.multiselect('Select Metrics', metrics, default=metrics[:2])

start_date = st.sidebar.date_input('Start Date', value=datetime.date.today() - datetime.timedelta(days=7))
end_date = st.sidebar.date_input('End Date', value=datetime.date.today())

energy_data_response = requests.get(f"{API_URL}/energy_data/")
if energy_data_response.status_code == 200:
    energy_data = pd.DataFrame(energy_data_response.json())
    energy_data['date'] = pd.to_datetime(energy_data['date'])
else:
    st.error("Failed to fetch energy data")
    st.stop()

filtered_data = energy_data[
    (energy_data['region'].isin(selected_regions)) &
    (energy_data['metric'].isin(selected_metrics)) &
    (energy_data['date'].dt.date >= start_date) &
    (energy_data['date'].dt.date <= end_date)
]

st.subheader("Data Exploration")
group_by_options = ['region', 'metric', 'date']
group_by = st.selectbox('Group Data By', group_by_options)

grouped_data = filtered_data.groupby(group_by).agg({
    'value': 'sum',
    'latitude': 'mean',
    'longitude': 'mean'
}).reset_index()

st.write(f"Data Grouped by {group_by.capitalize()}")
st.dataframe(grouped_data)

st.subheader("Comparative Analysis")

pivot_data = filtered_data.pivot_table(index='date', columns='metric', values='value', aggfunc='sum')
if not pivot_data.empty:
    fig_line = px.line(pivot_data.reset_index(), x='date', y=selected_metrics)
    fig_line.update_layout(
        title='Comparative Analysis of Energy Metrics Over Time',
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Metrics',
    )
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.write("No data available for the selected filters.")

st.subheader("Regional Comparison")
regional_data = filtered_data.groupby(['region', 'metric']).agg({
    'value': 'sum',
    'latitude': 'mean',
    'longitude': 'mean'
}).reset_index()
if not regional_data.empty:
    fig_bar = px.bar(regional_data, x='region', y='value', color='metric', barmode='group')
    fig_bar.update_layout(
        title='Energy Metrics by Region',
        xaxis_title='Region',
        yaxis_title='Value',
        legend_title='Metrics',
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.write("No data available for the selected filters.")


st.subheader("Real-Time Data Monitoring")

def generate_new_data_point():
    new_data_point = {
        'date': datetime.datetime.utcnow(),
        'region': random.choice(selected_regions) if selected_regions else 'Unknown',
        'metric': random.choice(selected_metrics) if selected_metrics else 'Unknown',
        'value': random.uniform(100, 1000),
        'latitude': random.uniform(-90, 90),
        'longitude': random.uniform(-180, 180),
    }
    return new_data_point

if 'real_time_data' not in st.session_state:
    st.session_state['real_time_data'] = filtered_data.copy()

new_data_point = generate_new_data_point()
st.session_state['real_time_data'] = pd.concat(
    [st.session_state['real_time_data'], pd.DataFrame([new_data_point])],
    ignore_index=True
)

st.write("Latest Data Point:")
st.write(pd.DataFrame([new_data_point]))


recent_data = st.session_state['real_time_data'].tail(20)

recent_data['date'] = pd.to_datetime(recent_data['date'])

fig_real_time = px.scatter(
    recent_data,
    x='date',
    y='value',
    color='metric',
    symbol='metric',
    title='Real-Time Energy Data Monitoring (Last 20 Data Points)'
)

fig_real_time.update_layout(
    xaxis_title='Date',
    yaxis_title='Value',
    legend_title='Metrics',
)

st.plotly_chart(fig_real_time, use_container_width=True)

st_autorefresh(interval=5000, key='real_time_refresh')
