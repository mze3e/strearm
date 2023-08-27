import base64
#from contextlib import contextmanager, redirect_stdout
#from urllib.parse import quote as urlquote
import os
import streamlit as st
from streamlit.components.v1 import html
import json
import jinja2
import time

#from streamlit_server_state import server, session_info
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

def get_table_download_link(data_frame):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = data_frame.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

def show_md_content(content_md_file, subfolder="", location="content/"):
    """
    in:
    out:
    """
    content_md_file_path = location + subfolder + content_md_file + ".md"

    if os.path.isfile(content_md_file_path):
        with open(content_md_file_path, 'r', encoding="utf-8") as f:
            md_content = f.read()

            if '{&' in md_content:
                content_list = md_content.split('{&')
                second_content_list = []
                st_statements_list = []
                for content in content_list:
                    if '&}' in content:
                        content = content.split('&}')
                        to_print_dict = json.loads(content[0])

                        if 'st.title' in to_print_dict.keys():
                            st.title(to_print_dict['st.title'])
                        if 'st.error' in to_print_dict.keys():
                            st.error(to_print_dict['st.error'])
                        if 'st.warning' in to_print_dict.keys():
                            st.warning(to_print_dict['st.warning'])
                        if 'st.info' in to_print_dict.keys():
                            st.info(to_print_dict['st.info'])
                        if 'st.success' in to_print_dict.keys():
                            st.success(to_print_dict['st.success'])
                        if 'util.display_image' in to_print_dict.keys():
                            image_file_with_ext = to_print_dict['util.display_image']
                            if 'width' in to_print_dict.keys():
                                display_image(image_file_with_ext, width=int(to_print_dict['width']))
                            else:
                                display_image(image_file_with_ext)

                        st.markdown(content[1])
                    else:
                        st.markdown(content)
            else:
                st.markdown(md_content)
    else:
        st.error(f'ERROR: Markdown file not found: {content_md_file_path}')

def show_html_content(content_html_file, subfolder="", location="content/", **xargs):
    """
    in:  
    out: 
    """
    content_html_file_path = location + subfolder + content_html_file + ".html"

    if os.path.isfile(content_html_file_path):
        with open(content_html_file_path, 'r', encoding="utf-8") as file:
            html(file.read(), **xargs)
    else:
        st.error(f'ERROR: HTML file not found: {content_html_file_path}')

def inject_custom_css(css_file_with_ext, subfolder="styles/", location="assets/"):
    css_file_path = location + subfolder + css_file_with_ext
    with open(css_file_path, 'r', encoding="utf-8") as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

def get_current_route():
    try:
        return st.experimental_get_query_params()['page'][0]
    except Exception:
        return None

def set_query_params(**kwargs):
    st.experimental_set_query_params(**kwargs)

def get_current_page_key():
    if get_current_route() is not None:
        for key, value in st.session_state.view_pages_dict.items():
            if value == get_current_route():
                return key
    else:
        return None

def get_current_page_value():
    if get_current_route() is not None:
        for key, value in st.session_state.view_pages_dict.items():
            if value == get_current_route():
                return value
    else:
        return None

def get_current_page_id():
    id = 0
    if get_current_route() is not None:
        for key, value in st.session_state.view_pages_dict.items():
            if value == get_current_route():
                return id
            else:
                id += 1
    else:
        return None

def get_base64_image(image_file_with_ext, subfolder="images/", location="assets/"):
    image_path = location + subfolder + image_file_with_ext
    with open(image_path, 'rb') as file:
        data = file.read()
    
    return base64.b64encode(data)

def display_image(image_file_with_ext, subfolder="images/", location="assets/", width=None, use_column_width=False):
    image_path = location + subfolder + image_file_with_ext 
    if use_column_width == False and width is None:
        st.image(image_path)
    elif use_column_width == True and width is None:
        st.image(image_path, use_column_width="auto")
    else:
        st.image(image_path, width=width)

def display_svg(svg_file_with_ext, subfolder="images/", location="assets/", width=None, use_column_width=False):
    svg_file_path = location + subfolder + svg_file_with_ext
    if os.path.isfile(svg_file_path):
        with open(svg_file_path, 'r') as file:
            svg_string = file.read()

    if use_column_width == False and width is None:
        st.image(svg_string)
    elif use_column_width == True and width is None:
        st.image(svg_string, use_column_width="auto")
    else:
        st.image(svg_string, width=width)

