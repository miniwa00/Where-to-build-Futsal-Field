import streamlit as st
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
import pandas as pd
import folium
from folium import plugins


# 서울 풋살장 데이터 전처리
def public_futsal_data():
    public_futsal = pd.read_csv("data/Seoul_Public_Futsal_Field.csv")
    public_futsal["info"] = public_futsal["구장명"] + " | " + public_futsal["비고"]
    return public_futsal


def private_futsal_data():
    private_futsal = pd.read_csv("data/Seoul_Private_Futsal_Field.csv")
    private_futsal["info"] = (
        private_futsal["구장명"]
        + " | "
        + private_futsal["비고"]
        + " | "
        + private_futsal["교육/대관"]
    )
    return private_futsal
