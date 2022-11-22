import streamlit as st
from st_on_hover_tabs import on_hover_tabs as navigation_tabs
from components.utils import inject_custom_css
from components.utils import get_current_route, get_current_page_key, set_query_params, get_current_page_id, get_current_page_value, display_svg

def set_session_state():
    st.session_state.views_root = st.session_state.router_dict['views_root']
    st.session_state.components_root = st.session_state.router_dict['components_root']
    st.session_state.assets_root = st.session_state.router_dict['assets_root']
    st.session_state.content_root = st.session_state.router_dict['content_root']

    st.session_state.view_pages_dict = st.session_state.router_dict['view_pages']
    st.session_state.view_pages_list = list(st.session_state.router_dict['view_pages'].keys())
    st.session_state.view_icons_dict = st.session_state.router_dict['view_icons']

    for key in st.session_state.view_pages_dict.keys(): #setting default icons if icon is not configured
        try:
            test_value = st.session_state.view_icons_dict[key]
        except Exception:
            st.session_state.view_icons_dict[key] = 'double_arrow'

    st.session_state.view_icons_list = list(st.session_state.view_icons_dict.values())

    st.session_state.settings_pages_dict = st.session_state.router_dict['settings_pages']
    st.session_state.settings_pages_list = list(st.session_state.router_dict['settings_pages'].keys())

def invoke_router():
    set_session_state()

    inject_custom_css('st-on-hover-tabs.css') 

    st.session_state.query_params = st.experimental_get_query_params()

    if get_current_page_id() is not None: #initial load
        st.session_state.current_page = get_current_page_key()
        tab_key = get_current_page_id()
    else:
        st.session_state.current_page = st.session_state.view_pages_list[0]
        tab_key = 0

    with st.sidebar:
        col1, col2, col3 = st.columns(3)
        with col2:
            display_svg('generic-avatar.svg', use_column_width=True)

        tabs = navigation_tabs(tabName=st.session_state.view_pages_list, 
                             iconName=st.session_state.view_icons_list,
                             styles = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabOptionsStyle': {':hover :hover': {'color': 'red',
                                                                      'cursor': 'pointer'}},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'}},
                             default_choice=tab_key,
                             key="tab_choice")

    if tabs in st.session_state.view_pages_list: #set query params to the clicked navigation tab
        set_query_params(
            page=st.session_state.view_pages_dict[tabs]
            )    

    st.session_state.current_page = get_current_page_key()


    header_text = """<p style="line-height: 45px; font-size: 20px; text-align: center;">THIS IS A TEST</p>"""