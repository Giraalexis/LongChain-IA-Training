import sys
sys.path.append(".")
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder #permite añadir un listado de menajes en el prompt
from langchain.chains import create_retrieval_chain #cadena de recuperacion
from langchain.chains.combine_documents import create_stuff_documents_chain 
from dotenv import load_dotenv
from modules.retriever.retriever import get_persisted_retriever_or_create, generate_faiss_index_name_with_url

async def chatbot_gen_dicionary_openia(system_context,user_question,chat_history):

    #api key
    load_dotenv()
    #model
    model = ChatOpenAI()
    #Genera un nombre para el faiss_index
    faiss_index = generate_faiss_index_name_with_url(system_context)
    #retriever, carga si ya existe local o crea uno nuevo
    retriever = get_persisted_retriever_or_create(system_context, "modules/retriever/faiss_index/"+faiss_index)
    #Ejemplo estructura
    estructura_ejemplo = '''[{"fecha": '2023-01-01', "ventas": 100}, {"fecha": "2023-01-02", "ventas": 150}]'''
    #prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Utiliza el siguiente contexto y el historial de chat para generar la estructura de datos solicitada por el usuario."),
        ("system", "Si el usuario pide generar un gráfico o una tabla, convierte la información en un diccionario adecuado que represente los datos en el formato solicitado."),
        ("system", "La respuesta debe ser exclusivamente una lista de diccionarios, sin incluir texto adicional."),
        ("system", "La estructura de salida esperada debe seguir el siguiente ejemplo: {estructura_ejemplo}."),
        ("system", "No incluyas el prefijo de formato como 'python' o 'json' en la respuesta."),
        ("system", "contexto:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    #Cree una cadena para pasar una lista de documentos a un modelo.
    document_chain = create_stuff_documents_chain(model, prompt)
    #Cree una cadena de recuperación que recupere documentos y luego los transmita.
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    

    response = retrieval_chain.invoke({
        "estructura_ejemplo": estructura_ejemplo,
        "system_context": system_context,
        "chat_history": chat_history,
        "input": user_question
    })
    #respuesta
    print(response["answer"])
    return response["answer"]

#chatbot_openia("definicion corta","gatos")

#res = chatbot_gen_dicionary_openia("https://www.meteored.cl/tiempo-en_Catemu-America+Sur-Chile-Valparaiso--1-518287.html","Genera una tabla comparativa entre dias y temperatura",["chat_history"])
#print(res['answer'])