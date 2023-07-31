from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import AzureOpenAI
from dotenv import load_dotenv
import openai
import os
import PyPDF2
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")

OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME = os.getenv("OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME")
OPENAI_ADA_EMBEDDING_MODEL_NAME = os.getenv("OPENAI_ADA_EMBEDDING_MODEL_NAME")

OPENAI_DAVINCI_DEPLOYMENT_NAME = os.getenv("OPENAI_DAVINCI_DEPLOYMENT_NAME")
OPENAI_DAVINCI_MODEL_NAME = os.getenv("OPENAI_DAVINCI_MODEL_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_USER = os.getenv("SQL_USER")
SQL_PWD = os.getenv("SQL_PWD")
SQL_DBNAME = os.getenv("SQL_DBNAME")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

AAD_TENANT_ID = os.getenv("AAD_TENANT_ID")

KUSTO_CLUSTER = os.getenv("KUSTO_CLUSTER")
KUSTO_DATABASE = os.getenv("KUSTO_DATABASE")
KUSTO_TABLE = os.getenv("KUSTO_TABLE")
KUSTO_MANAGED_IDENTITY_APP_ID = os.getenv("KUSTO_MANAGED_IDENTITY_APP_ID")
KUSTO_MANAGED_IDENTITY_SECRET = os.getenv("KUSTO_MANAGED_IDENTITY_SECRET")

COSMOS_MONGO_DB_CONN_STRING = os.getenv("COSMOS_MONGO_DB_CONN_STRING")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

AZURE_COMPUTER_VISION_ENDPOINT = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")
AZURE_COMPUTER_VISION_KEY = os.getenv("AZURE_COMPUTER_VISION_KEY")

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

# Configure OpenAI API
openai.api_type = "azure"
openai.api_version = OPENAI_DEPLOYMENT_VERSION
openai.api_base = OPENAI_DEPLOYMENT_ENDPOINT
openai.api_key = OPENAI_API_KEY

def init_OpenAI(openai_endpoint= OPENAI_DEPLOYMENT_ENDPOINT, deployment_name = OPENAI_DEPLOYMENT_NAME,model_name=OPENAI_MODEL_NAME, model_deployment_version=OPENAI_DEPLOYMENT_VERSION, model_api_key=OPENAI_API_KEY):
    # Configure OpenAI API
    openai.api_type = "azure"
    openai.api_version = model_deployment_version
    openai.api_base = openai_endpoint
    openai.api_key = model_api_key
    return openai

def init_llm(openai_endpoint= OPENAI_DEPLOYMENT_ENDPOINT, deployment_name = OPENAI_DEPLOYMENT_NAME,model_name=OPENAI_MODEL_NAME, model_deployment_version=OPENAI_DEPLOYMENT_VERSION, model_api_key=OPENAI_API_KEY):    
    llm = AzureOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME, 
                model_name=OPENAI_MODEL_NAME, 
                openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT, 
                openai_api_key=OPENAI_API_KEY,
                openai_api_version=OPENAI_DEPLOYMENT_VERSION)
    return llm

def remove_tags(what, from_string):
    pos = from_string.find(what)
    answer = from_string
    if pos > 0:
        answer = from_string[0:pos]
    return answer

def remove_tail_tags(what, from_string):
    pos = from_string.find(what)
    answer = from_string
    if pos > 0:
        answer = from_string[0:pos]
    return answer

def remove_chars(what, from_string):
    answer = from_string.replace(what, "")
    return answer

def start_after_string(what, from_string):
    pos = from_string.find(what)
    answer = from_string
    if pos > 0:
        answer = from_string[pos+len(what):len(from_string)]
    return answer

def init_embeddings():
    embeddings=OpenAIEmbeddings(deployment=OPENAI_ADA_EMBEDDING_DEPLOYMENT_NAME,
                                model=OPENAI_ADA_EMBEDDING_MODEL_NAME,
                                openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT,
                                openai_api_type="azure",
                                chunk_size=1)
    return embeddings


def convertPdf2Txt(fileName, newfileName):
    pdfFileObj = open(fileName, 'rb')
    newFile=open(newfileName,"a")
    reader = PyPDF2.PdfReader(pdfFileObj)
    num_pages = len(reader.pages)
    count = 0
    txt = ""
    text = ""
    while count < num_pages:
        pageObj = reader.pages[count]
        count +=1
        text += pageObj.extract_text()
        if text != "":
            txt = txt + text 
            newFile.writelines(text)
    newFile.close()

def pretty_print_json_string(json_string):
    json_object = json.loads(json_string)
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)
