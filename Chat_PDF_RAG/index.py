import streamlit as st
from streamlit import session_state
import time
import base64
import os
from function import Embedder,Agent
from hurry.filesize import size

# -------------------------------------------------------------------------------------------
# Skip ssl validation for Hugging face
import requests
from huggingface_hub import configure_http_backend

def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

configure_http_backend(backend_factory=backend_factory)

# ---------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Chat With Document - RAG",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.session_state['bot_manager'] = Agent()
embeddings_manager = Embedder()

# Initialize session_state variables if not already present
if 'temp_pdf_loc' not in st.session_state:
    st.session_state['temp_pdf_loc'] = None

if 'bot_manager' not in st.session_state:
    st.session_state['bot_manager'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []


# Setup Sidebar
with st.sidebar:
       
    # Navigation Menu
    menu = ["Chat With Me 🤖", "Contact 📧"]
    choice = st.selectbox("Switch Tab", menu)
    st.write("---")

    uploaded_file = st.file_uploader("Upload a Document", type=["pdf"])
    if uploaded_file is not None:
      
        # Save the uploaded file to a temporary location
        temp_pdf_loc = "tempdb.pdf"
        with open(temp_pdf_loc, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Store the temp_pdf_loc in session_state
        st.session_state['temp_pdf_loc'] = temp_pdf_loc
    st.write("---")
    st.header("Embeddings")
    create_embeddings = st.button("Create Embeddings")
    if create_embeddings:
        if st.session_state['temp_pdf_loc'] is None:
            st.warning("⚠️ Please upload a PDF first.")
        else:
            try:
                # Initialize the EmbeddingsManager
                with st.spinner("🔄 Preparing..."):
                    embeddings_manager = Embedder()
                
                with st.spinner("🔄 Embeddings are in process..."):
                    # Create embeddings
                    result = embeddings_manager.create_embeddings(st.session_state['temp_pdf_loc'])
                    time.sleep(1) 
                
                # Initialize the ChatbotManager after embeddings are created
                with st.spinner("🔄 Finalizing..."):
                    if st.session_state['bot_manager'] is None:
                        st.session_state['bot_manager'] =Agent()
                st.success(result)
                
            except FileNotFoundError as fnf_error:
                st.error(fnf_error)
            except ValueError as val_error:
                st.error(val_error)
            except ConnectionError as conn_error:
                st.error(conn_error)
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

if choice == "Chat With Me 🤖":
    st.title("Chat with your Document")
    st.markdown("---")
    
    for msg in st.session_state['messages']:
        st.chat_message(msg['role']).markdown(msg['content'])
    # User input
    if user_input := st.chat_input("Type your message here..."):
        # Display user message
        st.chat_message("user").markdown(user_input)
        st.session_state['messages'].append({"role": "user", "content": user_input})
        with st.spinner("🤖 Responding..."):
            try:
                answer = st.session_state['bot_manager'].get_response(user_input)
                time.sleep(1) 
            except Exception as e:
                answer = f"⚠️ An error occurred while processing your request: {e}"
        
        # Display chatbot message
        st.chat_message("assistant").markdown(answer)
        st.session_state['messages'].append({"role": "assistant", "content": answer})

# Contact Page
elif choice == "Contact 📧":
    st.title("Contact 📬")
    st.markdown("""
    Thanks for here, If you have any feedback, Queries or anything want to say, just send a mail :blush:

    - **Email:** [mechvijaiy@gmail.com](mailto:mechvijaiy@gmail.com) :speech_balloon:

    """)
