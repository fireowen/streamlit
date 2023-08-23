from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
import langchain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

# load environment variables
load_dotenv()
# set title of app
st.set_page_config(page_title="AskOwen")
st.header("AskOwen")

# upload the file
pdf = st.file_uploader("Upload your PDF", type="pdf")

# extract the text
if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # split into chunks
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1500, chunk_overlap=250, length_function=len)
    chunks = text_splitter.split_text(text)

    # create embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = Chroma.from_texts(texts=chunks, embedding=embeddings)

    # show user input
    user_question = st.text_input("Ask a query about the document:")
    if user_question:
        docs = knowledge_base.similarity_search(user_question)

        # language model and query
        llm = OpenAI(model_name="text-davinci-003", max_tokens=4096, temperature=0, n=50)
        chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=user_question)
            print(cb)
        st.write(response)