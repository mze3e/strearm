import streamlit as st
import pandas as pd
import numpy as np
import yaml
import os
import sys
import time
import datetime
import json
import requests
import base64
import io
import re
from importlib import import_module


DEFAULT_CONFIG_FILE_PATH = 'config_default.yml'
CONFIG_FILE_PATH = 'config.yml'
ROUTER_FILE_PATH = 'router.yml'

if os.path.isfile(DEFAULT_CONFIG_FILE_PATH):
    with open(DEFAULT_CONFIG_FILE_PATH, 'r') as stream:
        default_config_dict = yaml.safe_load(stream)
else:
    raise Exception('Default config file not found')

if os.path.isfile(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as stream:
        user_config_dict = yaml.safe_load(stream)
else:
    st.write('No user config file found')

if os.path.isfile(ROUTER_FILE_PATH):
    with open(ROUTER_FILE_PATH, 'r') as stream:
        router_dict = yaml.safe_load(stream)
else:
    st.write('No router file found')

st.session_state.view_pages_dict = router_dict['view_pages']
st.session_state.view_pages_list = router_dict['view_pages'].keys()
st.session_state.views_root = router_dict['views_root']
st.session_state.components_root = router_dict['components_root']
st.session_state.public_root = router_dict['public_root']
st.session_state.query_params = st.experimental_get_query_params()

if 'page' in st.session_state.query_params:
    for key in st.session_state.view_pages_dict.keys():
        if st.session_state.view_pages_dict[key] == st.session_state.query_params['page'][0]:
            st.session_state.current_page = key
            break

#Set the current page to the first page in the list
if 'current_page' in st.session_state:
    st.set_page_config(page_title=st.session_state.current_page + ' - ' + "Strearm - The Open Source CRM Built With Streamlit", page_icon="☎", layout="wide", initial_sidebar_state="auto")
else:
    st.session_state.current_page = st.session_state.view_pages_list[0]
    st.set_page_config(page_title=st.session_state.current_page + ' - ' + "Strearm - The Open Source CRM Built With Streamlit", page_icon="☎", layout="wide", initial_sidebar_state="auto")

def trigger_navigation_event():
    st.experimental_set_query_params(
        page=st.session_state.view_pages_dict[st.session_state.nav_current_page]
    )
st.sidebar.title('Navigation')
st.sidebar.selectbox('Select a page', st.session_state.view_pages_list, key='nav_current_page', on_change=trigger_navigation_event)

##Main Code Starts Here

method_to_run = st.session_state.view_pages_dict[st.session_state.current_page]
module_to_load = st.session_state.views_root + '.' + st.session_state.view_pages_dict[st.session_state.current_page]
module = import_module(module_to_load)
getattr(module, method_to_run)(st)