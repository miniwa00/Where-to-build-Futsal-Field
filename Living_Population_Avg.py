import streamlit as st
from sklearn.preprocessing import StandardScaler 
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cmp

class LivingPopulationAvg:
    
    def __init__(self, map, json):
        self.map = map
        self.json = json
    
    def livingPopulationAvg(self):
        
        # 서울 생활인구 데이터 (평균) Streamlit 설정

        st.sidebar.title("서울 생활인구 데이터 (평균)")
        st.sidebar.header("시간대 조건")
        col3, col4 = st.sidebar.columns(2)
        with col3:
            start_time = st.slider("시작시간", 0, 22, 0, 1, key=3)  # 0부터 22까지의 값을 선택할 수 있는 슬라이더

        with col4:
            end_time = st.slider("종료시간", 1, 23, 1, 1, key=4)  # 1부터 23까지의 값을 선택할 수 있는 슬라이더

        # 서울 생활인구 데이터 (평균) 전처리

        living = pd.read_csv('data/Seoul_Futsal_Living_Population.csv', encoding = 'cp949')

        dfs = []
        for i in range(start_time, end_time + 1):
            temp_df = living[living['시간대'] == i]
            if not temp_df.empty:
                dfs.append(temp_df)

        f3 = folium.FeatureGroup(name='생활인구 데이터 (평균)')
        self.map.add_child(f3)

        concatenated_df = dfs[0]    
        for i, df in enumerate(dfs[1:], start=1):
            suffixes = [f'_{i-1}', f'_{i}']
            concatenated_df = pd.merge(concatenated_df, df, on='행정동명', suffixes=suffixes)

        concatenated_df = concatenated_df.rename(columns={'풋살인구': '풋살인구_'+str(len(dfs[1:]))
                                                        , '시간대': '시간대_'+str(len(dfs[1:]))})
        cols_to_sum = [f'풋살인구_{i}' for i in range(len(dfs))]
        concatenated_df['풋살인구합계'] = concatenated_df[cols_to_sum].mean(axis=1)
        cols_to_drop = [col for col in concatenated_df.columns if '풋살인구_' in col or '시간대' in col]
        concatenated_df = concatenated_df.drop(columns=cols_to_drop)

        #scaler = StandardScaler()
        #data = concatenated_df['풋살인구합계'].values.reshape(-1, 1)
        #scaled_data = scaler.fit_transform(data)
        #concatenated_df['풋살인구합계'] = scaled_data

        # 서울 생활인구 데이터 (평균) folium 설정

        linear = cmp.LinearColormap(
                ['yellow', 'orange', 'red'],
                vmin=min(concatenated_df['풋살인구합계']), vmax=max(concatenated_df['풋살인구합계']),
                caption='시간대별 평균 풋살인구'
                )

        living_population_2 = folium.Choropleth(geo_data=self.json,
                                    data=concatenated_df,
                                    columns=['행정동명', '풋살인구합계'],
                                    key_on='feature.properties.adm_nm',
                                    fill_color='YlOrRd',
                                    fill_opacity=0.7,
                                    line_opacity=0.3,
                                    overlay=False,
                                    show=True,
                                    legend_name='생활인구수',
                                    highlight=True
                                    ).geojson.add_to(f3)  # fg 변수에 추가

        linear.add_to(self.map)
        living_population_2.zoom_on_click = False
        living_population_2.add_child(folium.features.GeoJsonTooltip(['adm_nm'], labels=False))

        return end_time, start_time, concatenated_df