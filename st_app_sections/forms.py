import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image




def convert_df(df):
    """
    convert
    """
    return df.to_csv().encode('utf-8')


def forms():

    image = Image.open('assets/Ilustracao_Sem_Titulo.png')
    col1, col2, col3 = st.columns([4,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image,width=250)

    with col3:
        st.write("")
    st.markdown("<h1 style='text-align: center; '>Liga dos Leões</h1>", unsafe_allow_html=True)

  
    
    
    
    st.title("Realize sua inscrição pelo forms:")


    with st.form(key='form1'):
        primeiro_nome=st.text_input("Primeiro nome")
        sobrenome=st.text_input("Sobrenome")
        nick=st.text_input("Nick")
        discord=st.text_input("Discord")

        submit_button = st.form_submit_button(label='Inscreva-se/Ver tabela de inscritos')
    if submit_button:
        
        st.success(f"Inscrição {primeiro_nome} realizada com sucesso")
        st.balloons()


        pagamento = "Não realizado"
        infos=[primeiro_nome,sobrenome,nick,discord,pagamento]
        jogadores=pd.read_csv("jogadores.csv")
        if primeiro_nome:
            
        
            
            
            novos_jogadores =  pd.DataFrame(infos)
            novos_jogadores=novos_jogadores.T.set_axis(["Nome","Sobrenome","Nick","Discord","Pagamento"],axis=1)
            
            jogadores=pd.concat([jogadores,novos_jogadores],ignore_index=True)
            # jogadores=novos_jogadores
            jogadores=jogadores.drop_duplicates(subset=['Nick'], keep='last')
            jogadores=jogadores.drop_duplicates(subset=['Discord'], keep='last')
            jogadores=jogadores.dropna(axis='rows')
            jogadores.index+=1
            jogadores.to_csv("jogadores.csv",index=False)
            st.sidebar.info(f"Quantidade de inscritos: {jogadores.shape[0]}")
            st.sidebar.info(f"Valor arrecadado:  {0}")
        


            
            st.header("Lista de inscritos")
            st.dataframe(jogadores)
            csv = convert_df(jogadores)
            st.download_button(
                    label="Baixar tabela",
                    data=csv,
                    file_name='pagamentos.csv',
                    mime='text/csv'
                    )    
        else:
            jogadores.index+=1
            jogadores.to_csv("jogadores.csv",index=False)
            st.sidebar.info(f"Quantidade de inscritos: {jogadores.shape[0]}")
            st.sidebar.info(f"Valor arrecadado:  {0}")
            st.dataframe(jogadores)
            

    






if __name__=='__main__':
    forms()