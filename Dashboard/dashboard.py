import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np


# Data import
data_path = "../Data"

pco2_or = f"{data_path}/ooi_oregon_pco2_hourly.csv"
pco2_or_df = pd.read_csv(pco2_or)
pco2_or_df['time'] = pd.to_datetime(pco2_or_df['time'])

ph_or = f"{data_path}/ooi_oregon_shelf_pH.csv"
ph_or_df = pd.read_csv(ph_or)
ph_or_df.loc[ph_or_df['pH'] < 0, 'pH'] = np.nan  # Remove anomoly; apparent sensor malfunction
ph_or_df['time'] = pd.to_datetime(ph_or_df['time'])

pco2_wa = f"{data_path}/ooi_washington_pco2_hourly.csv"
pco2_wa_df = pd.read_csv(pco2_wa)
pco2_wa_df['time'] = pd.to_datetime(pco2_wa_df['time'])

ph_wa = f"{data_path}/ooi_washington_shelf_pH.csv"
ph_wa_df = pd.read_csv(ph_wa)
ph_wa_df['time'] = pd.to_datetime(ph_wa_df['time'])


# Streamlit and plots
st.title("📊 Ocean Observatories Initiative (OOI) - Highlights from the Coastal Endurance Array")

sea_nominal_pH = 8.1
platform = 'Oregon Shelf Mooring'
min_date = ph_or_df['time'].min().strftime('%m-%Y')
max_date = ph_or_df['time'].max().strftime('%m-%Y')
fig1 = px.line(ph_or_df,x='time',y='pH',
        title=f'Seawater pH ({min_date} - {max_date}), {platform}')
fig1.add_hline(sea_nominal_pH)


min_date = ph_or_df['time'].min().strftime('%m-%Y')
max_date = ph_or_df['time'].max().strftime('%m-%Y')
fig2 = px.line(data_frame=pco2_or_df,x='time',y='partial_pressure_co2_ssw',
        title=f'Partial Pressure of CO2 (pCO2) ({min_date} - {max_date}), {platform}',
        labels={'partial_pressure_co2_ssw':'Pressure (microatm)'})


platform = 'Washington Shelf Mooring'
min_date = ph_wa_df['time'].min().strftime('%m-%Y')
max_date = ph_wa_df['time'].max().strftime('%m-%Y')
fig3 = px.line(ph_wa_df,x='time',y='pH',
        title=f'Seawater pH ({min_date} - {max_date}), {platform}')
fig3.add_hline(sea_nominal_pH)


min_date = ph_wa_df['time'].min().strftime('%m-%Y')
max_date = ph_wa_df['time'].max().strftime('%m-%Y')
fig4 = px.line(data_frame=pco2_wa_df,x='time',y='partial_pressure_co2_ssw',
        title=f'Partial Pressure of CO2 (pCO2) ({min_date} - {max_date}), {platform}',
        labels={'partial_pressure_co2_ssw':'Pressure (microatm)'})



# Layout - Using Tabs to Display Multiple Plots
tab1, tab2 = st.tabs(["Oregon Shelf Mooring", "Washington Shelf Mooring"])

with tab1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)


with tab2:
    st.plotly_chart(fig3, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)