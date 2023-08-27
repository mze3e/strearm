#from auth0_component import login_button
import streamlit as st
#import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader

clientId = r"nmGOu2JaTzzQRnUa4IjId0W42sHm9yuz"
domain = r"7vZuCgEWLM7SnRLlWK9ur2Fndl6BbFKA_2IkcU7TP1NSspArJ4Fsp9EG7WIjYtCe"

def login(st):
    st.title('LOGIN')
    st.write('This is a simple CRM built on Streamlit. It is a free and open source app framework for Machine Learning and Data Science teams. Create beautiful data apps in hours, not weeks. All in pure Python. All for free. All open source!')
    #user_info = login_button(clientId, domain)
    #st.write(user_info)

    with open('data/credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # authenticator = stauth.Authenticate(
    #     config['credentials'],
    #     config['cookie']['name'],
    #     config['cookie']['key'],
    #     config['cookie']['expiry_days'],
    #     config['preauthorized']
    # )

    # name, authentication_status, username = authenticator.login('Login', 'main')

    # if authentication_status:
    #     authenticator.logout('Logout', 'main')
    #     st.write(f'Welcome *{name}*')
    #     st.title('Some content')
    # elif authentication_status == False:
    #     st.error('Username/password is incorrect')
    # elif authentication_status == None:
    #     st.warning('Please enter your username and password')

    # if st.session_state["authentication_status"]:
    #     authenticator.logout('Logout', 'main')
    #     st.write(f'Welcome *{st.session_state["name"]}*')
    #     st.title('Some content')
    # elif st.session_state["authentication_status"] == False:
    #     st.error('Username/password is incorrect')
    # elif st.session_state["authentication_status"] == None:
    #     st.warning('Please enter your username and password')   

    # if authentication_status:
    #     try:
    #         if authenticator.reset_password(username, 'Reset password'):
    #             st.success('Password modified successfully')
    #     except Exception as e:
    #         st.error(e)

    # try:
    #     if authenticator.register_user('Register user', preauthorization=False):
    #         st.success('User registered successfully')
    # except Exception as e:
    #     st.error(e)


    # try:
    #     username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
    #     if username_forgot_pw:
    #         st.success('New password sent securely')
    #         # Random password to be transferred to user securely
    #     elif username_forgot_pw == False:
    #         st.error('Username not found')
    # except Exception as e:
    #     st.error(e)


    # try:
    #     username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
    #     if username_forgot_username:
    #         st.success('Username sent securely')
    #         # Username to be transferred to user securely
    #     elif username_forgot_username == False:
    #         st.error('Email not found')
    # except Exception as e:
    #     st.error(e)

    # if authentication_status:
    #     try:
    #         if authenticator.update_user_details(username, 'Update user details'):
    #             st.success('Entries updated successfully')
    #     except Exception as e:
    #         st.error(e)

    #with open('../config.yaml', 'w') as file:
    #    yaml.dump(config, file, default_flow_style=False)
