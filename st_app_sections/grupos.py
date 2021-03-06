import streamlit as st
import pandas as pd
from PIL import Image


__all__ = ["grupos"]
def grupos():


    image = Image.open('assets/Ilustracao_Sem_Titulo.png')
    col1, col2, col3 = st.columns([3,5.5,1])
    with col1:
        st.write("")

    with col2:
        st.image(image,width=250)

    with col3:
        st.write("")
    st.markdown("<h1 style='text-align: center; '>Liga dos Leões</h1>", unsafe_allow_html=True)

    
    j1=pd.read_csv("Rodada10_g1.csv")
    j1.index+=1
    j2=pd.read_csv("Rodada10_g2.csv")
    j2.index+=1
    j3=pd.read_csv("Rodada10_g3.csv")
    j3.index+=1
    # j4=pd.read_csv("Rodada10_g4.csv")
    # j4.index+=1
    # j5=pd.read_csv("Rodada8_g5.csv")
    # j5.index+=1
    # j6=pd.read_csv("Rodada6_g6.csv")
    # j6.index+=1
    # j7=pd.read_csv("Rodada4_g7.csv")
    # j7.index+=1

    col1,col2=st.columns(2)
    with col1:
        st.title("Grupo-1")
        st.write(f"O jogador a criar o lobby será: {j1.iloc[0,1]}")
        
        st.dataframe(j1.iloc[:,1])
        st.title("Grupo-3")
        st.write(f"O jogador a criar o lobby será: {j3.iloc[0,1]}")
        st.dataframe(j3.iloc[:,1])
        st.title("Grupo-5")
        # st.write(f"O jogador a criar o lobby será: {j5.iloc[0,1]}")
        # st.dataframe(j5.iloc[:,1])
        # st.title("Grupo-7")
        # st.write(f"O jogador a criar o lobby será: {j7.iloc[0,1]}")
        # st.dataframe(j7.iloc[:,1])

    with col2:
        st.title("Grupo-2")
        st.write(f"O jogador a criar o lobby será: {j2.iloc[0,1]}")
        st.dataframe(j2.iloc[:,1])
        # st.title("Grupo-4")
        # st.write(f"O jogador a criar o lobby será: {j4.iloc[0,1]}")
        # st.dataframe(j4.iloc[:,1])
        # st.title("Grupo-6")
        # st.write(f"O jogador a criar o lobby será: {j6.iloc[0,1]}")
        # st.dataframe(j6.iloc[:,1])

if __name__ == "__main__":
    grupos()