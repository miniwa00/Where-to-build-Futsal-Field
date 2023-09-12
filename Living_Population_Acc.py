import streamlit as st
from sklearn.preprocessing import StandardScaler 
import pandas as pd
import folium
from folium import plugins

class LivingPopulationAcc:
    
    def __init__(self, map, json):
        self.map = map
        self.json = json
    
    def livingPopulationAcc(self):
        
        # 서울 생활인구 데이터 (누적) Stremalit 설정

        st.sidebar.title("서울 생활인구 데이터 (누적)")
        st.sidebar.header("시간대 조건")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_time = st.slider("시작시간", 0, 22, 0, 1, key=1)  # 0부터 22까지의 값을 선택할 수 있는 슬라이더
        with col2:
            end_time = st.slider("종료시간", 1, 23, 1, 1, key=2)  # 1부터 23까지의 값을 선택할 수 있는 슬라이더

        # 서울 생활인구 데이터 (누적) 전처리

        living = pd.read_csv('data/Seoul_Futsal_Living_Population.csv', encoding = 'cp949')
        scaler = StandardScaler()
        living['풋살인구'] = scaler.fit_transform(living[['풋살인구']])

        dfs = []
        for i in range(start_time, end_time + 1):
            temp_df = living[living['시간대'] == i]
            if not temp_df.empty:
                dfs.append(temp_df)

        f1 = folium.FeatureGroup(name='생활인구 데이터 (누적)')
        self.map.add_child(f1)

        for i in range(start_time, end_time + 1):
            fg = plugins.FeatureGroupSubGroup(f1, f'생활인구_{i}')
            self.map.add_child(fg)
            locals()['fg' + str(i)] = fg

        # 서울 생활인구 데이터 (누적) folium 설정

        for i, df_temp in enumerate(dfs):
            living_population = folium.Choropleth(geo_data=self.json,
                                    data=df_temp,
                                    columns=['행정동명', '풋살인구'],
                                    key_on='feature.properties.adm_nm',
                                    fill_color='YlOrRd',
                                    fill_opacity=0.7,
                                    line_opacity=0.3,
                                    overlay=False,
                                    show=True,
                                    legend_name='생활인구수',
                                    highlight=True
                                    ).geojson.add_to(locals()['fg' + str(i+start_time)])  # fg 변수에 추가
            
            living_population.zoom_on_click = False
            living_population.add_child(folium.features.GeoJsonTooltip(['adm_nm'], labels=False))