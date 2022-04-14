import streamlit as st
import pandas as pd



__all__ = ["partidas"]
def grupos():
    j1=pd.read_csv("j1_Rodada-1.csv")
    j2=pd.read_csv("j2_Rodada-1.csv")
    j3=pd.read_csv("j3_Rodada-1.csv")
    j4=pd.read_csv("j4_Rodada-1.csv")
    j5=pd.read_csv("j5_Rodada-1.csv")
    j6=pd.read_csv("j6_Rodada-1.csv")
    j7=pd.read_csv("j7_Rodada-1.csv")

    col1,col2=st.columns(2)
    with col1:
        st.title("Grupo-1")
        st.dataframe(j1)
        st.title("Grupo-3")
        st.dataframe(j3)
        st.title("Grupo-5")
        st.dataframe(j5)
        st.title("Grupo-7")
        st.dataframe(j7)

    with col2:
        st.title("Grupo-2")
        st.dataframe(j2)
        st.title("Grupo-4")
        st.dataframe(j4)
        st.title("Grupo-6")
        st.dataframe(j6)

if __name__ == "__main__":
    grupos()