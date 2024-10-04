
import os
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
import streamlit as st
import chromadb
import base64
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Agent:
    def __init__(
        self,  
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu",
        encode_kwargs: dict = {"normalize_embeddings": True},
        llm_model: str = "llama3.2",
        llm_temperature: float = 0.7,
        chroma_client = chromadb.PersistentClient(path="./db"),
        collection_name: str = "chromaVector_db",
    ):
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.llm_model = llm_model
        self.llm_temperature = llm_temperature
        self.chroma_db = chroma_client
        self.collection_name = collection_name

        # Initialize Embeddings
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

        # Initialize Local LLM
        self.llm = ChatOllama(
            model=self.llm_model,
            temperature=self.llm_temperature,
        )

        self.prompt_template = """Use the following pieces of information to answer the user's question.
                            If you don't know the answer, just say that you don't know, don't try to make up an answer.

                            Context: {context}
                            Question: {question}

                            Only return the helpful answer. Answer must be detailed and well explained.
                            Helpful answer:
                            """     
        

        # Initialize the Qdrant vector store
        self.db = Chroma(
            persist_directory="./db", 
            embedding_function=self.embeddings,
            collection_name=self.collection_name 
            )
        
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=['context', 'question']
        )

        # Initialize the retriever
        self.retriever = self.db.as_retriever() 

        # Define chain type kwargs
        self.chain_type_kwargs = {"prompt": self.prompt}

        # Initialize the RetrievalQA chain with return_source_documents=False
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=False,
            chain_type_kwargs=self.chain_type_kwargs,
            verbose=False
        )
    
    def get_dbreqcords(self):
        pass        

    def get_response(self, query: str) -> str:
        """
        Processes the user's query and returns the chatbot's response.

        Args:
            query (str): The user's input question.

        Returns:
            str: The chatbot's response.
        """
        try:
            response = self.qa.invoke(query)
            # print(response)
            return response  # 'response' is now a string containing only the 'result'
        except Exception as e:
            # print(f"⚠️ An error occurred while processing your request: {e}")
            st.error(f"⚠️ An error occurred while processing your request: {e}")
            return "⚠️ Sorry, I couldn't process your request at the moment."
        
class Embedder:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu", # CUDA for GPU
        encode_kwargs: dict = {"normalize_embeddings": True},
        chroma_client = chromadb.PersistentClient(path=r"/db"),
        collection_name: str = "chromaVector_db",
    ):
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.chroma_db = chroma_client
        self.collection_name = collection_name
        
        self.chroma_db.get_or_create_collection(name=self.collection_name)
        
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )
    
    def clear_embeddings(self, id='All'):
        if id == 'All':
            pass
        return "Vector DB has been cleared"

    def create_embeddings(self, pdf_path: str):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The file {pdf_path} does not exist.")

        # Load and preprocess the document
        loader = UnstructuredPDFLoader(pdf_path)
        docs = loader.load()
        if not docs:
            raise ValueError("No documents were loaded from the PDF.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=250
        )
        splits = text_splitter.split_documents(docs)
        if not splits:
            raise ValueError("No text chunks were created from the documents.")

        # Create and store embeddings in Qdrant
        try:
            Chroma.from_documents(
                splits,
                self.embeddings,
                collection_name=self.collection_name,
                persist_directory='./db'
            )
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Qdrant: {e}")

        return "✅ Vector DB Successfully Created and Stored"
        