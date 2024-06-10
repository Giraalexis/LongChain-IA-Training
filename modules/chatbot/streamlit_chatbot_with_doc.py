import streamlit as st
import requests
from langchain_core.messages import HumanMessage, AIMessage #mensaje tipo humano e ia


url_chatbot= "http://127.0.0.1:8000/chatbot_openia_with_doc" #contexto doc

st.title("CHATBOT WITH DOC WEB")

#define el doc page, mantiene en top page
container = st.container()
with container:
    contextoWeb = st.text_input("Pagina Web:")


#ipregunta del usuario hacerca del doc page
pregunta = st.chat_input("Pregunta: ")


#inizializa chat history streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

#inizializa chat history streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#muestra chat history streamlit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = {
"input_context": contextoWeb,
"input_question": pregunta,
"chat_history": st.session_state.chat_history
}

if pregunta and contextoWeb:
    with st.chat_message("user"):
        st.markdown(pregunta)
        st.session_state.messages.append({"role": "user", "content": pregunta}) #se guarda chat_history para streamlit
        st.session_state.chat_history.append(pregunta) #se guarda chat_history para chatbot
    response = requests.post(url_chatbot, json = question)
    if response.status_code == 200:
        with st.chat_message("ai"):
            st.markdown(response.json()['answer'])
            st.session_state.messages.append({"role": "ai", "content": response.json()['answer']}) #se guarda chat_history para streamlit
            st.session_state.chat_history.append(response.json()['answer']) #se guarda chat_history para chatbot
    else:
        with st.chat_message("assistant"):
            st.markdown("Error de servidor, intenta nuevamente")
    print(st.session_state.chat_history) #para chatbot
    print(st.session_state.messages) 




