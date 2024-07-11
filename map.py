import os
import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
from Futsal_Field import public_futsal_data, private_futsal_data


public_futsal = public_futsal_data()
private_futsal = private_futsal_data()
# Streamlit 설정
st.set_page_config(page_title="Seoul Futsal Field Map", layout="centered")
st.title("Seoul Futsal Field Map")
st.caption("Created by [Your Name]")

# 서울 지도 생성
seoul_map = folium.Map(
    location=[37.5642135, 127.0016985], tiles="cartoDB positron", zoom_start=12
)

# ----------------------------------------------------풋살장------------------------------------------------
# 사이드바 설정
st.sidebar.title("서울 풋살장 데이터")
sel_opt1 = ["공공", "민간"]
sel_box1 = st.sidebar.multiselect("풋살장 종류를 골라주세요", sel_opt1)

# 공공 풋살장 추가
if "공공" in sel_box1:
    for i in range(len(public_futsal)):
        lat = public_futsal.loc[i, "위도"]
        long = public_futsal.loc[i, "경도"]
        info = public_futsal.loc[i, "info"]
        folium.Marker(
            [lat, long], icon=folium.Icon(icon="info-sign", color="blue"), tooltip=info
        ).add_to(seoul_map)

# 민간 풋살장 추가
if "민간" in sel_box1:
    for i in range(len(private_futsal)):
        lat = private_futsal.loc[i, "위도"]
        long = private_futsal.loc[i, "경도"]
        info = private_futsal.loc[i, "info"]
        folium.Marker(
            [lat, long], icon=folium.Icon(icon="info-sign", color="red"), tooltip=info
        ).add_to(seoul_map)

# ---------------------------------------------------거주 인구---------------------------------------

# 지도 렌더링
st_folium(seoul_map, width=725)
