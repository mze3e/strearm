import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage, auth, db
import pandas as pd
import json
import requests
from components.utils import show_md_content, show_html_content, firebase_config, event_listener
import streamlit.components.v1 as components
import pyrebase

config = {
  "apiKey": "AIzaSyBu_kLxb2bpOh2MbFdjkhBUS6EPV0KwEkE",
  "authDomain": "strearm-mze3e.firebaseapp.com",
  "databaseURL": "https://strearm-mze3e-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "strearm-mze3e.appspot.com"
}

pybase = pyrebase.initialize_app(config)

def app(st):
    #st.title('APP')
    #st.write('This is a simple CRM built on Streamlit. It is a free and open source app framework for Machine Learning and Data Science teams. Create beautiful data apps in hours, not weeks. All in pure Python. All for free. All open source!')
    #show_html_content('navbar', width=1000, height=100)
    show_md_content("markdoc")

    try:
        firebase_app = firebase_admin.get_app()
    except Exception as e:
        print("Initializing firebase app")
        cred = credentials.Certificate(firebase_config())
        firebase_app = firebase_admin.initialize_app(cred , {
            'databaseURL':st.secrets.firebase_db.url,
            })

    st.write(firebase_app.name)

    st.write(firebase_app.options)

    if st.button("Set data to firebase"):
        ref = db.reference("/Books")
        with open("data/books.json", "r") as f:
            file_contents = json.load(f)
        
        ref.set(file_contents)

    if st.button("Set data to firebase using push"):
        ref = db.reference("/Books")
        with open("data/books.json", "r") as f:
            file_contents = json.load(f)
        
        for key, value in file_contents.items():
            ref.push(value)

        #ref.set(file_contents)

    if st.button("Get data from firebase"):
        ref = db.reference("/Books")
        df = pd.DataFrame.from_dict(ref.get(), orient='index')
        st.write(df)

    if st.button("Get data and set firebase"):
        ref = db.reference("/Books")
        st.write(ref.get())

    if st.button("Destroy firebase app"):
        firebase_admin.delete_app(firebase_app)

    if st.button("Set data to firestore"):
        fdb = firestore.client()
        with open("data/books.json", "r") as f:
            file_contents = json.load(f)
        
        for key in file_contents.keys():
            fdb.collection(u'books').document(key).set(file_contents[key])

    if st.button("Set data to firestore using push"):
        fdb = firestore.client()
        with open("data/books.json", "r") as f:
            file_contents = json.load(f)
        
        for key in file_contents.keys():
            fdb.collection(u'books').document(key).set(file_contents[key])

    if st.button("Get data from firestore"):
        fdb = firestore.client()
        
        doc_ref = fdb.collection(u'books')
        doc_ref.get()
        for item in doc_ref.list_documents():
            st.write(item.id)
            st.write(item.get().to_dict())

        # doc_ref = fdb.collection(u'books').document(u'book1')
        # doc = doc_ref.get()
        # st.write(doc.to_dict())

    #db.reference('/Books').listen(event_listener)

    if st.button("Create data using pyrebase"):
        # Get a reference to the auth service
        auth = pybase.auth()
        user = dict()
        user['idToken'] = 'aaklsfdjdklsajf'
        # Get a reference to the database service
        pdb = pybase.database()

        # data to save
        data = {
            "name": "Mortimer 'Morty' Smith"
        }

        # Pass the user's idToken to the push method
        results = pdb.child("users").push(data, user['idToken'])

    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    # import code for encoding urls and generating md5 hashes
    import urllib
    from hashlib import md5
    
    from libgravatar import Gravatar
    from email_decomposer.EmailDecomposer import EmailDecomposer

    # Set your variables here
    #email = "someone@somewhere.com"
    default = "robohash"
    size = 256
    
    if st.button("fetch gravatar"):
        gravatar_url = Gravatar(email).get_image(size=size, default=default)
        st.image(gravatar_url)

        suggested_name = EmailDecomposer().decompose(data=[email])['first_name'][email]
        
        if not suggested_name:
            suggested_name =  EmailDecomposer().decompose(data=[email])['last_name'][email]
        
        if not suggested_name:
            try: 
                if '.' in email.split("@")[0]:
                    suggested_name = email.split("@")[0].split(".")[0].capitalize()
                elif '_' in email.split("@")[0]:
                    suggested_name = email.split("@")[0].split("_")[0].capitalize()
                else:
                    suggested_name = email.split("@")[0].capitalize()
            except:
                suggested_name = email.split("@")[0].capitalize()

        st.write(suggested_name)
    #create_user(email, password, display_name=None, photo_url=gravatar_url_libgravatar, email_verified=False, disabled=False)

    if st.button("Create user using pyrebase"):
        try:
            auth = pybase.auth()
            user = auth.create_user_with_email_and_password(email, password)
            st.write(user)
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "EMAIL_EXISTS":
                print("Email already exists")

    if st.button("SignIn using pyrebase"):
        auth = pybase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        st.write(user)

    if st.button("Refresh token using pyrebase"):
        auth = pybase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        st.write("Original Token")
        st.write(user['idToken'])
        #user = auth.sign_in_with_email_and_password(email, password)
        # before the 1 hour expiry:
        user = auth.refresh(user['refreshToken'])
        # now we have a fresh token
        st.write("Token Refreshed")
        st.write(user['idToken'])