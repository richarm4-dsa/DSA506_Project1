import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

# Build the absolute path to your Data folder
data_path = SCRIPT_DIR / ".." / "Data"

# Data import
pco2_or = data_path / "ooi_oregon_pco2_hourly.csv"
print(pco2_or)
pco2_or_df = pd.read_csv(pco2_or)
pco2_or_df['time'] = pd.to_datetime(pco2_or_df['time'])

ph_or = data_path / "ooi_oregon_shelf_pH.csv"
ph_or_df = pd.read_csv(ph_or)
ph_or_df.loc[ph_or_df['pH'] < 0, 'pH'] = np.nan  # Remove anomoly; apparent sensor malfunction
ph_or_df['time'] = pd.to_datetime(ph_or_df['time'])

pco2_wa = data_path / "ooi_washington_pco2_hourly.csv"
pco2_wa_df = pd.read_csv(pco2_wa)
pco2_wa_df['time'] = pd.to_datetime(pco2_wa_df['time'])

ph_wa = data_path / "ooi_washington_shelf_pH.csv"
ph_wa_df = pd.read_csv(ph_wa)
ph_wa_df.loc[ph_wa_df['pH'] < 0, 'pH'] = np.nan  # Remove anomoly; apparent sensor malfunction
ph_wa_df['time'] = pd.to_datetime(ph_wa_df['time'])

# Streamlit and plots
st.title("📊 Ocean Acidification due to Stored pCO2 from the OOI Coastal Endurance Array")

# Oregon
sea_nominal_pH = 8.1

# Oregon
platform = 'Oregon Shelf Mooring'
min_date_or = "April 2015"  #ph_or_df['time'].min().strftime('%m-%Y')
max_date_or = "June 2026" # ph_or_df['time'].max().strftime('%m-%Y')
fig1o = px.line(ph_or_df,x='time',y='pH',
        title=f'Seawater pH, {platform}')
fig1o.add_hline(sea_nominal_pH)

fig2o = px.line(data_frame=pco2_or_df,x='time',y='partial_pressure_co2_ssw',
        title=f'Partial Pressure of CO2 (pCO2), {platform}',
        labels={'partial_pressure_co2_ssw':'Pressure (microatm)'})

pco2_or_df.set_index('time',inplace=True)
ph_or_df.set_index('time',inplace=True)

pco2_or_df = pco2_or_df.groupby(level=0).mean()
ph_or_df = ph_or_df.groupby(level=0).mean()

pco2_hourly = pco2_or_df.resample('h').mean()
pH_hourly = ph_or_df.resample('h').mean()

pco2_pH_or_synced = pd.merge(pco2_hourly,pH_hourly,left_index=True,right_index=True,how='outer')

fig3o = px.scatter(data_frame=pco2_pH_or_synced, x='partial_pressure_co2_ssw', y='pH', 
                   title=f'pH vs Partial Pressure of CO2 (pCO2) - {platform}',
                   labels={'partial_pressure_co2_ssw':'Pressure (microatm)'})
fig3o.add_hline(sea_nominal_pH)


#Washington
platform = 'Washington Shelf Mooring'
min_date_wa = "April 2015" #ph_wa_df['time'].min().strftime('%m-%Y')
max_date_wa = "September 2025" #ph_wa_df['time'].max().strftime('%m-%Y')
fig1w = px.line(ph_wa_df,x='time',y='pH',
        title=f'Seawater pH, {platform}')
fig1w.add_hline(sea_nominal_pH)

fig2w = px.line(data_frame=pco2_wa_df,x='time',y='partial_pressure_co2_ssw',
        title=f'Partial Pressure of CO2 (pCO2), {platform}',
        labels={'partial_pressure_co2_ssw':'Pressure (microatm)'})

pco2_wa_df.set_index('time',inplace=True)
ph_wa_df.set_index('time',inplace=True)

pco2_wa_df = pco2_wa_df.groupby(level=0).mean()
ph_wa_df = ph_wa_df.groupby(level=0).mean()

pco2_hourly = pco2_wa_df.resample('h').mean()
pH_hourly = ph_wa_df.resample('h').mean()

pco2_pH_wa_synced = pd.merge(pco2_hourly,pH_hourly,left_index=True,right_index=True,how='outer')

fig3w = px.scatter(data_frame=pco2_pH_wa_synced, x='partial_pressure_co2_ssw', y='pH', 
                   title=f'pH vs Partial Pressure of CO2 (pCO2) - {platform}',
                   labels={'partial_pressure_co2_ssw':'Pressure (microatm)'})
fig3w.add_hline(sea_nominal_pH)

# Layout - Using Tabs to Display Multiple Plots
tab1, tab2, tab3 = st.tabs(["Oregon Shelf Mooring", "Washington Shelf Mooring", "About"])

# Oregon
with tab1:
    st.header("Oregon Shelf Mooring")
    st.subheader(f"Deployed {min_date_or} through {max_date_or}")
    st.markdown("""
    As the amount of CO2 in the atmosphere increases, more of it is absorbed by the ocean, which becomes more acidic.
    """)
    st.plotly_chart(fig1o, use_container_width=True)
    st.plotly_chart(fig2o, use_container_width=True)
    st.plotly_chart(fig3o, use_container_width=True)

# Washington
with tab2:
    st.header("Washington Shelf Mooring")
    st.subheader(f"Deployed {min_date_wa} through {max_date_wa}")
    st.markdown("""
    As the amount of CO2 in the atmosphere increases, more of it is absorbed by the ocean, which becomes more acidic.
    """)
    st.plotly_chart(fig1w, use_container_width=True)
    st.plotly_chart(fig2w, use_container_width=True)
    st.plotly_chart(fig3w, use_container_width=True)

with tab3:
    st.header("About")
    st.markdown("""
    This dashboard visualizes sensor data from two platforms in the Ocean Observatories Inititative (OOI) Coastal Endurance Array, one of nine oceanic sensor
    arrays around the world deployed and maintained by the US National Science Foundation to collect oceanic and atmospheric data for public use.
    """)

    st.subheader("Data Sources")
    st.markdown("""
    NSF Ocean Observatories Initiative. Coastal Endurance Oregon Shelf Surface Mooring data from 2015-04-01 to 2026-06-15. Accessed on 2026-06-20.  
    https://dataexplorer.oceanobservatories.org/#ooi/array/CE/subsite/CE02SHSM
    """)
    st.markdown("""
    NSF Ocean Observatories Initiative. Coastal Endurance Washington Shelf Surface Mooring data from 2015-04-01 to 2025-09-18. Accessed on 2026-06-20.  
    https://dataexplorer.oceanobservatories.org/#ooi/array/CE/subsite/CE07SHSM
    """)
    st.markdown("""
    Wingard, C., Dever, E., & Fram, J. (2025). 10 Years of Quality Controlled Carbonate Measurements from the NSF Ocean Observatories Initiative (OOI) Coastal Endurance Array (v1.0.0) [Data set]. Zenodo.   
    https://doi.org/10.5281/zenodo.17883448
    """)


