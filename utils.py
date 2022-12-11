import streamlit as st
from streamlit.legacy_caching.hashing import _CodeHasher
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server
import zipfile
import os
import shutil
import random
import string

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


MAX_SIZE = 300000000 # 300MB


temp_zip_folder = './temp/'
temp_zip_file = temp_zip_folder + 'data.zip'

if not os.path.isdir('./temp'):
    os.makedirs('./temp/')

class SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)

def get_state(hash_funcs=None):
    session = get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = SessionState(session, hash_funcs)

def get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session

def is_zip_oversized(path, max_size=MAX_SIZE):
    if os.path.getsize(path) > max_size:
        return True
    return False

def is_zip_valid(path):
    try:
        check_zip = zipfile.ZipFile(path)
        check_zip.close()
    except:
        st.warning('Not a valid zip file.')
        # clear_data_storage(temp_zip_folder)
        return False
    return True

def does_zip_have_nifti(file):

    with zipfile.ZipFile(file) as zip_ref:
        name_list = zip_ref.namelist()
        for item in name_list:
            if item[-7:] == '.nii.gz':
                return True
    st.warning('Zip folder does not have folders with DICOM files.')
    return False

def clear_data_storage(path):

    if os.path.isfile(path):
        os.remove(path)

    if os.path.isdir(path):
        shutil.rmtree(path)

def store_data(file, temp_data_directory, temporary_location=temp_zip_file):
    
    st.warning('Loading data from zip.')

    with open(temporary_location, 'wb') as out:
        out.write(file.getbuffer())
    
    if is_zip_oversized(temporary_location):
        st.warning('Oversized zip file.')
        # clear_data_storage(temporary_location)
        return False

    with zipfile.ZipFile(temporary_location) as zip_ref:        
        zip_ref.extractall(temp_data_directory + '/')
        st.success('The file is uploaded')
        
    # clear_data_storage(temp_zip_folder)

    return True

