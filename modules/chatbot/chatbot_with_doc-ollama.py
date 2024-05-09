from langchain_community.llms import Ollama #modelo ia
from langchain_community.document_loaders import WebBaseLoader #cargador de documento web
from langchain_community.embeddings import OllamaEmbeddings #modelo vectorial
from langchain_community.vectorstores import FAISS #vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter #divisor de texto de caracter recursivo
from langchain.chains.combine_documents import create_stuff_documents_chain  
from langchain_core.prompts import ChatPromptTemplate #prompt de langchain
from langchain.chains import create_retrieval_chain #cadena de recuperacion

def chatBotOllamaWithDocWeb(system_context, user_question):
    #carga el documento:
    loader = WebBaseLoader(system_context)
    docs = loader.load()
    #carga modelo vectorial (embeddings)
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    #modelo llm
    llm = Ollama(model="llama3")
    #inizializa recursiveCgaracterTexto
    text_splitter = RecursiveCharacterTextSplitter()        
    #divide el documento en partes
    documents = text_splitter.split_documents(docs)
    #vectoriza el documento
    vector = FAISS.from_documents(documents, embeddings)
    #restrieve
    retriever = vector.as_retriever()
    #prompt
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")
    #Cree una cadena para pasar una lista de documentos a un modelo.
    document_chain = create_stuff_documents_chain(llm, prompt)
    #Cree una cadena de recuperación que recupere documentos y luego los transmita.
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    #pregunta
    response = retrieval_chain.invoke({"input": user_question})
    #respuesta
    print(response["answer"])

#ejemplo
chatBotOllamaWithDocWeb("https://es.numbeo.com/criminalidad/clasificaciones-por-país", "Chile es un pais seguro?")