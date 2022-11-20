import streamlit as st
import pandas as pd
import numpy as np
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
from config import get_config
from router import invoke_router
from components.utils import navbar_component, inject_custom_css

get_config()
invoke_router()
inject_custom_css('navbar.css')
navbar_component()

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