import streamlit as st
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cmp

class PopulationDensity:
    
    def __init__(self, map, json):
        self.map = map
        self.json = json
    
    def populationDensity(self):
        
        # 서울 인구밀도 데이터 Streamlit 설정

        st.sidebar.title("서울 인구밀도 데이터")
        dense_check = st.sidebar.checkbox('인구밀도 표시', value=False)

        # 서울 인구밀도 데이터 전처리

        dense = pd.read_csv('data/Seoul_Population_Density.csv', encoding='utf-8')
        dense = dense[['행정동명', '인구밀도']]

        dense['인구밀도'] = scaler.fit_transform(dense[['인구밀도']])

        # 서울 인구밀도 데이터 folium 설정

        if dense_check:
            f2 = folium.FeatureGroup(name='인구밀도 데이터')
            self.map.add_child(f2)
            
            linear = cmp.LinearColormap(
                ['yellow', 'green', 'blue'],
                vmin=min(dense['인구밀도']), vmax=max(dense['인구밀도']),
                caption='인구밀도'
                )

            population_density = folium.Choropleth(geo_data = self.json,
                                data = dense,
                                columns = ['행정동명', '인구밀도'],
                                key_on = 'feature.properties.adm_nm',
                                fill_color = 'YlGnBu',
                                fill_opacity = 0.7,
                                line_opacity = 0.3,
                                overlay = False,
                                legend_name = '인구밀집도',
                                highlight=True
                                ).geojson.add_to(f2)
                                
            linear.add_to(self.map)
            population_density.zoom_on_click = False
            population_density.add_child(folium.features.GeoJsonTooltip(['adm_nm'], labels=False))