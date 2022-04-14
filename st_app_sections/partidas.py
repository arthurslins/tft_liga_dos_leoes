

import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from PIL import Image
import time


def reset_button():
    st.session_state["p"] = False
    return

__all__ = ["partidas"]

def partidas():
    image = Image.open('assets/Ilustracao_Sem_Titulo.png')
    col1, col2, col3 = st.columns([3,5.5,1])
    with col1:
        st.write("")

    with col2:
        st.image(image,width=250)

    with col3:
        st.write("")
    st.markdown("<h1 style='text-align: center; '>Liga dos Leões</h1>", unsafe_allow_html=True)

    st.write("##")
    st.write('Selecione seu grupo e quando sua partida finalizar clique no botão de finalizar partida para a tabela ser atualizada')
    st.write("##")
    # st.header("Tabela atualizada dos jogos da rodada")
    # option = st.selectbox(
    #     'Qual rodada gostaria de ver:',
    #     ('Rodada-1', 'Rodada-2', 'Rodada-3'))

    # st.write('Você selecionou:', option)


    j1=pd.read_csv("j1_Rodada-1.csv")
    j2=pd.read_csv("j2_Rodada-1.csv")
    j3=pd.read_csv("j3_Rodada-1.csv")
    j4=pd.read_csv("j4_Rodada-1.csv")
    j5=pd.read_csv("j5_Rodada-1.csv")
    j6=pd.read_csv("j6_Rodada-1.csv")
    j7=pd.read_csv("j7_Rodada-1.csv")

    # tabela=pd.concat([j1,j2,j3,j4])
    
    # tabela_view=tabela.loc[:,["Nick","Pontos"]]
    # tabela_view.sort_values("Pontos",ascending=True,inplace=True)
    # tabela_view.reset_index(drop=True,inplace=True)
    # tabela_view.index+=1
    # tabela_view.to_csv("tabela.csv",index=False)
    tabela_view=pd.read_csv('tabela.csv')
    # if 'key' not in st.session_state:
    #     st.session_state.key = tabela_view
    # st.sidebar.title("Ranking global")
    # st.sidebar.dataframe(st.session_state.key)
    # button=st.sidebar.button("Atualizar")
    # if button:
    #     st.sidebar.success("Ranking atualizado")
        

    
    



    def func(df,j):
        nick=df["Nick"][1]
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
        conv_dict=dict({1:10,2:8,3:7,4:6,5:4,6:3,7:2,8:1})
        
        pos=pd.DataFrame(data_tuples,columns=["Nick",f"Jogo{j}"])
        pos=pos.replace({f"Jogo{j}":conv_dict})
        pos.index+=1
        # st.dataframe(pos)
        return pos

    # try:
    option = st.selectbox(
    'Escolha o grupo a ser visualiado',
    ('Grupo 1', 'Grupo 2', 'Grupo 3', "Grupo 4","Grupo 5","Grupo 6","Grupo 7"))

    st.write('Você selecionou:', option)
    
    if option == 'Grupo 1':
        df=j1
        j=1
        if 'df' not in st.session_state:
            st.session_state.df = df
        
        st.dataframe(st.session_state.df)


        col1,col2 = st.columns(2)      
        # if st.session_state.df.sum(axis=1)!= 41:
        with col1:
            # st.write(st.session_state.df.columns)
            
            if st.session_state.df.iloc[:,1].sum(axis=0)!=41:
                jogo_1 = st.button('Calcular resultados do jogo-1')
                with st.spinner('Aguarde um momento...'):
                    j=1
                
                    if jogo_1:
                        j=1
                        pos=func(st.session_state.df,j)
                        st.session_state.df
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        
                        
                        
                        st.session_state.df=st.session_state.df.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df.fillna(0,inplace=True)
                        st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                        st.session_state.df["Pontos"]=0
                        st.session_state.df["Pontos"]= st.session_state.df["Pontos"]+st.session_state.df.iloc[:,-1]
                        st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df.reset_index(drop=True,inplace=True)
                        st.session_state.df.index+=1
                        st.session_state.df=st.session_state.df[["Nick","Jogo1","Pontos"]]
                        
                        
                        # tabela_view=tabela_view.merge(st.session_state.df,on="Nick",how="left")
                        # # tabela_view.fillna(0,inplace=True)
                        # # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # # tabela_view["Pontuação Final"]= tabela_view.iloc[:,1:].sum(axis=1)
                        # # tabela_view=tabela_view[["Nick","Pontuação Final","Pontos da Rodada","Pontos"]]
                        # tabela_view.to_csv("tabela.csv",index=False)
                        
                        
                        st.dataframe(st.session_state.df)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                    
                        
                        
        
            
            
        with col2:
            
            if st.session_state.df.iloc[:,2].sum(axis=0)!=82:   
                
                jogo_2 = st.button('Calcular resultados do jogo-2')
                with st.spinner('Aguarde um momento...'):
                    j=2
                    if jogo_2:
                        pos=func(st.session_state.df,j)
                        
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df=st.session_state.df.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df.fillna(0,inplace=True)
                        st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                        st.session_state.df["Pontos"]=0
                        st.session_state.df["Pontos"]= st.session_state.df.iloc[:,1:].sum(axis=1)
                        st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df.reset_index(drop=True,inplace=True)
                        st.session_state.df.index+=1
                        st.session_state.df=st.session_state.df[["Nick","Jogo1","Jogo2","Pontos"]]
                        st.dataframe(st.session_state.df)

                        # tabela_view["Pontos da Rodada"]=st.session_state.df["Pontos"]
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontuação Final"]= tabela_view.iloc[:,1:].sum(axis=1)
                        # tabela_view=tabela_view[["Nick","Pontuação Final","Pontos da Rodada","Pontos"]]
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                

        with col1:
            
            if st.session_state.df.iloc[:,-1].sum(axis=0)!=123:
                jogo_3 = st.button('Calcular resultados do jogo-3')
                with st.spinner('Aguarde um momento...'):
                    j=3
                    if jogo_3:
                        pos=func(st.session_state.df,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df=st.session_state.df.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df.fillna(0,inplace=True)
                        st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                        st.session_state.df["Pontos"]=0
                        st.session_state.df["Pontos"]=st.session_state.df.iloc[:,1:].sum(axis=1)
                        st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df.reset_index(drop=True,inplace=True)
                        st.session_state.df.index+=1
                        st.session_state.df=st.session_state.df[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                        st.dataframe(st.session_state.df) 

                        # tabela_view["Pontos da Rodada"]=st.session_state.df["Pontos"]
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontuação Final"]= tabela_view.iloc[:,1:].sum(axis=1)
                        # tabela_view=tabela_view[["Nick","Pontuação Final","Pontos da Rodada","Pontos"]]
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                
                    

        with col2:
            
            if st.session_state.df.iloc[:,-1].sum(axis=0)!=164:
                
                jogo_4 = st.button('Calcular resultados do jogo-4')
                with st.spinner('Aguarde um momento...'):
                    j=4
                    if jogo_4:
                        pos=func(st.session_state.df,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df=st.session_state.df.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df.fillna(0,inplace=True)
                        st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                        st.session_state.df["Pontos"]=0
                        st.session_state.df["Pontos"]= st.session_state.df.iloc[:,1:].sum(axis=1)
                        st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df.reset_index(drop=True,inplace=True)
                        st.session_state.df.index+=1
                        st.session_state.df=st.session_state.df[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                        st.session_state.df

                        # tabela_view["Pontos da Rodada"]=st.session_state.df["Pontos"]
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontuação Final"]= tabela_view.iloc[:,1:].sum(axis=1)
                        # tabela_view=tabela_view[["Nick","Pontuação Final","Pontos da Rodada","Pontos"]]
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                
        
        
        
    elif option =="Grupo 2":
        df=j2
        j=2
        if 'df2' not in st.session_state:
            st.session_state.df2 = df
        # ss=st.session_state.df2
        st.dataframe(st.session_state.df2)
        

        col1,col2 = st.columns(2)      
        with col1:
            
                if st.session_state.df2.iloc[:,1].sum(axis=0)!=41:
                    
                    jogo_12 = st.button('Calcular resultados do jogo-1')
                    with st.spinner('Aguarde um momento...'):
                        j=1
                    
                        if jogo_12:
                            j=1
                            pos=func(st.session_state.df2,j)
                            st.session_state.df2
                            # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                            # tabela_view.fillna(0,inplace=True)
                            # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                            # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                            # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                            # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                            # tabela_view.reset_index(drop=True,inplace=True)
                            # tabela_view.index+=1
                            # tabela_view.to_csv("tabela.csv",index=False)
                            st.session_state.df2=st.session_state.df2.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                            st.session_state.df2.fillna(0,inplace=True)
                            st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                            st.session_state.df2["Pontos"]=0
                            st.session_state.df2["Pontos"]= st.session_state.df2["Pontos"]+st.session_state.df2.iloc[:,-1]
                            st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                            st.session_state.df2.reset_index(drop=True,inplace=True)
                            st.session_state.df2.index+=1
                            st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Pontos"]]
                            st.dataframe(st.session_state.df2)
                            st.balloons()
                            time.sleep(2)
                            st.experimental_rerun()
                    
                    

        
            
            
        with col2:
            if st.session_state.df2.iloc[:,2].sum(axis=0)!=82:
                   
                jogo_22 = st.button('Calcular resultados do jogo-2')
                with st.spinner('Aguarde um momento...'):
                    j=2
                    if jogo_22:
                        pos=func(st.session_state.df2,j)
                        
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df2=st.session_state.df2.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df2.fillna(0,inplace=True)
                        st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                        st.session_state.df2["Pontos"]=0
                        st.session_state.df2["Pontos"]= st.session_state.df2.iloc[:,1:].sum(axis=1)
                        st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df2.reset_index(drop=True,inplace=True)
                        st.session_state.df2.index+=1
                        st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Jogo2","Pontos"]]
                        st.session_state.df2
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                    

        with col1:
            if st.session_state.df2.iloc[:,-1].sum(axis=0)!=123:
                jogo_32 = st.button('Calcular resultados do jogo-3')
                with st.spinner('Aguarde um momento...'):
                    j=3
                    if jogo_32:
                        pos=func(st.session_state.df2,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df2=st.session_state.df2.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df2.fillna(0,inplace=True)
                        st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                        st.session_state.df2["Pontos"]=0
                        st.session_state.df2["Pontos"]= st.session_state.df2.iloc[:,1:].sum(axis=1)
                        st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df2.reset_index(drop=True,inplace=True)
                        st.session_state.df2.index+=1
                        st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                        st.session_state.df2
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col2:
            if st.session_state.df2.iloc[:,-1].sum(axis=0)!=164:
                jogo_42 = st.button('Calcular resultados do jogo-4')
                with st.spinner('Aguarde um momento...'):
                    j=4
                    if jogo_42:
                        pos=func(st.session_state.df2,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df2=st.session_state.df2.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df2.fillna(0,inplace=True)
                        st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                        st.session_state.df2["Pontos"]=0
                        st.session_state.df2["Pontos"]= st.session_state.df2.iloc[:,1:].sum(axis=1)
                        st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df2.reset_index(drop=True,inplace=True)
                        st.session_state.df2.index+=1
                        st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                        st.session_state.df2
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()



    elif option == "Grupo 3":
        df=j3
        if 'df3' not in st.session_state:
            st.session_state.df3 = df
        st.dataframe(st.session_state.df3)
        j=3

        col1,col2 = st.columns(2)      
        with col1:
            if st.session_state.df3.iloc[:,1].sum(axis=0)!=41:
                jogo_13 = st.button('Calcular resultados do jogo-1')
                with st.spinner('Aguarde um momento...'):
                    j=1
                
                    if jogo_13:
                        
                        pos=func(st.session_state.df3,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df3=st.session_state.df3.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df3.fillna(0,inplace=True)
                        st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                        st.session_state.df3["Pontos"]=0
                        st.session_state.df3["Pontos"]= st.session_state.df3.iloc[:,1:].sum(axis=1)
                        st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df3.reset_index(drop=True,inplace=True)
                        st.session_state.df3.index+=1
                        st.session_state.df3=st.session_state.df3[["Nick","Jogo1","Pontos"]]
                        st.dataframe(st.session_state.df3)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                    
        
            
            
        with col2:
            if st.session_state.df3.iloc[:,-1].sum(axis=0)!=82:   
                jogo_23 = st.button("Calcular resultados do jogo-2")
                with st.spinner('Aguarde um momento...'):
                    j=2
                    if jogo_23:
                        pos=func(st.session_state.df3,j)
                        
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df3=st.session_state.df3.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df3.fillna(0,inplace=True)
                        st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                        st.session_state.df3["Pontos"]=0
                        st.session_state.df3["Pontos"]= st.session_state.df3.iloc[:,1:].sum(axis=1)
                        st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df3.reset_index(drop=True,inplace=True)
                        st.session_state.df3.index+=1
                        st.session_state.df3=st.session_state.df3[["Nick","Jogo1","Jogo2","Pontos"]]
                        st.session_state.df3
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col1:
            if st.session_state.df3.iloc[:,-1].sum(axis=0)!=123:
                jogo_33 = st.button("Calcular resultados do jogo-3")
                with st.spinner('Aguarde um momento...'):
                    j=3
                    if jogo_33:
                        pos=func(st.session_state.df3,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df3=st.session_state.df3.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df3.fillna(0,inplace=True)
                        st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                        st.session_state.df3["Pontos"]=0
                        st.session_state.df3["Pontos"]= st.session_state.df3.iloc[:,1:].sum(axis=1)
                        st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df3.reset_index(drop=True,inplace=True)
                        st.session_state.df3.index+=1
                        st.session_state.df3=st.session_state.df3[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                        st.session_state.df3
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col2:
            if st.session_state.df3.iloc[:,-1].sum(axis=0)!=164:
                jogo_43 = st.button('Calcular resultados do jogo-4')
                with st.spinner('Aguarde um momento...'):
                    j=4
                    if jogo_43:
                        pos=func(st.session_state.df3,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df3=st.session_state.df3.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df3.fillna(0,inplace=True)
                        st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                        st.session_state.df3["Pontos"]=0
                        st.session_state.df3["Pontos"]= st.session_state.df3.iloc[:,1:].sum(axis=1)
                        st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df3.reset_index(drop=True,inplace=True)
                        st.session_state.df3.index+=1
                        st.session_state.df3=st.session_state.df3[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                        st.session_state.df3
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

    elif option == "Grupo 4":
        df=j4
        if 'df4' not in st.session_state:
            st.session_state.df4 = df
        st.dataframe(st.session_state.df4)  
        j=4
        col1,col2 = st.columns(2) 
        with col1:
            if st.session_state.df4.iloc[:,1].sum(axis=0)!=41:
                jogo_14 = st.button('Calcular resultados do jogo-1')
                with st.spinner('Aguarde um momento...'):
                    j=1
                
                    if jogo_14:
                        
                        pos=func(st.session_state.df4,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df4=st.session_state.df4.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df4.fillna(0,inplace=True)
                        st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                        st.session_state.df4["Pontos"]=0
                        st.session_state.df4["Pontos"]=  st.session_state.df4.iloc[:,1:].sum(axis=1)
                        st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df4.reset_index(drop=True,inplace=True)
                        st.session_state.df4.index+=1
                        st.session_state.df4=st.session_state.df4[["Nick","Jogo1","Pontos"]]
                        st.dataframe(st.session_state.df4)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                        
        
            
            
        with col2:
            if st.session_state.df4.iloc[:,-1].sum(axis=0)!=82:   
                jogo_24 = st.button('Calcular resultados do jogo-2')
                with st.spinner('Aguarde um momento...'):
                    j=2
                    if jogo_24:
                        pos=func(st.session_state.df4,j)
                        
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df4=st.session_state.df4.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df4.fillna(0,inplace=True)
                        st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                        st.session_state.df4["Pontos"]=0
                        st.session_state.df4["Pontos"]= st.session_state.df4.iloc[:,1:].sum(axis=1)
                        st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df4.reset_index(drop=True,inplace=True)
                        st.session_state.df4.index+=1
                        st.session_state.df4=st.session_state.df4[["Nick","Jogo1","Jogo2","Pontos"]]
                        st.session_state.df4
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col1:
            if st.session_state.df4.iloc[:,-1].sum(axis=0)!=123:
                jogo_34 = st.button('Calcular resultados do jogo-3')
                with st.spinner('Aguarde um momento...'):
                    j=3
                    if jogo_34:
                        pos=func(st.session_state.df4,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df4=st.session_state.df4.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df4.fillna(0,inplace=True)
                        st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                        st.session_state.df4["Pontos"]=0
                        st.session_state.df4["Pontos"]= st.session_state.df4.iloc[:,1:].sum(axis=1)
                        st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df4.reset_index(drop=True,inplace=True)
                        st.session_state.df4.index+=1
                        st.session_state.df4=st.session_state.df4[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                        st.session_state.df4
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col2:
            if st.session_state.df4.iloc[:,-1].sum(axis=0)!=164:
                jogo_44 = st.button('Calcular resultados do jogo-4')
                with st.spinner('Aguarde um momento...'):
                    j=4
                    if jogo_44:
                        pos=func(st.session_state.df4,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df4=st.session_state.df4.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df4.fillna(0,inplace=True)
                        st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                        st.session_state.df4["Pontos"]=0
                        st.session_state.df4["Pontos"]= st.session_state.df4.iloc[:,1:].sum(axis=1)
                        st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df4.reset_index(drop=True,inplace=True)
                        st.session_state.df4.index+=1
                        st.session_state.df4=st.session_state.df4[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                        st.session_state.df4
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

    elif option == "Grupo 5":
        df=j5
        if 'df5' not in st.session_state:
            st.session_state.df5 = df
        st.dataframe(st.session_state.df5)  
        j=5
        col1,col2 = st.columns(2) 
        with col1:
            if st.session_state.df5.iloc[:,1].sum(axis=0)!=41:
                jogo_15 = st.button('Calcular resultados do jogo-1')
                with st.spinner('Aguarde um momento...'):
                    j=1
                
                    if jogo_15:
                        
                        pos=func(st.session_state.df5,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df5=st.session_state.df5.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df5.fillna(0,inplace=True)
                        st.session_state.df5.iloc[:,1:]=st.session_state.df5.iloc[:,1:].astype(int)
                        st.session_state.df5["Pontos"]=0
                        st.session_state.df5["Pontos"]= st.session_state.df5.iloc[:,1:].sum(axis=1)
                        st.session_state.df5.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df5.reset_index(drop=True,inplace=True)
                        st.session_state.df5.index+=1
                        st.session_state.df5=st.session_state.df5[["Nick","Jogo1","Pontos"]]
                        st.dataframe(st.session_state.df5)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                        
        
            
            
        with col2:
            if st.session_state.df5.iloc[:,-1].sum(axis=0)!=82:   
                jogo_25 = st.button('Calcular resultados do jogo-2')
                with st.spinner('Aguarde um momento...'):
                    j=2
                    if jogo_25:
                        pos=func(st.session_state.df5,j)
                        
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df5=st.session_state.df5.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df5.fillna(0,inplace=True)
                        st.session_state.df5.iloc[:,1:]=st.session_state.df5.iloc[:,1:].astype(int)
                        st.session_state.df5["Pontos"]=0
                        st.session_state.df5["Pontos"]= st.session_state.df5.iloc[:,1:].sum(axis=1)
                        st.session_state.df5.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df5.reset_index(drop=True,inplace=True)
                        st.session_state.df5.index+=1
                        st.session_state.df5=st.session_state.df5[["Nick","Jogo1","Jogo2","Pontos"]]
                        st.session_state.df5
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col1:
            if st.session_state.df5.iloc[:,-1].sum(axis=0)!=123:
                jogo_35 = st.button('Calcular resultados do jogo-3')
                with st.spinner('Aguarde um momento...'):
                    j=3
                    if jogo_35:
                        pos=func(st.session_state.df5,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df5=st.session_state.df5.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df5.fillna(0,inplace=True)
                        st.session_state.df5.iloc[:,1:]=st.session_state.df5.iloc[:,1:].astype(int)
                        st.session_state.df5["Pontos"]=0
                        st.session_state.df5["Pontos"]= st.session_state.df5.iloc[:,1:].sum(axis=1)
                        st.session_state.df5.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df5.reset_index(drop=True,inplace=True)
                        st.session_state.df5.index+=1
                        st.session_state.df5=st.session_state.df5[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                        st.session_state.df5
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col2:
            if st.session_state.df5.iloc[:,-1].sum(axis=0)!=164:
                jogo_45 = st.button('Calcular resultados do jogo-4')
                with st.spinner('Aguarde um momento...'):
                    j=4
                    if jogo_45:
                        pos=func(st.session_state.df5,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df5=st.session_state.df5.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df5.fillna(0,inplace=True)
                        st.session_state.df5.iloc[:,1:]=st.session_state.df5.iloc[:,1:].astype(int)
                        st.session_state.df5["Pontos"]=0
                        st.session_state.df5["Pontos"]= st.session_state.df5.iloc[:,1:].sum(axis=1)
                        st.session_state.df5.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df5.reset_index(drop=True,inplace=True)
                        st.session_state.df5.index+=1
                        st.session_state.df5=st.session_state.df5[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                        st.session_state.df5
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()


    elif option == "Grupo 6":
        df=j6
        if 'df6' not in st.session_state:
            st.session_state.df6 = df
        st.dataframe(st.session_state.df6)  
        j=6
        col1,col2 = st.columns(2) 
        with col1:
            if st.session_state.df6.iloc[:,1].sum(axis=0)!=41:
                jogo_16 = st.button('Calcular resultados do jogo-1')
                with st.spinner('Aguarde um momento...'):
                    j=1
                
                    if jogo_16:
                        
                        pos=func(st.session_state.df6,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df6=st.session_state.df6.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df6.fillna(0,inplace=True)
                        st.session_state.df6.iloc[:,1:]=st.session_state.df6.iloc[:,1:].astype(int)
                        st.session_state.df6["Pontos"]=0
                        st.session_state.df6["Pontos"]= st.session_state.df6.iloc[:,1:].sum(axis=1)
                        st.session_state.df6.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df6.reset_index(drop=True,inplace=True)
                        st.session_state.df6.index+=1
                        st.session_state.df6=st.session_state.df6[["Nick","Jogo1","Pontos"]]
                        st.dataframe(st.session_state.df6)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                        
        
            
            
        with col2:
            if st.session_state.df6.iloc[:,-1].sum(axis=0)!=82:   
                jogo_26 = st.button('Calcular resultados do jogo-2')
                with st.spinner('Aguarde um momento...'):
                    j=2
                    if jogo_26:
                        pos=func(st.session_state.df6,j)
                        
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df6=st.session_state.df6.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df6.fillna(0,inplace=True)
                        st.session_state.df6.iloc[:,1:]=st.session_state.df6.iloc[:,1:].astype(int)
                        st.session_state.df6["Pontos"]=0
                        st.session_state.df6["Pontos"]= st.session_state.df6.iloc[:,1:].sum(axis=1)
                        st.session_state.df6.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df6.reset_index(drop=True,inplace=True)
                        st.session_state.df6.index+=1
                        st.session_state.df6=st.session_state.df6=st.session_state.df6[["Nick","Jogo1","Jogo2","Pontos"]]
                        st.session_state.df6
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col1:
            if st.session_state.df6.iloc[:,-1].sum(axis=0)!=123:
                jogo_36 = st.button('Calcular resultados do jogo-3')
                with st.spinner('Aguarde um momento...'):
                    j=3
                    if jogo_36:
                        pos=func(st.session_state.df6,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df6=st.session_state.df6.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df6.fillna(0,inplace=True)
                        st.session_state.df6.iloc[:,1:]=st.session_state.df6.iloc[:,1:].astype(int)
                        st.session_state.df6["Pontos"]=0
                        st.session_state.df6["Pontos"]= st.session_state.df6.iloc[:,1:].sum(axis=1)
                        st.session_state.df6.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df6.reset_index(drop=True,inplace=True)
                        st.session_state.df6.index+=1
                        st.session_state.df6=st.session_state.df6[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                        st.session_state.df6
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col2:
            if st.session_state.df6.iloc[:,-1].sum(axis=0)!=164:
                jogo_46 = st.button('Calcular resultados do jogo-4')
                with st.spinner('Aguarde um momento...'):
                    j=4
                    if jogo_46:
                        pos=func(st.session_state.df6,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df6=st.session_state.df6.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df6.fillna(0,inplace=True)
                        st.session_state.df6.iloc[:,1:]=st.session_state.df6.iloc[:,1:].astype(int)
                        st.session_state.df6["Pontos"]=0
                        st.session_state.df6["Pontos"]= st.session_state.df6.iloc[:,1:].sum(axis=1)
                        st.session_state.df6.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df6.reset_index(drop=True,inplace=True)
                        st.session_state.df6.index+=1
                        st.session_state.df6=st.session_state.df6[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                        st.session_state.df6
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()


    elif option == "Grupo 7":
        df=j7
        if 'df7' not in st.session_state:
            st.session_state.df7 = df
        st.dataframe(st.session_state.df7)  
        j=7
        col1,col2 = st.columns(2) 
        with col1:
            if st.session_state.df7.iloc[:,1].sum(axis=0)!=41:
                jogo_17 = st.button('Calcular resultados do jogo-1')
                with st.spinner('Aguarde um momento...'):
                    j=1
                
                    if jogo_17:
                        
                        pos=func(st.session_state.df7,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df7=st.session_state.df7.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df7.fillna(0,inplace=True)
                        st.session_state.df7.iloc[:,1:]=st.session_state.df7.iloc[:,1:].astype(int)
                        st.session_state.df7["Pontos"]=0
                        st.session_state.df7["Pontos"]= st.session_state.df7.iloc[:,1:].sum(axis=1)
                        st.session_state.df7.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df7.reset_index(drop=True,inplace=True)
                        st.session_state.df7.index+=1
                        st.session_state.df7=st.session_state.df7[["Nick","Jogo1","Pontos"]]
                        st.dataframe(st.session_state.df7)
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()
                    
        
            
            
        with col2:
            if st.session_state.df7.iloc[:,-1].sum(axis=0)!=82:   
                jogo_27 = st.button('Calcular resultados do jogo-2')
                with st.spinner('Aguarde um momento...'):
                    j=2
                    if jogo_27:
                        pos=func(st.session_state.df7,j)
                        
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df7=st.session_state.df7.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df7.fillna(0,inplace=True)
                        st.session_state.df7.iloc[:,1:]=st.session_state.df7.iloc[:,1:].astype(int)
                        st.session_state.df7["Pontos"]=0
                        st.session_state.df7["Pontos"]= st.session_state.df7.iloc[:,1:].sum(axis=1)
                        st.session_state.df7.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df7.reset_index(drop=True,inplace=True)
                        st.session_state.df7.index+=1
                        st.session_state.df7=st.session_state.df7[["Nick","Jogo1","Jogo2","Pontos"]]
                        st.session_state.df7
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col1:
            if st.session_state.df7.iloc[:,-1].sum(axis=0)!=123:
                jogo_37 = st.button('Calcular resultados do jogo-3')
                with st.spinner('Aguarde um momento...'):
                    j=3
                    if jogo_37:
                        pos=func(st.session_state.df7,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df7=st.session_state.df7.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df7.fillna(0,inplace=True)
                        st.session_state.df7.iloc[:,1:]=st.session_state.df7.iloc[:,1:].astype(int)
                        st.session_state.df7["Pontos"]=0
                        st.session_state.df7["Pontos"]= st.session_state.df7.iloc[:,1:].sum(axis=1)
                        st.session_state.df7.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df7.reset_index(drop=True,inplace=True)
                        st.session_state.df7.index+=1
                        st.session_state.df7=st.session_state.df7[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                        st.session_state.df7
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()

        with col2:
            if st.session_state.df7.iloc[:,-1].sum(axis=0)!=164:
                jogo_47 = st.button('Calcular resultados do jogo-4')
                with st.spinner('Aguarde um momento...'):
                    j=4
                    if jogo_47:
                        pos=func(st.session_state.df7,j)
                        # tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                        # tabela_view.fillna(0,inplace=True)
                        # tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                        # tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                        # tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                        # tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                        # tabela_view.reset_index(drop=True,inplace=True)
                        # tabela_view.index+=1
                        # tabela_view.to_csv("tabela.csv",index=False)
                        st.session_state.df7=st.session_state.df7.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                        st.session_state.df7.fillna(0,inplace=True)
                        st.session_state.df7.iloc[:,1:]=st.session_state.df7.iloc[:,1:].astype(int)
                        st.session_state.df7["Pontos"]=0
                        st.session_state.df7["Pontos"]= st.session_state.df7.iloc[:,1:].sum(axis=1)
                        st.session_state.df7.sort_values("Pontos",ascending=False,inplace=True)
                        st.session_state.df7.reset_index(drop=True,inplace=True)
                        st.session_state.df7.index+=1
                        st.session_state.df7=st.session_state.df7[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                        st.session_state.df7
                        st.balloons()
                        time.sleep(2)
                        st.experimental_rerun()




    # st.write("##")
    # st.write('Selecione seu grupo e quando sua partida finalizar clique no botão de finalizar partida para a tabela ser atualizada')
    # st.write("##")
    # def func2(s_s,tabela_view):
    #         s_s=s_s.loc[:,"Nick"].to_frame().merge(pos,on='Nick',how='left')
    #         s_s.fillna(0,inplace=True)
    #         s_s.iloc[:,1:]=s_s.iloc[:,1:].astype(int)
    #         s_s["Pontos"]=0
    #         s_s["Pontos"]= s_s["Pontos"]+s_s[f"Jogo{j}"]
    #         s_s.sort_values("Pontos",ascending=False,inplace=True)
    #         s_s.reset_index(drop=True,inplace=True)
    #         s_s.index+=1
    #         s_s

    

    # rank=pd.read_csv("tabela.csv")
    # rank.index+=1
    # # st.title("Ranking Global")
    # # st.dataframe(rank)    
    # except Exception:
    #     pass
if __name__ == "__main__":
    partidas()