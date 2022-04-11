from cgitb import enable
from operator import index

from matplotlib.pyplot import pause
import streamlit as st
import pandas as pd
import numpy as np
import string
import random
import json
import requests



def convert_df(df):
    """
    convert
    """
    return df.to_csv().encode('utf-8')





st.markdown("<h1 style='text-align: center; color: black;'>TFT CAMP</h1>", unsafe_allow_html=True)
st.header("Tabela atualizada dos jogos da rodada")
option = st.selectbox(
     'Qual rodada gostaria de ver:',
     ('Rodada-1', 'Rodada-2', 'Rodada-3'))

st.write('Você selecionou:', option)





j1=pd.read_csv("j1_Rodada-1.csv")
j2=pd.read_csv("j2_Rodada-1.csv")
j3=pd.read_csv("j3_Rodada-1.csv")
j4=pd.read_csv("j4_Rodada-1.csv")

tabela=pd.concat([j1,j2,j3,j4])
tabela_view=tabela



# st.dataframe(j1)
# st.dataframe(j2)

# nick="Eunucão"

agree = st.checkbox('Jogo-1 Finalizado')

if agree:    
    nick=j1["Nick"][1]
    st.write('Resultados serão computados')
    
    puuid=requests.get(f"https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{nick}?api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
    
    puuid=puuid["puuid"]
    matchs=requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=4&api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
    
    partida=requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/{matchs[0]}?api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
    colocacoes=[]
    for n in range(0,8):
        colocacoes.append(partida["info"]["participants"][n]["placement"])
    
    participantes=partida["metadata"]["participants"]
    nick_p=[]
    for participante in participantes:
        nicks=requests.get(f"https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{participante}?api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
        nick_p.append(nicks["name"])  
    # st.write(nick_p)
    
    data_tuples = list(zip(nick_p,colocacoes))
    pos=pd.DataFrame(data_tuples,columns=["Nick","Jogo"])
   
    j1=j1.merge(pos,how="left",on="Nick",suffixes=["_1"," "])
    # st.dataframe(j1)
    j1["Jogo 1"]=j1["Jogo"]
    j1.drop("Jogo",inplace=True,axis=1)
    j1["Jogo 1"].fillna(0,inplace=True)
    # st.dataframe(j1)
    j1.iloc[:,1:]=j1.iloc[:,1:].astype(int)
    j1["Pontos"]=j1.iloc[:,1:].sum(axis=1)
    j1=j1.sort_values("Pontos",ascending=False)
    # j11=j1
    # j1=j1[["Nick","Jogo 1_y","Jogo 2","Jogo 3","Jogo 4","Pontos"]]
    # st.dataframe(j1)
    
    

    
    if 'key' not in st.session_state:
        st.session_state['key'] = j1




        
    
     
    st.balloons()
    st.write('Resultados computados')
    st.dataframe(st.session_state.key)
    # st.dataframe(j11)
agree2=st.checkbox('Jogo-2 Finalizado')    
    


if agree2:    
    nick=j1["Nick"][1]
    st.write('Resultados serão computados')
    
    puuid=requests.get(f"https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{nick}?api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
    
    puuid=puuid["puuid"]
    matchs=requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=4&api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
    
    partida=requests.get(f"https://americas.api.riotgames.com/tft/match/v1/matches/{matchs[0]}?api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
    colocacoes=[]
    for n in range(0,8):
        colocacoes.append(partida["info"]["participants"][n]["placement"])
    
    participantes=partida["metadata"]["participants"]
    nick_p=[]
    for participante in participantes:
        nicks=requests.get(f"https://br1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{participante}?api_key=RGAPI-138fd8e0-06f7-4c98-a83e-49402304c000").json()
        nick_p.append(nicks["name"])  
    # st.write(nick_p)
    
    data_tuples = list(zip(nick_p,colocacoes))
    pos=pd.DataFrame(data_tuples,columns=["Nick","Jogo"])
   
    j1=j1.merge(pos,how="left",on="Nick",suffixes=["_1"," "])
    # st.dataframe(j1)
    j1["Jogo 2"]=j1["Jogo"]
    j1.drop("Jogo",inplace=True,axis=1)
    j1["Jogo 2"].fillna(0,inplace=True)
    # st.dataframe(j1)
    j1.iloc[:,1:]=j1.iloc[:,1:].astype(int)
    j1["Pontos"]=j1.iloc[:,1:].sum(axis=1)
    j1=j1.sort_values("Pontos",ascending=False)
    if 'key' not in st.session_state:
        st.session_state['key'] = j1




        
    
     
    st.balloons()
    st.write('Resultados computados')
    st.dataframe(st.session_state.key)
    

    


tabela_view.sort_values(by="Pontos",inplace=True)
tabela_view.reset_index(drop=True,inplace=True)
tabela_view.index+=1
st.sidebar.dataframe(tabela_view)

tabela.to_csv(f"tabela{option}.csv")

csv = convert_df(tabela)

 
    
st.download_button(
                label="Baixar tabela",
                data=csv,
                file_name='tabela.csv',
                mime='text/csv'
            )    





