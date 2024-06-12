import os, sys
sys.path.append(".")
from langchain_community.document_loaders import WebBaseLoader #cargador de documento web
from langchain_community.vectorstores import FAISS #vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter #divisor de texto de caracter recursivo
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from datetime import datetime



#Genera vector
def get_vector_docWeb(system_context):
    #carga variables de entonrno
    load_dotenv()
    #carga el documento:
    loader = WebBaseLoader(system_context)
    docs = loader.load()
    #carga modelo vectorial (embeddings)
    embeddings = OpenAIEmbeddings()
    #inizializa recursiveCgaracterTexto
    text_splitter = RecursiveCharacterTextSplitter()        
    #divide el documento en partes
    documents = text_splitter.split_documents(docs)
    #vectoriza el documento
    vector = FAISS.from_documents(documents, embeddings) #faiss_index
    return vector

#Guardar faiss_index vector
def save_vector_docWeb(vector,path):
    vector.save_local(path)

#Carga faiss_index vector
def load_vector_docWeb(path, embeddings):
    if os.path.exists(path):
        vector = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
        return vector
    else:
        return None

## Cargar el retriever FAISS de disco o crearlo si no existe
def get_persisted_retriever_or_create(system_context, faiss_index):
    # Cargar modelo de embeddings
    embeddings = OpenAIEmbeddings()
    vector = load_vector_docWeb(faiss_index, embeddings)
    if vector is not None:
        print("retorna retriever ya generado")
        return vector.as_retriever()
    else:
        vector = get_vector_docWeb(system_context)
        save_vector_docWeb(vector,faiss_index)
        print("Genera un nuevo retriever")
        return vector.as_retriever()
    
#Genera el nombre de faiss_index
def generate_faiss_index_name_with_url(url):
    # Obtener el nombre base del archivo a partir del dominio de la URL
    nombre_base = url.split('.')[1]  # Obtener el segundo componente del dominio
    # Obtener la fecha y hora actual para hacer el nombre del archivo único
    fecha_actual = datetime.now().strftime("%Y%m%d")
    # Combinar el nombre base con la fecha y hora para obtener el nombre de archivo completo
    nombre_archivo = f"{nombre_base}_{fecha_actual}.faiss"
    return nombre_archivo