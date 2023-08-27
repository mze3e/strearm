import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage, auth, db

try:
    firebase_app = firebase_admin.get_app()
except Exception as e:
    print("Initializing firebase app")
    cred = credentials.Certificate(firebase_config())
    firebase_app = firebase_admin.initialize_app(cred , {
        'databaseURL':st.secrets.firebase_db.url,
        })

st.write(firebase_app.name)



st.title('WIP: Streamlit app + Firestore real-time listener')


if 'change_detected' not in st.session_state:


    # Flag to know inside the Streamlit app session if change was detected or not yet.
    st.session_state.change_detected = False


    # Declare name of document to listen to, also name of collection it belongs to.
    col_name = 'example_collection'
    doc_name = 'example_document'


    # Create threading.Event that will make Thread wait at "callback_done.wait()" until condition is met.
    import threading
    callback_done = threading.Event()


    # Put the firestore listener + Event in a target function so they can run inside a background Thread in a Streamlit app.
    def listener_thread_target(col_name:str, doc_name:str):


        # Snapshot function that goes inside firestore listener, which listens for any change in document and does "callback_done.set()" when a change is detected.
        def on_snapshot(doc_snapshot, changes, read_time):
            if changes[0].type.name == 'MODIFIED':
                callback_done.set()


        # Create the firestore listener for the given document name (doc_name). 
        doc_watch = db.collection(col_name).document(doc_name).on_snapshot(on_snapshot)

        # Background thread is forced to wait here until the condition inside listener is met and "callback_done.set()" happens.
        callback_done.wait()

        # From here until the end of listener_thread_target, everything the background Thread will do once "callback_done.set()" happens:

        # Set to True the session state variable that tracks change.
        st.session_state.change_detected = True

        ######################################################################
        #
        # NOT WORKING - unsubscribe the firestore listener so it stops running.
        doc_watch.unsubscribe()        
        #
        # NOT WORKING - force rerun to see the change without having to refresh app manually.
        # st.experimental_rerun()
        #
        ######################################################################

    # Create a background Thread that has the listener_thread_target as target.
    from streamlit.runtime.scriptrunner import add_script_run_ctx
    listener_thread = threading.Thread(target=listener_thread_target,args=(col_name,doc_name))

    # Add the session context to the background Thread.
    add_script_run_ctx(listener_thread)

    # Start the background Thread.
    listener_thread.start()


# See in the app if the change was detected or not.
st.write(st.session_state.change_detected)

# Button to refresh app manually.
st.button('Naive refresh button')