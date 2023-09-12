import streamlit as st
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cmp

class FutsalField:
    
    def __init__(self, map):
        self.map = map
    
    def futsalField(self):

        # 서울 풋살장 데이터 Streamlit 설정

        st.sidebar.title('서울 풋살장 데이터')
        sel_opt1 = ['민간', '공공']
        sel_box1 = st.sidebar.multiselect('풋살장 종류를 골라주세요',sel_opt1)

        # 서울 풋살장 데이터 전처리

        public_futsal = pd.read_csv("data/Seoul_Public_Futsal_Field.csv")
        public_futsal['info'] = public_futsal['구장명'] + " | " + public_futsal['비고']

        private_futsal = pd.read_csv("data/Seoul_Private_Futsal_Field.csv")
        private_futsal['info'] = private_futsal['구장명'] + " | " + private_futsal['비고'] + " | " + private_futsal['교육/대관']

        # 서울 풋살장 데이터 folium 설정

        m4 = folium.FeatureGroup(name='서울 공공 풋살장')
        self.map.add_child(m4)

        m5 = folium.FeatureGroup(name='서울 민간 풋살장')
        self.map.add_child(m5)

        for i in range(len(sel_box1)):
            if sel_box1[i] == '공공':
                for i in range(len(public_futsal)):
                    lat = public_futsal.loc[i,'위도']
                    long = public_futsal.loc[i,'경도']
                    info = public_futsal.loc[i,'info']
            
                    folium.Marker(
                            [lat, long],
                            icon=folium.Icon(icon ='ball', color = 'blue'),
                            tooltip = info
                            ).add_to(m4)
            else:
                for i in range(len(private_futsal)):
                    lat = private_futsal.loc[i,'위도']
                    long = private_futsal.loc[i,'경도']
                    info = private_futsal.loc[i,'info']
            
                    folium.Marker(
                            [lat, long],
                            icon=folium.Icon(icon ='ball', color = 'red'),
                            tooltip = info
                            ).add_to(m5)