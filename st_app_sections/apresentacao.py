import streamlit as st
from PIL import Image


__all__ = ["apresentacao"]








def apresentacao():
    image = Image.open('assets/Ilustracao_Sem_Titulo.png')
    col1, col2, col3 = st.columns([4,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image,width=250)

    with col3:
        st.write("")
    
    st.markdown("<h1 style='text-align: center; '>Liga dos Leões</h1>", unsafe_allow_html=True)

    st.write("Com o fim do ProLegends, eu aposto que você pensou que não teríamos nada para fazer nessa hiato competitivo do TFT... Mas temos uma solução!")

    st.write("Bem-vindo a 🦁 Liga dos Leões 🦁")

    st.write("Um campeonato em forma de Liga (Pontos Corridos) a fim de fomentar o cenário de TFT nessa reta final de Set 6.5!")

    st.write("Quer entender mais sobre a Liga? Você encontra informações importantes como datas e formato em informações além do regulamento completo em regulamento.")

    st.write("Tem alguma dúvida em relação ao campeonato? Mande em dúvidas")

if __name__ == "__main__":
    apresentacao()
    