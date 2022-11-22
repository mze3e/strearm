import streamlit as st

from components.utils import show_md_content, show_html_content
import streamlit.components.v1 as components

def app(st):
    #st.title('APP')
    #st.write('This is a simple CRM built on Streamlit. It is a free and open source app framework for Machine Learning and Data Science teams. Create beautiful data apps in hours, not weeks. All in pure Python. All for free. All open source!')
    #show_html_content('navbar', width=1000, height=100)
    show_md_content("markdoc")
