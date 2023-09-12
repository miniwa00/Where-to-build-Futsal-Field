import pandas as pd
from Barplot import Barplot
from Futsal_Field import FutsalField
from Living_Population_Avg import LivingPopulationAvg
from Parking_Lot import ParkingLot
from Population_Density import PopulationDensity
from Living_Population_Acc import LivingPopulationAcc
from Subway import Subway
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_folium import st_folium 
import folium
from folium import plugins
import json
from datetime import date
from sklearn.preprocessing import StandardScaler
import branca.colormap as cmp

# Set Seoul 'dong' json file, map of Seoul

# In the administrative division of South Korea, a "동" (dong) refers to a unit that is smaller than "읍" (eup) and "면" (myeon), 
# typically used to describe smaller areas within cities or urban areas. 
# A "dong" can encompass residential, commercial, or mixed-use areas and plays a significant role in the administrative structure of Korean cities, 
# providing various services for local residents and businesses.

jpath = 'json/seoul_geo.json'
seoul_geo = json.load(open(jpath, encoding = 'utf-8'))
seoul_map = folium.Map(
                    location = [37.5642135, 127.0016985], 
                    tiles = 'cartoDB positron', 
                    zoom_start = 10.5
                    )

# Load subway station json file
with open('json/station_coordinate.json', encoding='utf-8') as f:
    a = json.loads(f.read())
js = pd.DataFrame(a)
js = js.drop(columns = ['line', 'code'], axis=1)
js = js.rename(columns = {'lat' : '위도', 'lng' : '경도', 'name' : '지하철역'})
js = js.drop_duplicates().reset_index(drop=True)

# Set title of Streamlit demo app
st.set_page_config(page_title='Seoul Map', layout='centered')
st.title("Where to build futsal field?")
st.caption("Made by 김윤재, 신지후, 정남주, 김종민 @ BDPV(Prof. Hyeonsil Moon) Kookmin Univ.")
if st.button('새로고침'):
    st.experimental_rerun()

# -------------------------------------- MAPPING ----------------------------------------------------

# Preprocess & Mapping living population(accumulated) data
LivingPopulationAcc(seoul_map, seoul_geo).livingPopulationAcc()

# Preprocess & Mapping living population(average) data
end_time, start_time, concatenated_df = LivingPopulationAvg(seoul_map, seoul_geo).livingPopulationAvg()

# Preprocess & Mapping population density data
PopulationDensity(seoul_map, seoul_geo).populationDensity()

# Preprocess & Mapping Seoul public parking lot data
ParkingLot(seoul_map).parkingLot()

# Preprocess & Mapping subway boarding and disembarking data
end_time_sub, start_time_sub = Subway(seoul_map, js, end_time, start_time).subway()

# Preprocess & Mapping Seoul public and private futsal field data
FutsalField(seoul_map).futsalField()

# folium load 
folium.LayerControl().add_to(seoul_map)
st_folium(seoul_map, width=725)

# -------------------------------------- BARPLOT ----------------------------------------------------

# population of boarding and disembarking of subway stations by subway line Barplot
Barplot(end_time, start_time, end_time_sub, start_time_sub, concatenated_df).subwayBarplot()

# Living population of certain 'dong' Barplot
Barplot(end_time, start_time, end_time_sub, start_time_sub, concatenated_df).livingPopulationBarplot()