import requests
import pandas as pd
import os
# from SAP_RAG_API import RAG_api as api
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'SAP_RAG_API')))
import RAG_api as api


#function to get the file content
def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

#function to call the file upload api
def call_file_api(input_data):
    response = api.upload_file(input_data)
    return response

#function to call the chat api
def call_chat_api(query, file_name = None, history = None):
    if file_name == None:
        response = api.process_input(query)
    else:
        response = api.process_input(query, file_name)
    return response

#function to get data from table
def get_table_from_cursor(cursor):
    data = pd.DataFrame(cursor.fetchall())
    header = [i[0] for i in cursor.description]
    data = data.rename(columns=dict(zip(data.columns, header)))
    data = data.convert_dtypes()
    return data


#function to get the answer from the response
def get_source(response):
    ans = response['answer']
    source = ""
    print(response['source_documents'][0].metadata['source'])
    try:
        print(response['source_documents'][0].metadata['source'])
        if os.path.basename(response['source_documents'][0].metadata['source']) != "":
            src = os.path.basename(response['source_documents'][0].metadata['source'])
            source += "\n Document Name: " +src + "  Page No.: " + str(response['source_documents'][0].metadata['page']+1) 
        
            reply = ans + '\n\n' + 'Source: ' +  source
            return reply
    except:
        print('hi')
        return "Sorry There is no relevent Source Document!" + '\n\n' + "Thanks for asking!"
    

#function to call clear data api
def delete_table(filter):
    if filter == None:
        response = api.clear_data()
    else:
        response = api.clear_data(filter)
    return response

def get_file_list():
    x = api.get_file_list()
    return x
