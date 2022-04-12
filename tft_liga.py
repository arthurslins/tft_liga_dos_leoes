from st_app_sections import forms, apresentacao,regras,partidas
import pandas as pd
from PIL import Image
import streamlit as st

import base64

from tft_liga_dos_leoes.st_app_sections import partidas2


st.set_page_config(layout="wide")
base= "dark"



st.sidebar.markdown("<h1 style='text-align: center; '>Liga dos Leões</h1>", unsafe_allow_html=True)
image = Image.open('assets/baixados.jpg')


st.sidebar.image(image)
section = st.sidebar.selectbox(
    "Ir para:",
    (
    'Apresentação do campeonato',
    'Regras',
    "Partidas"
    )
    )
jogadores=pd.read_csv("jogadores.csv")

# if section == 'Inscrições':
#     forms()

if section == 'Apresentação do campeonato':
    apresentacao()
elif section == 'Regras':
    regras()
elif section == "Partidas":
    partidas()
