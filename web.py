#upload document, delete, and choose
import streamlit as st

st.set_page_config(
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_name" not in st.session_state:
    st.session_state.file_name = "" 

if st.session_state.messages == []:
    st.session_state.messages.append({"role": "assistant", "content": "Hi, how can I help you?"})


pages_dict = {
    "Chat With Docs":
    [
        st.Page("pages/1_upload.py", title = "Upload Documents", icon = ":material/upload_file:", default = True),
        st.Page("pages/2_chat.py", title = "Chat", icon = ":material/chat:"),
    ]
}

pages = st.navigation(pages_dict)
pages.run()
