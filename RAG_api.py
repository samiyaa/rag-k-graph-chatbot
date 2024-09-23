from fastapi import FastAPI, File, UploadFile, Form
from huggingface_hub import HfApi
import os
import api_functions as func
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.chat_message_histories import ChatMessageHistory
import tempfile
import pandas as pd
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_experimental.graph_transformers import LLMGraphTransformer

import os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import RetrievalQAWithSourcesChain




# #initiate fastapi as app
app = FastAPI()

#get HuggingFace token from the environment and login to HuggingFace
HF_key = os.environ.get("HF_TOKEN")

HFapi = HfApi(HF_key)

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HF_key, model_name="sentence-transformers/all-MiniLM-l6-v2"
)


url=os.environ.get("neo_url")
username=os.environ.get("neo_username")
password=os.environ.get("neo_pwd")

index_name = "vector"  

neo4j_vector = Neo4jVector.from_existing_index(
    embeddings,
    url=url,
    username=username,
    password=password,
    index_name=index_name,
)


#endpoint to process uploaded file
@app.post("/upload")
def upload_file(file): #get file
    error = 0

    #store file temporarily
    file_path = func.get_temp_file_path(file)
    file_extension = os.path.splitext(file_path)[1]

    if file_extension == ".pdf":
        neo4j_vector.add_documents(func.get_text_from_pdf(file_path))
        #neo4j_vector.persist()
    else:
        error = 1
    
    if error == 0:
        return {"status": "Success", "file_name": file.name}
    else:
        return {"status": "File type not supported"}

# #endpoint to process query and return answer
@app.post("/chat")
def process_input(query, file_name="Temp"): #get query and file name

    #create llm 
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    )

    #create QA chain
    if file_name != "Temp":
        retriever = neo4j_vector.as_retriever(search_kwargs={"k": 2,
        "filter":{"source":{"$like": "%"+file_name+"%"}}})
    else:
        retriever = neo4j_vector.as_retriever(search_kwargs={"k": 2})

    retriever = neo4j_vector.as_retriever()
    
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm, chain_type="stuff", retriever=retriever
    )

    #get answer
    result = chain.invoke({"question": query})
    return result


#endpoint to clear data
@app.post("/clear_data")
def clear_data(filter="None"): # get filter file name

    if filter == "None":
        neo4j_vector.query("""match (n:Chunk) delete n""")

    else:
        neo4j_vector.query(f"""match (n:Chunk) where n.source = '{filter}' delete n""")

    return {"status": "Success"}


def get_file_list():
    x = neo4j_vector.query("""match (n:Chunk) return distinct n.source as source""")
    x = [i['source'] for i in x]
    return x
