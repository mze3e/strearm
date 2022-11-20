import os
import streamlit as st
import yaml

DEFAULT_CONFIG_FILE_PATH = 'config_default.yml'
CONFIG_FILE_PATH = 'config.yml'
ROUTER_FILE_PATH = 'router.yml'

def get_config():
    if os.path.isfile(DEFAULT_CONFIG_FILE_PATH):
        with open(DEFAULT_CONFIG_FILE_PATH, 'r') as stream:
            st.session_state.default_config_dict = yaml.safe_load(stream)
    else:
        raise Exception('Default config file not found')

    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as stream:
            st.session_state.user_config_dict = yaml.safe_load(stream)
    else:
        #st.write('No user config file found')
        pass

    if os.path.isfile(ROUTER_FILE_PATH):
        with open(ROUTER_FILE_PATH, 'r') as stream:
            st.session_state.router_dict = yaml.safe_load(stream)
    else:
        st.write('No router file found')