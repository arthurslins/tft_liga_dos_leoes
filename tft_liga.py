from st_app_sections import forms, apresentacao,regras
import pandas as pd
from PIL import Image
import streamlit as st

import base64

# @st.cache(allow_output_mutation=True)
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def set_png_as_page_bg(png_file):
#     bin_str = get_base64_of_bin_file(png_file) 
#     page_bg_img = '''
#     <style>
#     .stApp {
    
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     background-repeat: no-repeat;
#     background-attachment: scroll; # doesn't work
    
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)
    
#     return

# def set_png_as_page_bg2(png_file):
#     bin_str = get_base64_of_bin_file(png_file) 
#     page_bg_img = '''
#     <style>
#     .stApp {

#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     background-repeat: no-repeat;
#     background-attachment: scroll; # doesn't work

#     }
#     </style>
#     ''' % bin_str
    
#     st.sidebar.markdown(page_bg_img, unsafe_allow_html=True)
#     return

# set_png_as_page_bg('the-best-top-desktop-hd-dark-black-wallpapers-dark-black-wallpaper-dark-background-dark-wallpaper-23.webp')
# set_png_as_page_bg2('the-best-top-desktop-hd-dark-black-wallpapers-dark-black-wallpaper-dark-background-dark-wallpaper-23.webp')

main_bg = "the-best-top-desktop-hd-dark-black-wallpapers-dark-black-wallpaper-dark-background-dark-wallpaper-23.webp"
main_bg_ext = "webp"

side_bg = "the-best-top-desktop-hd-dark-black-wallpapers-dark-black-wallpaper-dark-background-dark-wallpaper-23.webp"
side_bg_ext = "webp"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .css-ffhzg2 {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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
jogadores=pd.read_csv("jogadores.csv")
st.sidebar.info(f"Quantidade de inscritos: {jogadores.shape[0]}")
st.sidebar.info(f"Valor arrecadado:  {0}")
if section == 'Inscrições':
    forms()

elif section == 'Apresentação do campeonato':
    apresentacao()
elif section == 'Regras':
    regras()
