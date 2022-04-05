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

# def id_generator(size=30, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

# num_rows = 48

# data = np.array([id_generator() for i in range(2*num_rows)]).reshape(-1,3)
# df1=pd.DataFrame(data,columns=["Nome","Nick","Discord"])

# np_j1=np.arange(7,33,4)
# np_j1=np.append(np_j1,0)
# np_j1=np.sort(np_j1)

# np_j2=np.arange(6,33,4)
# np_j2=np.append(np_j2,1)
# np_j2=np.sort(np_j2)


# np_j3=np.arange(5,33,4)
# np_j3=np.append(np_j3,2)
# np_j3=np.sort(np_j3)

# np_j4=np.arange(4,32,4)
# np_j4=np.append(np_j4,3)
# np_j4=np.sort(np_j4)



# def shuffle(np_j1,np_j2,np_j3,np_j4,df1):
#     j1=df1.iloc[list(np_j1)]
#     j2=df1.iloc[list(np_j2)]
#     j3=df1.iloc[list(np_j3)]
#     j4=df1.iloc[list(np_j4)]
    
#     return j1,j2,j3,j4

# j1,j2,j3,j4=shuffle(np_j1,np_j2,np_j3,np_j4,df1)

st.markdown("<h1 style='text-align: center; color: black;'>TFT CAMP</h1>", unsafe_allow_html=True)
st.header("Tabela atualizada dos jogos da rodada")
option = st.selectbox(
     'Qual rodada gostaria de ver:',
     ('Rodada-1', 'Rodada-2', 'Rodada-3'))

st.write('Você selecionou:', option)



# j1=j1.reset_index(drop=True)
# j1.index+=1
# j1.drop(["Nome","Discord"],axis=1,inplace=True)
# j1[["Jogo-1","Jogo-2","Jogo-3","Jogo-4","Pontuação"]]=0

# j2=j2.reset_index(drop=True)
# j2.index+=1
# j2.drop(["Nome","Discord"],axis=1,inplace=True)
# j2[["Jogo-1","Jogo-2","Jogo-3","Jogo-4","Pontuação"]]=0

# j3=j3.reset_index(drop=True)
# j3.index+=1
# j3.drop(["Nome","Discord"],axis=1,inplace=True)
# j3[["Jogo-1","Jogo-2","Jogo-3","Jogo-4","Pontuação"]]=0

# j4=j4.reset_index(drop=True)
# j4.index+=1
# j4.drop(["Nome","Discord"],axis=1,inplace=True)
# j4[["Jogo-1","Jogo-2","Jogo-3","Jogo-4","Pontuação"]]=0

j1=pd.read_csv("j1_Rodada-1.csv")
j2=pd.read_csv("j2_Rodada-1.csv")
j3=pd.read_csv("j3_Rodada-1.csv")
j4=pd.read_csv("j4_Rodada-1.csv")

tabela=pd.concat([j1,j2,j3,j4])
tabela_view=tabela

# j1.to_csv(f"j1_{option}.csv",index=False)
# j2.to_csv(f"j2_{option}.csv",index=False)
# j3.to_csv(f"j3_{option}.csv",index=False)
# j4.to_csv(f"j4_{option}.csv",index=False)

# view_df1, view_df2 = st.columns(2)

st.dataframe(j1)
# nick=j1["Nick"][1]
nick="Eunucão"
agree = st.checkbox('Jogo-1 Finalizado')

if agree:    
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
    pos=pd.DataFrame(data_tuples,columns=["Nick","Jogo-1"])
    # st.dataframe(pos)
    j1=j1.merge(pos,how="left",on="Nick")
    
     
    st.balloons()
    st.write('Resultados computados')

# st.dataframe(j1)
st.dataframe(j2)
st.dataframe(j3)
st.dataframe(j4)
# tabela_view.sort_values(by="Pontuação",inplace=True)
# tabela_view.reset_index(drop=True,inplace=True)
# tabela_view.index+=1
# view_df2.dataframe(tabela_view)

tabela.to_csv(f"tabela{option}.csv")

csv = convert_df(tabela)

 
    
st.download_button(
                label="Baixar tabela",
                data=csv,
                file_name='tabela.csv',
                mime='text/csv'
            )    





