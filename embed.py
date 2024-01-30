from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import BSHTMLLoader
from langchain.prompts import PromptTemplate
from langchain.chains import VectorDBQA 
import os
import glob

# absolute path to search all text files inside a specific folder
dir_path = r'/Users/j_fel/Desktop/ProfileLLM/html/answer/**/*.html'

os.environ['OPENAI_API_KEY']="sk-111111111111111111111111111111111111111111111111"
os.environ['OPENAI_API_BASE']="http://127.0.0.1:5000/v1"
import openai


# This adds documents from a langchain loader to the database. The customized splitters serve to be able to break at sentence level if required.
def add_documents(loader, instance):
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500, separators= ["\n\n", "\n", ".", ";", ",", " ", ""])
    texts = text_splitter.split_documents(documents)
    print(texts)
    instance.add_documents(texts)

# Create embeddings instance
embeddings = OpenAIEmbeddings()

# Create Chroma instance
instance = Chroma(embedding_function=embeddings, persist_directory="/Users/j_fel/Desktop/ProfileLLM/db")
# instance = FAISS.from_documents(add_documents(),embeddings())
# # add Knowledgebase Dump (CSV file)
# loader = TextLoader("csv file")
# add_documents(loader, instance)

# # add EN sitemap
# loader = SitemapLoader(web_path='')
# add_documents(loader, instance)

# # add EN Blog sitemap, only use English blog posts
# loader = SitemapLoader(web_path='', filter_urls=[""])
# add_documents(loader, instance)

# # add documentation PDFs



pdf_files = [r"C:\Users\j_fel\Desktop\ProfileLLM\pdfFiles\Juan-Felix-Pangestu_CV.pdf", r"C:\Users\j_fel\Desktop\ProfileLLM\pdfFiles\fun facts.pdf"]

for file_name in pdf_files:
    loader = UnstructuredPDFLoader(file_name)
    add_documents(loader, instance)
    time.sleep(10)


# loader= BSHTMLLoader('html/answer/full.htm', open_encoding="utf-8")
# data=loader.load()
# add_documents(loader, instance)




# path to search file
# count=0
# for file in glob.glob(dir_path, recursive=True):
#     count+=1
#     print(file)
#     loader= BSHTMLLoader(file,open_encoding='utf-8')
#     data=loader.load()
#     add_documents(loader, instance)
#     print(count)




# print(instance.similarity_search("",k=1))

instance.persist()
instance = None





