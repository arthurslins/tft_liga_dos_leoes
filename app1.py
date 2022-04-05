from st_app_sections import inscricao
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

# elif section == 'Otimização':
#     resultados()
# elif section == 'Continuidade':
#     continuidade()
