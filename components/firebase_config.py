import jinja2
import streamlit as st


class firebase_config:
    """This component allows you to configure your Firebase project credentials in Streamlit."""

    def __init__(self):
        # Load the template json file using jinja2
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        template = env.get_template('firebase.json')

        # Render the template with the project_id value
        self.config_json = template.render(**st.secrets.firebase_credentials)

    def get_config(self):
        return self.config_json