import streamlit as st
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cmp

class Subway:
    
    def __init__(self, map, json, end_time, start_time):
        self.map = map
        self.json = json
        self.end_time = end_time
        self.start_time = start_time
    
    def subway(self):
        
        # 서울 지하철 승하차 데이터 Streamlit 설정

        st.sidebar.title("서울 지하철 승하차 데이터")

        sel_opt = ['승차','하차']
        sel_box = st.sidebar.multiselect('승하차 여부를 선택하세요', sel_opt)

        st.sidebar.header("시간대 조건")
        col5, col6 = st.sidebar.columns(2)
        with col5:
            start_time_sub = st.slider("시작시간", 0, 22, 0, 1, key=5)  
        with col6:
            end_time_sub = st.slider("종료시간", 1, 23, 1, 1, key=6)  


        # 서울 지하철 승차 데이터 전처리

        df = pd.read_csv('data/Subway_Boarding.csv', encoding = 'utf-8') 
        df = df.drop(columns = ['사용월', '호선명'], axis=1)

        subway = pd.merge(df, self.json, how = 'inner', on = '지하철역')
        g_subway = subway.groupby(['지하철역']).agg('mean')

        lat = g_subway[['위도','경도']]
        g_subway = g_subway.drop(columns = ['위도','경도'])

        g_sub = pd.DataFrame(g_subway.stack())
        g_sub = g_sub.rename(columns = {0 : '승차인원수'})

        g_sub1 = pd.merge(g_sub,lat, how = 'left', on = '지하철역')

        index = []
        b = []
        for i in g_sub.index:
            index.append(i[1])
        for j in index:
            b.append(int(j[:2]))

        g_sub1['시간대'] = b   
        g_sub1 = g_sub1.dropna()

        g_sub1['승하차여부'] = '승차'
        g_sub1 = g_sub1.rename(columns={'승차인원수' : '인원수'})

        # 서울 지하철 하차 데이터 전처리

        df = pd.read_csv('data/Subway_Disembarking.csv', encoding = 'utf-8') 
        df = df.drop(columns = ['사용월', '호선명'], axis=1)

        subway = pd.merge(df, self.json, how = 'inner', on = '지하철역')
        g_subway = subway.groupby(['지하철역']).agg('mean')

        lat = g_subway[['위도','경도']]
        g_subway = g_subway.drop(columns = ['위도','경도'])

        g_sub = pd.DataFrame(g_subway.stack())
        g_sub = g_sub.rename(columns = {0 : '하차인원수'})

        g_sub2 = pd.merge(g_sub,lat, how = 'left', on = '지하철역')

        index = []
        b = []
        for i in g_sub.index:
            index.append(i[1])
        for j in index:
            b.append(int(j[:2]))

        g_sub2['시간대'] = b   
        g_sub2 = g_sub2.dropna()

        g_sub2['승하차여부'] = '하차'
        g_sub2 = g_sub2.rename(columns = {'하차인원수' : '인원수'})

        # 서울 지하철 승하차 folium 설정

        if self.end_time > self.start_time:
            temp_sub1 = g_sub1[g_sub1['시간대'].between(start_time_sub, end_time_sub)]
            temp_sub2 = g_sub2[g_sub2['시간대'].between(start_time_sub, end_time_sub)]

        m2 = folium.FeatureGroup(name='승차 데이터')
        self.map.add_child(m2)

        m3 = folium.FeatureGroup(name='하차 데이터')
        self.map.add_child(m3)

        for i in range(len(sel_box)):
            if sel_box[i] == '승차':
                for i in range(len(temp_sub1)):
                    lat = temp_sub1.iloc[i,1]
                    lng = temp_sub1.iloc[i,2]
                    pop = temp_sub1.iloc[i,0]
                    folium.CircleMarker([lat,lng],
                                        radius = pop/5000,
                                        color = 'green').add_to(m2)
            else:
                for i in range(len(temp_sub2)):
                    lat = temp_sub2.iloc[i,1]
                    lng = temp_sub2.iloc[i,2]
                    pop = temp_sub2.iloc[i,0]
                    folium.CircleMarker([lat,lng],
                                        radius = pop/5000,
                                        color = 'blue').add_to(m3)
                    
        return end_time_sub, start_time_sub