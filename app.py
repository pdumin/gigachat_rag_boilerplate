import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_models.gigachat import GigaChat

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain.chains import RetrievalQA
from chromadb.config import Settings

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'file' not in st.session_state:
    st.session_state.file = False

def set_file():
    st.session_state.file = True
    st.session_state.messages = []

def rerun():
    os.remove('src.txt')
    st.rerun()


KEY=st.secrets['GIGA_KEY']



@st.cache_resource
def load_pipeline(uploaded_file):
    if uploaded_file is not None: 
        with open('src.txt', 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.file = True
    with st.spinner('Splitting and getting embeddings...'):
        loader = TextLoader("src.txt")       
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=150,
        )
        llm = GigaChat(credentials=KEY, verify_ssl_certs=False)
        documents = text_splitter.split_documents(documents)
        embeddings = GigaChatEmbeddings(credentials=KEY, verify_ssl_certs=False)
        db = Chroma.from_documents(
            documents,
            embeddings,
            client_settings=Settings(anonymized_telemetry=False))
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    return qa_chain

uploaded_file = st.sidebar.file_uploader(
    'Upload file', 
    type=['txt'], 
    accept_multiple_files=False, 
    on_change=set_file
    )

if st.session_state.file:
    qa_chain = load_pipeline(uploaded_file)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = qa_chain({"query": prompt})
    with st.chat_message("assistant"):
        st.write(response['result'])
    st.session_state.messages.append({"role": "assistant", "content": response['result']})
