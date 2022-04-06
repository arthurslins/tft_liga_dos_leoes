from st_app_sections import forms, apresentacao,regras
from PIL import Image
import streamlit as st



st.sidebar.markdown("<h1 style='text-align: center; '>Liga dos Leões</h1>", unsafe_allow_html=True)
image = Image.open('assets/baixados.jpg')


st.sidebar.image(image)
section = st.sidebar.selectbox(
    "Ir para:",
    (
    'Apresentação do campeonato',
    'Regras',
    'Inscrições'
    )
    )

st.sidebar.write(f"Quantidade de inscritos: {0}")
st.sidebar.write(f"Valor arrecadado:  {0}")
if section == 'Inscrições':
    forms()

elif section == 'Apresentação do campeonato':
    apresentacao()
elif section == 'Regras':
    regras()
