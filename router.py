import streamlit as st

def invoke_router():
    st.session_state.views_root = st.session_state.router_dict['views_root']
    st.session_state.components_root = st.session_state.router_dict['components_root']
    st.session_state.assets_root = st.session_state.router_dict['assets_root']
    st.session_state.content_root = st.session_state.router_dict['content_root']
    
    st.session_state.view_pages_dict = st.session_state.router_dict['view_pages']
    st.session_state.view_pages_list = list(st.session_state.router_dict['view_pages'].keys())
    
    st.session_state.settings_pages_dict = st.session_state.router_dict['settings_pages']
    st.session_state.settings_pages_list = list(st.session_state.router_dict['settings_pages'].keys())    
    
    st.session_state.query_params = st.experimental_get_query_params()

    if 'page' in st.session_state.query_params:
        for key, value in st.session_state.view_pages_dict.items():
            if value == st.session_state.query_params['page'][0]:
                st.session_state.current_page = key
                break

    #Set the current page to the first page in the list
    if 'current_page' in st.session_state:
        st.set_page_config(page_title=st.session_state.current_page + ' - ' + "Strearm - The Open Source CRM Built With Streamlit", page_icon="☎", layout="wide", initial_sidebar_state="auto")
    else:
        st.session_state.current_page = st.session_state.view_pages_list[0]
        st.set_page_config(page_title=st.session_state.current_page + ' - ' + "Strearm - The Open Source CRM Built With Streamlit", page_icon="☎", layout="wide", initial_sidebar_state="auto")