def navbar_component():
    image_as_base64 = get_base64_image("settings.png")

    navbar_items = ''


    for key, value in st.session_state.view_pages_dict.items():
        navbar_items += (f'<a class="navitem" href="/?page={value}">{key}</a>')

    settings_items = ''
    for key, value in st.session_state.settings_pages_dict.items():
        settings_items += (
            f'<a href="/?nav={value}" class="settingsNav">{key}</a>')

    component = rf'''
            <nav class="container navbar" id="navbar">
                <ul class="navlist">
                {navbar_items}
                </ul>
                <div class="dropdown" id="settingsDropDown">
                    <img class="dropbtn" src="data:image/png;base64, {image_as_base64.decode("utf-8")}"/>
                    <div id="myDropdown" class="dropdown-content">
                        {settings_items}
                    </div>
                </div>
            </nav>
            '''
    st.markdown(component, unsafe_allow_html=True)
    js = '''
    <script>
        // navbar elements
        var navigationTabs = window.parent.document.getElementsByClassName("navitem");
        var cleanNavbar = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        
        for (var i = 0; i < navigationTabs.length; i++) {
            cleanNavbar(navigationTabs[i]);
        }
        
        // Dropdown hide / show
        var dropdown = window.parent.document.getElementById("settingsDropDown");
        dropdown.onclick = function() {
            var dropWindow = window.parent.document.getElementById("myDropdown");
            if (dropWindow.style.visibility == "hidden"){
                dropWindow.style.visibility = "visible";
            }else{
                dropWindow.style.visibility = "hidden";
            }
        };
        
        var settingsNavs = window.parent.document.getElementsByClassName("settingsNav");
        var cleanSettings = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        
        for (var i = 0; i < settingsNavs.length; i++) {
            cleanSettings(settingsNavs[i]);
        }
    </script>
    '''
    html(js)

def bootstrap_navbar():
    component = rf'''
    <nav class="navbar navbar-expand-lg bg-light navbar-light ">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Brand</a>

        <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">

            <li class="nav-item">
            <a class="nav-link" href="#">Link</a>
            </li>

            <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-mdb-toggle="dropdown" aria-expanded="false">
                Dropdown
            </a>

            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                <li>
                <a class="dropdown-item" href="#">Action</a>
                </li>
                <li>
                <a class="dropdown-item" href="#">Another action</a>
                </li>
                <li>
                <hr class="dropdown-divider" />
                </li>
                <li>
                <a class="dropdown-item" href="#">Something else here</a>
                </li>
            </ul>
            </li>

        </ul>

        <ul class="navbar-nav d-flex flex-row me-1">
            <li class="nav-item me-3 me-lg-0">
            <a class="nav-link" href="#"><i class="fas fa-shopping-cart"></i></a>
            </li>
            <li class="nav-item me-3 me-lg-0">
            <a class="nav-link" href="#"><i class="fab fa-twitter"></i></a>
            </li>
        </ul>

        <form class="w-auto">
            <input type="search" class="form-control" placeholder="Type query" aria-label="Search">
        </form>

        </div>
    </div>
    </nav>
    '''
    st.markdown(component, unsafe_allow_html=True)

def trigger_navigation_event():
    st.experimental_set_query_params(
        page=st.session_state.view_pages_dict[st.session_state.nav_current_page]
    )

def firebase_config():
    # Load the template json file using jinja2
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    template = env.get_template('firebase.json')

    # Render the template with the project_id value
    return json.loads(template.render(**st.secrets.firebase_credentials), strict=False)

def streamlit_session():
    # The container can host multiple sessions, so we must make sure to select the correct one!
    session_id = get_script_run_ctx().session_id
    session = session_info.get_this_session_info()
    session_headers = session.client.request.headers._dict
    # st.write(session_id)
    # st.write(session_info.get_session_id())
    # st.write(session_headers)
    return session_id, session, session_headers

def event_listener(event):
    print("Received event: ", time.time())
    print("event.event_type: ", event.event_type)  # can be 'put' or 'patch'
    print("event.path: ", event.path)  # relative to the reference, it seems
    print("event.data: ", event.data)  # new data at /reference/event.path. None if deleted