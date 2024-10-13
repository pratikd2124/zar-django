from langchain_groq import ChatGroq
from langchain_fireworks import FireworksEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import  PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader,TextLoader,CSVLoader, UnstructuredFileLoader
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.getenv('firework_api_key')
groq_api_key = os.getenv('groq_api_key')

os.environ["FIREWORKS_API_KEY"] = api_key


# File path
path =  '/home/ubuntu/zar-django/chatbot/info.txt'


# Define the vector embedding function
def vector_embedding():
    textloader = TextLoader(file_path=path)
    docs = textloader.load()

    embeddings = FireworksEmbeddings(
        model="nomic-ai/nomic-embed-text-v1.5",
    )

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs[:250])
    vectors = FAISS.from_documents(final_documents, embeddings)
    return vectors


# Set up your LLM
llm = ChatGroq(groq_api_key=groq_api_key,
               model_name="Llama3-8b-8192")

# Define your prompt template
prompt_template = ChatPromptTemplate.from_template(
    '''You are a professional chatbot assistant for Zar Luxury. Your goal is to provide accurate and concise information to users based on the context provided. 

    Context:
    {context}
    
    User Query:
    {input}
    
    Carefully understand what user want. Please respond with a clear, helpful answer that addresses the user's needs directly and professionally.'''
)
vectors = vector_embedding()
document_chain=create_stuff_documents_chain(llm,prompt_template)

def MainChatbot():

    retriever=vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    return retrieval_chain

