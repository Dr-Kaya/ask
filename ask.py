#import libraries
import streamlit as st
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

#generate response function
def generate_response(uploaded_file, openai_api_key, query_text):
    #Load document if file is uploaded
    if uploaded_file is not None:
        documents = [uploaded_file.read().decode("utf-8")]
    
    #split documents into chinks
    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap=0)
    texts = text_splitter.create_documents(documents)

    #select embeeddings
    embeddings = OPENAIEmbeddings(openai_api_key = openai_api_key)

    #Create a vectorscore from documents
    db = Chroma.from_documents(texts, embeddings)

    #create a retriever interface
    retriever = db.as_retriever()

    #Create QA chain
    qa = RetrievalQA.from_chain_type(llm = OpenAI(openai_api_key = openai_api_key), chain_type = 'stuff', retriever = retriever)

    return qa.run(query_text)

#Page Title
st.set_page_config(page_title = 'Ask the Document App')
st.title('Ask the Doc Application')

#file upload
uploaded_file = st.file_uploader('Upload an article', type = 'txt')

#Query text
query_text = st.text_input('Enter your question:', placeholder = 'Please provide a short summary', disabled = not uploaded_file)

#Form Input and Query
result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = st.text_input('Enter your OpenAI API Key:', type = 'password', disabled = not (uploaded_file and query_text))
    submitted = st.form_submit_button('Submit', disabled = not (uploaded_file and query_text))
    if submitted and openai_api_key.startswith('sk-'):
        response = generate_response(uploaded_file, openai_api_key, query_text)
        result.append(response)
        del openai_api_key

if len(result):
    st.info(response)
