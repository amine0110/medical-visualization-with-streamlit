import streamlit as st
import streamlit.components.v1 as components
from ipywidgets import embed
import vtk
from itkwidgets import view

path_to_file = './samples/volume.nii.gz'

st.set_page_config(page_title='3D Visualization', page_icon=':pill:', layout='wide')

st.subheader('This is Amine :wave:')
st.title("Data Scientist")
st.write("I am a phd student")
st.write("[Visit my Website](https://pycad.co/)")

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