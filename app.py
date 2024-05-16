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

KEY=st.secrets['GIGA_KEY']

llm = GigaChat(credentials=KEY, verify_ssl_certs=False)

@st.cache_resource
def load_pipeline():
    with st.spinner('Splitting and getting embeddings...'):
        loader = TextLoader("source.txt")       
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=150,
        )
        documents = text_splitter.split_documents(documents)
        embeddings = GigaChatEmbeddings(credentials=KEY, verify_ssl_certs=False)
        db = Chroma.from_documents(
            documents,
            embeddings,
            client_settings=Settings(anonymized_telemetry=False))
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    st.success('Done')
    return qa_chain

qa_chain = load_pipeline()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    response = qa_chain({"query": prompt})
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write(response['result'])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response['result']})
