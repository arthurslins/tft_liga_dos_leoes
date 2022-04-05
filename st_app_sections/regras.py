from markdown import markdown
import streamlit as st
from PIL import Image



__all__ = ["regras"]





def regras():


    image = Image.open('assets/Ilustracao_Sem_Titulo.png')
    col1, col2, col3 = st.columns([4,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(image,width=250)

    with col3:
        st.write("")
    st.markdown("<h1 style='text-align: center;'>Informações da Liga</h1>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>🦁 Formato da Liga 🦁</h1>", unsafe_allow_html=True)

    st.markdown("""
    A Liga dos Leões será composta de 12 rodadas MD4 em modelo suíço, onde o primeiro dia terá SEED aleatória.""") 
    st.write(""" A liga também terá o sistema de escalada, onde haverão eliminações dos 8 menos pontuados a cada X semanas (A validar pelo número de inscritos).""")

    st.markdown("""
    ### Exemplo: """)

    st.markdown("""
        * Se 32 inscritos, a cada 4 rodadas os 8 que menos pontuarem serão eliminados
        * Se 64 inscritos, a cada 3 rodadas os 8 que menos pontuarem serão eliminados """)

    st.write("A final ocorrerá em uma MD6 com os 8 melhores da fase de pontos corridos. O fator desempate da final será a colocação obtida ao final das 12 md4.") 
    
    st.markdown("""
    ### ❗Pontuação de Partidas❗ """)

    st.write("A Liga dos Leões utilizará a pontuação padrão de campeonatos, onde:" )


    st.markdown("""
    * TOP 1 - 10 pts.
    * TOP 2 - 8 pts.
    * TOP 3 - 7 pts.
    * TOP 4 - 6 pts.
    * TOP 5 - 4 pts.
    * TOP 6 - 3 pts.
    * TOP 7 - 2 pts.
    * TOP 8 - 1 pt. """)


    st.markdown("""
    ### 📅 Datas da Liga 📅""")

    st.write(""" A Liga dos Leões ocorrerá toda segunda e quinta, às 19h, a partir do dia 14 de abril.""")

    st.markdown("""
    * Round 1:  MD4 - 14 de abril (QUI) às 19h
    * Round 2:  MD4 - 18 de abril (SEG) às 19h
    * Round 3:  MD4 - 21 de abril (QUI) às 19h
    * Round 4:  MD4 - 25 de abril (SEG) às 19h
    * Round 5:  MD4 - 28 de abril (QUI) às 19h
    * Round 6:  MD4 - 2 de maio   (SEG) às 19h
    * Round 7:  MD4 - 5 de maio   (QUI) às 19h
    * Round 8:  MD4 - 9 de maio   (SEG) às 19h
    * Round 9:  MD4 - 12 de maio  (QUI) às 19h
    * Round 10: MD4 - 16 de maio  (SEG) às 19h
    * Round 11: MD4 - 19 de maio  (QUI) às 19h
    * Round 12: MD4 - 23 de maio  (SEG) às 19h

    * FINAL: MD6 - A definir""")

if __name__ == "__main__":
    regras()