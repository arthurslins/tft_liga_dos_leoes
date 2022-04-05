from st_app_sections import inscricao, apresentacao,regras
from PIL import Image
import streamlit as st




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

if section == 'Inscrições':
    inscricao()

elif section == 'Apresentação do campeonato':
    apresentacao()
elif section == 'Regras':
    regras()
