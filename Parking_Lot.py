import streamlit as st
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cmp

class ParkingLot:
    
    def __init__(self, map):
        self.map = map
    
    def parkingLot(self):
        
        # 서울 주차장 데이터 Streamlit 설정

        st.sidebar.title("서울 주차장 데이터")
        parking_check = st.sidebar.checkbox('주차장 표시', value=False)

        # 서울 주차장 데이터 전처리

        parking = pd.read_csv('data/Seoul_Public_Parking_Lot.csv',encoding='euc-kr')

        # 서울 주차장 데이터 folium 설정

        if parking_check:
            m1 = folium.FeatureGroup(name='주차장 데이터')
            self.map.add_child(m1)

            for i in range(len(parking)):
                lat = parking.loc[i,'위도']
                long = parking.loc[i,'경도']
                name = parking.loc[i,'주차장명']
                folium.Circle(
                            [lat, long],
                            radius = 10,
                            color = 'red',
                            tooltip = name
                            ).add_to(m1)