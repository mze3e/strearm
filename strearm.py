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
from components.utils import inject_custom_css, get_current_route, get_current_page_key

inject_custom_css('custom.css') 

get_config()

# st.set_page_config(
#     page_title="Ex-stream-ly Cool App",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

invoke_router()


#st.set_page_config(page_title=st.session_state.current_page + ' - ' + "Strearm - The Open Source CRM Built With Streamlit", page_icon="☎", layout="wide", initial_sidebar_state="auto")



#inject_custom_css('navbar.css')
#inject_custom_css('bootstrap-navbar.css')
#navbar_component()
#bootstrap_navbar()

# st.sidebar.title('Navigation')
# st.sidebar.selectbox('Select a page', st.session_state.view_pages_list, key='nav_current_page', on_change=trigger_navigation_event)

##Main Code Starts Here

method_to_run = st.session_state.view_pages_dict[st.session_state.current_page]
module_to_load = st.session_state.views_root + '.' + st.session_state.view_pages_dict[st.session_state.current_page]
module = import_module(module_to_load)
getattr(module, method_to_run)(st)