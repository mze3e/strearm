import base64
from contextlib import contextmanager, redirect_stdout
from urllib.parse import quote as urlquote
import os
import streamlit as st
from streamlit.components.v1 import html


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'

def show_content(content_md_file, subfolder="", location="content/"):
    content_md_file_path = location + subfolder + content_md_file + ".md"

    if os.path.isfile(content_md_file_path):
        with open(content_md_file_path) as f:
            st.markdown(f.read())
    else:
        st.error(f'ERROR: Markdown file not found: {content_md_file_path}')

def inject_custom_css(css_file_with_ext, subfolder="styles/", location="assets/"):
    css_file_path = location + subfolder + css_file_with_ext
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_current_route():
    try:
        return st.experimental_get_query_params()['page'][0]
    except:
        return None

def get_base64_image(image_file_with_ext, subfolder="images/", location="assets/", width=None, height=None):
    image_path = location + subfolder + image_file_with_ext
    with open(image_path, 'rb') as f:
        data = f.read()
    
    return base64.b64encode(data)


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