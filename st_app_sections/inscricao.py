from operator import index
# from matplotlib.pyplot import pause
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


__all__ = ["inscricao"]

def convert_df(df):
    """
    convert
    """
    return df.to_csv().encode('utf-8')
def seinscrever(jogadores):
        
    novos_jogadores=[]
    agree = st.checkbox('Tenho certeza que digitei tudo corretamente')
    novos_jogadores=st.text_input("Insira seu nome, nick e discord separado por virgulas (Nome, Nick, Discord)")
    
    # st.warning('Por favor insira as informações.')
   
    if agree:
               
        st.success('Parabéns inscrição feita com sucesso.')
        st.balloons()
        novos_jogadores=novos_jogadores.split(",")
        jogadores.loc[len(jogadores)] = np.array(novos_jogadores)
        jogadores.to_csv("jogadores.csv",index=False)
    else:
        st.warning("Confira seu cadastro e marque a checkbox se estiver tudo ok")
        
    return jogadores



def inscricao():
    image = Image.open('assets/Ilustracao_Sem_Titulo.png')
    col1, col2, col3 = st.columns([4,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image,width=250)

    with col3:
        st.write("")
    st.markdown("<h1 style='text-align: center; '>TFT CAMP</h1>", unsafe_allow_html=True)
    st.header("Lista de inscritos")
           
    jogadores=pd.read_csv("jogadores.csv")
    # jogadores=jogadores.drop_duplicates(subset=['Nome'], keep='last')
    jogadores=jogadores.drop_duplicates(subset=['Nick'], keep='last')
    jogadores=jogadores.drop_duplicates(subset=['Discord'], keep='last')
    jogadores.reset_index(drop=True,inplace=True)
    jogadores.index+=1
    # jogadores["Pagamento confirmado"]=0  
    st.dataframe(jogadores)
    st.header("Realize sua inscrição")
    df=seinscrever(jogadores)
    df=df.drop_duplicates(subset=['Nome'], keep='last')
    df=df.drop_duplicates(subset=['Nick'], keep='last')
    df=df.drop_duplicates(subset=['Discord'], keep='last')
    df.reset_index(drop=True,inplace=True)
    df.index+=1
    # df["Pagamento confirmado"]=0
    
    df_pag=df
    df_pag["Pagamento"]=0    
    view_df1, view_df2 = st.columns(2)
    view_df1.dataframe(df)
    
    view_df2.dataframe(df_pag.iloc[:,-1])


    csv = convert_df(df_pag)

    # st.download_button(
    #                     label="Baixar tabela de inscritos",
    #                     data=df,
    #                     file_name='inscritos.csv',
    #                     mime='text/csv'
    #                 )    
    
    st.download_button(
                    label="Baixar tabela",
                    data=csv,
                    file_name='pagamentos.csv',
                    mime='text/csv'
                )    
  
if __name__ == "__main__":
    inscricao()

    



