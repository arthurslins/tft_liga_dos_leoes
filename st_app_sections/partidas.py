
import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from PIL import Image



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
    # st.header("Tabela atualizada dos jogos da rodada")
    # option = st.selectbox(
    #     'Qual rodada gostaria de ver:',
    #     ('Rodada-1', 'Rodada-2', 'Rodada-3'))

    # st.write('Você selecionou:', option)


    j1=pd.read_csv("j1_Rodada-1.csv")
    j2=pd.read_csv("j2_Rodada-1.csv")
    j3=pd.read_csv("j3_Rodada-1.csv")
    j4=pd.read_csv("j4_Rodada-1.csv")

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
        pos=pd.DataFrame(data_tuples,columns=["Nick",f"Jogo{j}"])
        pos.index+=1
        # st.dataframe(pos)
        return pos

    
    option = st.selectbox(
    'Escolha o grupo a ser visualiado',
    ('Grupo 1', 'Grupo 2', 'Grupo 3', "Grupo 4"))

    st.write('Você selecionou:', option)
    
    if option == 'Grupo 1':
        df=j1
        j=1
        if 'df' not in st.session_state:
            st.session_state.df = df
        
        st.dataframe(st.session_state.df)


        col1,col2 = st.columns(2)      
        with col1:
            jogo_1 = st.button('Jogo-1')
            j=1
        
            if jogo_1:
                j=1
                pos=func(st.session_state.df,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df=st.session_state.df.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df.fillna(0,inplace=True)
                st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df["Pontos"]= st.session_state.df["Pontos"]+st.session_state.df[f"Jogo{j}"]
                st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df.reset_index(drop=True,inplace=True)
                st.session_state.df.index+=1
                st.session_state.df=st.session_state.df[["Nick","Jogo1","Pontos"]]
                st.dataframe(st.session_state.df)
                st.experimental_rerun()
                
        
            
            
        with col2:   
            jogo_2 = st.button('Jogo-2')
            j=2
            if jogo_2:
                pos=func(st.session_state.df,j)
                
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df=st.session_state.df.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df.fillna(0,inplace=True)
                st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df["Pontos"]= st.session_state.df["Pontos"]+st.session_state.df[f"Jogo{j}"]
                st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df.reset_index(drop=True,inplace=True)
                st.session_state.df.index+=1
                st.session_state.df=st.session_state.df[["Nick","Jogo1","Jogo2","Pontos"]]
                st.session_state.df
                st.experimental_rerun()

        with col1:
            jogo_3 = st.button('Jogo-3')
            j=3
            if jogo_3:
                pos=func(st.session_state.df,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df=st.session_state.df.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df.fillna(0,inplace=True)
                st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df["Pontos"]= st.session_state.df["Pontos"]+st.session_state.df[f"Jogo{j}"]
                st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df.reset_index(drop=True,inplace=True)
                st.session_state.df.index+=1
                st.session_state.df=st.session_state.df[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                st.session_state.df
                st.experimental_rerun()

        with col2:
            jogo_4 = st.button('Jogo-4')
            j=4
            if jogo_4:
                pos=func(st.session_state.df,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df=st.session_state.df.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df.fillna(0,inplace=True)
                st.session_state.df.iloc[:,1:]=st.session_state.df.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df["Pontos"]= st.session_state.df["Pontos"]+st.session_state.df[f"Jogo{j}"]
                st.session_state.df.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df.reset_index(drop=True,inplace=True)
                st.session_state.df.index+=1
                st.session_state.df=st.session_state.df[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                st.session_state.df
                st.experimental_rerun()
        
        
        
    elif option =="Grupo 2":
        df=j2
        if 'df2' not in st.session_state:
            st.session_state.df2 = df
        # ss=st.session_state.df2
        st.dataframe(st.session_state.df2)
        j=2

        col1,col2 = st.columns(2)      
        with col1:
            jogo_12 = st.button('Jogo-1')
            j=1
        
            if jogo_12:
                
                pos=func(st.session_state.df2,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df2=st.session_state.df2.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df2.fillna(0,inplace=True)
                st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df2["Pontos"]= st.session_state.df2["Pontos"]+st.session_state.df2[f"Jogo{j}"]
                st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df2.reset_index(drop=True,inplace=True)
                st.session_state.df2.index+=1
                st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Pontos"]]
                st.dataframe(st.session_state.df2)
                st.experimental_rerun()
                
        
            
            
        with col2:   
            jogo_22 = st.button('Jogo-2')
            j=2
            if jogo_22:
                pos=func(st.session_state.df2,j)
                
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df2=st.session_state.df2.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df2.fillna(0,inplace=True)
                st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df2["Pontos"]= st.session_state.df2["Pontos"]+st.session_state.df2[f"Jogo{j}"]
                st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df2.reset_index(drop=True,inplace=True)
                st.session_state.df2.index+=1
                st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Jogo2","Pontos"]]
                st.session_state.df2
                st.experimental_rerun()

        with col1:
            jogo_32 = st.button('Jogo-3')
            j=3
            if jogo_32:
                pos=func(st.session_state.df2,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df2=st.session_state.df2.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df2.fillna(0,inplace=True)
                st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df2["Pontos"]= st.session_state.df2["Pontos"]+st.session_state.df2[f"Jogo{j}"]
                st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df2.reset_index(drop=True,inplace=True)
                st.session_state.df2.index+=1
                st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                st.session_state.df2
                st.experimental_rerun()

        with col2:
            jogo_42 = st.button('Jogo-4')
            j=4
            if jogo_42:
                pos=func(st.session_state.df2,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df2=st.session_state.df2.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df2.fillna(0,inplace=True)
                st.session_state.df2.iloc[:,1:]=st.session_state.df2.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df2["Pontos"]= st.session_state.df2["Pontos"]+st.session_state.df2[f"Jogo{j}"]
                st.session_state.df2.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df2.reset_index(drop=True,inplace=True)
                st.session_state.df2.index+=1
                st.session_state.df2=st.session_state.df2[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                st.session_state.df2
                st.experimental_rerun()



    elif option == "Grupo 3":
        df=j3
        if 'df3' not in st.session_state:
            st.session_state.df3 = df
        st.dataframe(st.session_state.df3)
        j=3

        col1,col2 = st.columns(2)      
        with col1:
            jogo_13 = st.button('Jogo-1')
            j=1
        
            if jogo_13:
                
                pos=func(st.session_state.df3,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df3=st.session_state.df3.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df3.fillna(0,inplace=True)
                st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df3["Pontos"]= st.session_state.df3["Pontos"]+st.session_state.df3[f"Jogo{j}"]
                st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df3.reset_index(drop=True,inplace=True)
                st.session_state.df3.index+=1
                st.session_state.df3=st.session_state.df3[["Nick","Jogo1","Pontos"]]
                st.dataframe(st.session_state.df3)
                st.experimental_rerun()
                
        
            
            
        with col2:   
            jogo_23 = st.button('Jogo-2')
            j=2
            if jogo_23:
                pos=func(st.session_state.df3,j)
                
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df3=st.session_state.df3.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df3.fillna(0,inplace=True)
                st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df3["Pontos"]= st.session_state.df3["Pontos"]+st.session_state.df3[f"Jogo{j}"]
                st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df3.reset_index(drop=True,inplace=True)
                st.session_state.df3.index+=1
                st.session_state.df3=st.session_state.df3[["Nick","Jogo1","Jogo2","Pontos"]]
                st.session_state.df3
                st.experimental_rerun()

        with col1:
            jogo_33 = st.button('Jogo-3')
            j=3
            if jogo_33:
                pos=func(st.session_state.df3,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df3=st.session_state.df3.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df3.fillna(0,inplace=True)
                st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df3["Pontos"]= st.session_state.df3["Pontos"]+st.session_state.df3[f"Jogo{j}"]
                st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df3.reset_index(drop=True,inplace=True)
                st.session_state.df3.index+=1
                st.session_state.df3[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                st.session_state.df3
                st.experimental_rerun()

        with col2:
            jogo_43 = st.button('Jogo-4')
            j=4
            if jogo_43:
                pos=func(st.session_state.df3,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df3=st.session_state.df3.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df3.fillna(0,inplace=True)
                st.session_state.df3.iloc[:,1:]=st.session_state.df3.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df3["Pontos"]= st.session_state.df3["Pontos"]+st.session_state.df3[f"Jogo{j}"]
                st.session_state.df3.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df3.reset_index(drop=True,inplace=True)
                st.session_state.df3.index+=1
                st.session_state.df3[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                st.session_state.df3
                st.experimental_rerun()

    else:
        df=j4
        if 'df4' not in st.session_state:
            st.session_state.df4 = df
        st.dataframe(st.session_state.df4)  
        j=4
        col1,col2 = st.columns(2) 
        with col1:
            jogo_14 = st.button('Jogo-1')
            j=1
        
            if jogo_14:
                
                pos=func(st.session_state.df4,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df4=st.session_state.df4.loc[:,["Nick","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df4.fillna(0,inplace=True)
                st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df4["Pontos"]= st.session_state.df4["Pontos"]+st.session_state.df4[f"Jogo{j}"]
                st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df4.reset_index(drop=True,inplace=True)
                st.session_state.df4.index+=1
                st.session_state.df4=st.session_state.df4[["Nick","Jogo1","Pontos"]]
                st.dataframe(st.session_state.df4)
                st.experimental_rerun()
                
        
            
            
        with col2:   
            jogo_24 = st.button('Jogo-2')
            j=2
            if jogo_24:
                pos=func(st.session_state.df4,j)
                
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df4=st.session_state.df4.loc[:,["Nick","Jogo1","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df4.fillna(0,inplace=True)
                st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df4["Pontos"]= st.session_state.df4["Pontos"]+st.session_state.df4[f"Jogo{j}"]
                st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df4.reset_index(drop=True,inplace=True)
                st.session_state.df4.index+=1
                st.session_state.df4=st.session_state.df4[["Nick","Jogo1","Jogo2","Pontos"]]
                st.session_state.df4
                st.experimental_rerun()

        with col1:
            jogo_34 = st.button('Jogo-3')
            j=3
            if jogo_34:
                pos=func(st.session_state.df4,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df4=st.session_state.df4.loc[:,["Nick","Jogo1","Jogo2","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df4.fillna(0,inplace=True)
                st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df4["Pontos"]= st.session_state.df4["Pontos"]+st.session_state.df4[f"Jogo{j}"]
                st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df4.reset_index(drop=True,inplace=True)
                st.session_state.df4.index+=1
                st.session_state.df4[["Nick","Jogo1","Jogo2","Jogo3","Pontos"]]
                st.session_state.df4
                st.experimental_rerun()

        with col2:
            jogo_44 = st.button('Jogo-4')
            j=4
            if jogo_44:
                pos=func(st.session_state.df4,j)
                tabela_view=tabela_view.merge(pos, on="Nick",how='left')
                tabela_view.fillna(0,inplace=True)
                tabela_view.iloc[:,1:]=tabela_view.iloc[:,1:].astype(int)
                tabela_view["Pontos"]= tabela_view["Pontos"]+tabela_view[f"Jogo{j}"]
                tabela_view.drop(f"Jogo{j}",axis=1,inplace=True)
                tabela_view.sort_values("Pontos",ascending=False,inplace=True)
                tabela_view.reset_index(drop=True,inplace=True)
                tabela_view.index+=1
                tabela_view.to_csv("tabela.csv",index=False)
                st.session_state.df4=st.session_state.df4.loc[:,["Nick","Jogo1","Jogo2","Jogo3","Pontos"]].merge(pos,on='Nick',how='left')
                st.session_state.df4.fillna(0,inplace=True)
                st.session_state.df4.iloc[:,1:]=st.session_state.df4.iloc[:,1:].astype(int)
                # st.session_state.df["Pontos"]=0
                st.session_state.df4["Pontos"]= st.session_state.df4["Pontos"]+st.session_state.df4[f"Jogo{j}"]
                st.session_state.df4.sort_values("Pontos",ascending=False,inplace=True)
                st.session_state.df4.reset_index(drop=True,inplace=True)
                st.session_state.df4.index+=1
                st.session_state.df4[["Nick","Jogo1","Jogo2","Jogo3","Jogo4","Pontos"]]
                st.session_state.df4
                st.experimental_rerun()

    st.write("##")
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

    

    rank=pd.read_csv("tabela.csv")
    rank.index+=1
    st.sidebar.title("Ranking Global")
    st.sidebar.dataframe(rank)    

if __name__ == "__main__":
    partidas()