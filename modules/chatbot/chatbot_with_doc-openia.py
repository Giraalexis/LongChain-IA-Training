from langchain_community.llms import Ollama #modelo ia
from langchain_community.document_loaders import WebBaseLoader #cargador de documento web
from langchain_community.embeddings import OllamaEmbeddings #modelo vectorial
from langchain_community.vectorstores import FAISS #vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter #divisor de texto de caracter recursivo
from langchain.chains.combine_documents import create_stuff_documents_chain  
from langchain_core.prompts import ChatPromptTemplate #prompt de langchain
from langchain.chains import create_retrieval_chain #cadena de recuperacion
from langchain_core.prompts import MessagesPlaceholder #permite añadir un listado de menajes en el prompt
from langchain_core.messages import HumanMessage, AIMessage #mensaje tipo humano e ia
from deep_translator import GoogleTranslator #traductor de idiomas
import asyncio # permite ejecutar async
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import json
from langchain_openai import OpenAIEmbeddings

#splitter: divide el documento en partes
#Embedding: transforma las partes del documento en vectores
#Retriver: busca y recupera fragmentos importantes para responder consultas del usuario


def chatBotOllamaWithDocWeb(system_context):
    key = json.load(open('./utils/api_key.json', encoding='utf-8'))
    #carga el documento:
    loader = WebBaseLoader(system_context)
    docs = loader.load()
    #carga modelo vectorial (embeddings)
    embeddings = OpenAIEmbeddings(api_key=key["API_KEY"]["OPEN_IA"])
    #modelo llm
    llm = ChatOpenAI(api_key=key["API_KEY"]["OPEN_IA"])
    #inizializa recursiveCgaracterTexto
    text_splitter = RecursiveCharacterTextSplitter()        
    #divide el documento en partes
    documents = text_splitter.split_documents(docs)
    #vectoriza el documento
    vector = FAISS.from_documents(documents, embeddings)
    #retriever
    retriever = vector.as_retriever()
    #chat_history
    chat_history = []
    #prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Responde la pregunta con el idioma en el cual se pregunta"),
        ("system", "Responde la pregunta segun el siguiente context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    #Cree una cadena para pasar una lista de documentos a un modelo.
    document_chain = create_stuff_documents_chain(llm, prompt)
    #Cree una cadena de recuperación que recupere documentos y luego los transmita.
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    

    #CONVERACION CONTINUA
    while True:

        #user question
        user_question = input("\nPregunta: ")

        #condicion de salida while
        if user_question.upper() in ['EXIT','SALIR'] :
            print("FIN CONVERACION")
            break

        #Stream
        response = ""
        for chunk in (retrieval_chain.stream({
        "chat_history": chat_history,
        "input": user_question
        })):
            
            if 'answer' not in chunk:
                continue
            else:
                print(chunk['answer'], end='', flush=True)
                response += chunk['answer']
          
        #se guarda el chat_history
        chat_history.append(HumanMessage(content=user_question))
        chat_history.append(AIMessage(content=response))
            
    



#ejemplo
chatBotOllamaWithDocWeb("https://es.numbeo.com/criminalidad/clasificaciones-por-país")  