import streamlit as st
import streamlit.components.v1 as components
from ipywidgets import embed
import vtk
from itkwidgets import view
from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

path_to_file = './samples/volume.nii.gz'
lottie_file = load_lottieurl('https://assets10.lottiefiles.com/private_files/lf30_4FGi6N.json')

st.set_page_config(page_title='3D Visualization', page_icon=':pill:', layout='wide')

st.subheader('This is Amine :wave:')
st.title("Data Scientist")
st.write("I am a phd student")
st.write("[Visit my Website](https://pycad.co/)")

st_lottie(lottie_file, height=1000, key='coding')

if st.button('Show 3D'):
    with st.container():
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(path_to_file)
        reader.Update()

        view_width = 1800
        view_height = 1600

        snippet = embed.embed_snippet(views=view(reader.GetOutput()))
        html = embed.html_template.format(title="", snippet=snippet)
        components.html(html, width=view_width, height=view_height)

