import streamlit as st
import pandas as pd
import functions as func
from io import StringIO

def get_uploaded_docs():
    return func.get_file_list()

st.title("File Manager 📄")

doc_list = get_uploaded_docs()

#if documents have been uploaded, then display the uploaded files to the user
if doc_list != []:
    with st.expander("Uploaded Files"):
        c = st.columns([3,1])
        with c[0]:
            cont = st.container(height= 150, border= True)
            for doc in doc_list:
                cont.write(doc)
        with c[1]:
            st.page_link("pages/2_chat.py", label= "Initiate Chat", icon = ":material/chat:")

file = st.file_uploader("Upload a file to Chat with", type=["pdf"]) #can be changed to allow more file types, by changing to type=["pdf", "txt", "csv"] etc. 

if file is not None:
    st.toast("File Uploaded Locally")

    if file.name in doc_list:
        st.error("File Already Exists")
    else:
        output = func.call_file_api(file)
        
        if output["status"] == "Success":
            st.toast("File Uploaded to DB")
            st.write('Click the below button to navigate to chat page')
            st.page_link("pages/2_chat.py", label= "Initiate Chat", icon = ":material/chat:")
        else:
            st.error(output["status"])
