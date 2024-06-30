from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
import pandas as pd


load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
ASTRA_DB_API_ENDPOINT=os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE=os.getenv("ASTRA_DB_KEYSPACE")

embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def ingestdata(status):
    
    vstore = AstraDBVectorStore(
            embedding=embedding,
            collection_name="financebot",
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )
    
    
    storage=status
    
    if storage==None:
        docs = load_file()
        inserted_ids = vstore.add_documents(docs)

    else:
        inserted_ids = None
        return vstore
    return vstore, inserted_ids

if __name__=='__main__':
    vstore,inserted_ids=ingestdata(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound basshead.")
    for res in results:
            print(f"* {res.page_content} [{res.metadata}]")
            
def load_file():
    loader=PyPDFLoader(file_path=r"F:\End_to_End_Projects\LLMOPSTRADINGBOT\data\finance_data.pdf")
    pages = loader.load()
    raw_text = ''
    for i, page in enumerate(pages):
        text=page.page_content
        if text:
            raw_text+=text

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100)

    texts=splitter.split_text(raw_text)
    docs=[]

    for i, text in enumerate(texts):
        doc=Document(page_content=texts[i])
        docs.append(doc)
    return docs