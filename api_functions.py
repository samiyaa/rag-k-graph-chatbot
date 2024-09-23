import pandas as pd
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import re


#function to store file in temp dir and send temp file path
def get_temp_file_path(file):
    temp_dir = tempfile.mkdtemp()
    # Save the uploaded PDF to the temporary directory
    path = os.path.join(temp_dir, file.name)
    with open(path, "wb") as f:
        f.write(file.read())
    return path

#function to process pdf, convert it as docs and return pages
def get_text_from_pdf(file):
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    for page in pages:
        if page.page_content.count('/g') > 3:
            page.page_content = decode(page.page_content)
    
    for page in pages:
        page.metadata['source'] = page.metadata['source'].split('\\')[-1]
    # print(pages[0].metadata['source'])
    return pages


#function to convert cid to char to decode the encoded pdf pages
def cidToChar(cidx):
    return chr(int(re.findall(r'\/g(\d+)',cidx)[0]) + 29)


#function to decode the encoded pdf pages
def decode(sentence):
    sen = ''
    for x in sentence.split('\n'):
        if x != '' and x != '/g3':         # merely to compact the output
            abc = re.findall(r'\/g\d+',x)
            if len(abc) > 0:
                for cid in abc: x=x.replace(cid, cidToChar(cid))
            sen += repr(x).strip("'")
    return re.sub(r'\s+', ' ', sen)
