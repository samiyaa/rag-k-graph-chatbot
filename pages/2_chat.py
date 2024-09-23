import streamlit as st
import functions as func
import time
import os

st.header("Chat 👾")
    
if st.session_state.messages == []:
    st.session_state.messages.append({"role": "assistant", "content": "Hi, how can I help you?"})

#Clear data
@st.dialog("Are you sure?")
def clear_data_db(file = None):
    c1, c2 = st.columns(2)
    st.write("Are you sure?")
    with c1:
        if st.button("Clear Data"):
            if file == None:
                mess = func.delete_table(None)
            else:
                mess = func.delete_table(file)
            st.rerun()
            return mess

def stream_data():
    for word in response["answer"].split(" "):
        yield word + " "
        time.sleep(0.02)

#initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "file_name" not in st.session_state:
    st.session_state.file_name=""

#Choose which document(s) user wants to chat with
doc_list = func.get_file_list()
all_doc = st.sidebar.toggle("All Documents", )

if all_doc == False:
    file_name = st.sidebar.selectbox("Select Document", doc_list)
    st.session_state.file_name = file_name
    
#Clear Chat
if st.sidebar.button("Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

#Clear Data in Database
if st.sidebar.button("Clear Data in DB", use_container_width=True):
    if all_doc:
        clear_data_db()
    else:
        clear_data_db(file_name)
    
#display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("How can I help?"):
    if prompt.lower() == "clear chat":
        st.session_state.messages = []
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)
        response = func.call_chat_api(prompt, st.session_state.file_name)
        st.chat_message('assistant').write_stream(stream_data)

        st.session_state.messages.append({"role": "assistant", "content": response['answer']})
    st.rerun()
