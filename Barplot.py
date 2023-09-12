import streamlit as st
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
import pandas as pd
import folium
from folium import plugins
import branca.colormap as cmp
import matplotlib.pyplot as plt
import seaborn as sns

class Barplot:
    
    def __init__(self, end_time, start_time, end_time_sub, start_time_sub, concatenated_df):
        self.end_time = end_time
        self.start_time = start_time
        self.end_time_sub = end_time_sub
        self.start_time_sub = start_time_sub
        self.concatenated_df = concatenated_df
    
    def subwayBarplot(self):
        
        st.header('호선, 시간대 별 승/하차 인원수')
        subway_range = st.radio('호선선택', options = ['1호선','2호선','3호선','4호선','5호선','6호선','7호선','8호선','9호선'])

        df = pd.read_csv('data/Subway_Boarding.csv', encoding = 'utf-8') 
        df = df.drop(columns = ['사용월'], axis=1)
        df = df[df['호선명'] == subway_range]
        g_subway3 = df.groupby(['호선명','지하철역']).agg('mean')
        g_sub3 = pd.DataFrame(g_subway3.stack())
        index = []
        b= []
        for i in g_sub3.index:
            index.append(i[2])

        for j in index:
            b.append(int(j[:2]))

        g_sub3['시간대'] = b   
        g_sub3 = g_sub3.rename(columns = {0 : '승차 인원수'})
        g_sub3 = g_sub3.dropna()

        df = pd.read_csv('data/Subway_Disembarking.csv', encoding = 'utf-8') 
        df = df.drop(columns = ['사용월'], axis=1)
        df = df[df['호선명'] == subway_range]

        g_subway4 = df.groupby(['호선명','지하철역']).agg('mean')
        g_sub4 = pd.DataFrame(g_subway4.stack())
        index = []
        b = []
        for i in g_sub4.index:
            index.append(i[2])
        for j in index:
            b.append(int(j[:2]))

        g_sub4['시간대'] = b   
        g_sub4 = g_sub4.rename(columns = {0 : '하차 인원수'})
        g_sub4 = g_sub4.dropna()

        if self.end_time > self.start_time:
            temp_sub3 = g_sub3[g_sub3['시간대'].between(self.start_time_sub, self.end_time_sub)]
            temp_sub4 = g_sub4[g_sub4['시간대'].between(self.start_time_sub, self.end_time_sub)]
        c = []
        for i in temp_sub3.index:
            c.append(i[1])
        temp_sub3 = pd.DataFrame(index = c, data = temp_sub3['승차 인원수'].values, columns = ['승차 인원수'])
        c = []
        for i in temp_sub4.index:
            c.append(i[1])
        temp_sub4 = pd.DataFrame(index = c, data = temp_sub4['하차 인원수'].values, columns = ['하차 인원수'])

        st.write('승차 인원수 그래프 (사이드 바 시간과 연동)')
        st.bar_chart(data = temp_sub3)
        st.write('하차 인원수 그래프 (사이드 바 시간과 연동)')
        st.bar_chart(data = temp_sub4)

    def livingPopulationBarplot(self):
        st.header('지역/시간대별 평균 생활인구 필터링')
        my_df = self.concatenated_df.copy()
        my_df['행정동명'] = my_df['행정동명'].str.replace('서울특별시', '').str.strip()
        sel_opt = my_df['행정동명']
        sel_box = st.multiselect('지역을 선택하세요', sel_opt, default=('종로구 사직동', '강남구 논현1동', '은평구 진관동'))

        my_df = my_df[my_df.행정동명.isin(sel_box)]
        fig = plt.figure(figsize=(15,10))
        ax = sns.barplot(x=my_df.행정동명, y=my_df.풋살인구합계, data=my_df)
        ax.bar_label(ax.containers[0], label_type='center', color='white')
        st.write('생활인구수 그래프 (사이드 바 시간과 연동)')
        st.bar_chart(my_df, x='행정동명', y='풋살인구합계')