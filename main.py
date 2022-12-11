import streamlit as st
import streamlit.components.v1 as components
from ipywidgets import embed
import vtk
from itkwidgets import view
from streamlit_lottie import st_lottie
import requests
from utils import get_state, does_zip_have_nifti, store_data, get_random_string
from glob import glob
import os

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


global temp_data_directory
temp_data_directory = ''



lottie_file = load_lottieurl('https://assets10.lottiefiles.com/private_files/lf30_4FGi6N.json')
state = get_state()
data_key = 'has_data'
data_has_changed = False
 


st.set_page_config(page_title='3D Visualization', page_icon=':pill:', layout='wide')
local_css("style/style.css")
st.title("3D Medical Imaging Visualization")
st.subheader("Upload & Visualize")
st.write("[Visit my Website](https://pycad.co/)")

st_lottie(lottie_file, height=1000, key='coding')

input_path = st.file_uploader('Upload files')

# Upload section
with st.container():
    st.write('---')
    if input_path:
        if not state:
            if does_zip_have_nifti(input_path):
                temp_data_directory = f'./data/{get_random_string(15)}/'
                os.makedirs(temp_data_directory, exist_ok=True)
                store_data(input_path, temp_data_directory)
                data_has_changed = True

st.write("---")
if st.button('Show 3D'):
    path_to_file = glob(f'{temp_data_directory}/*.nii.gz')
    if path_to_file:
        with st.container():
            reader = vtk.vtkNIFTIImageReader()
            reader.SetFileName(path_to_file[0])
            reader.Update()

            view_width = 1800
            view_height = 1600

            snippet = embed.embed_snippet(views=view(reader.GetOutput()))
            html = embed.html_template.format(title="", snippet=snippet)
            components.html(html, width=view_width, height=view_height)

with st.container():
    st.write("---")
    st.header("Get In Touch With Us!")
    st.write("##")

    # Documention: https://formsubmit.co/ 
    contact_form = """
    <form action="https://formsubmit.co/mohammed@pycad.co" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()