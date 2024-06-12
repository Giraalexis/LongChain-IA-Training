import streamlit as st
import requests

url_chatbot= "http://127.0.0.1:8001/chatbot_openia_with_doc" #contexto doc

st.title("CHATBOT WITH DOC WEB")

#inizializa contextoWeb y retriever
    #si es nuevo lo guarda y genera retriever
    #si es diferente, actualiza contextoWeb y retriever
    #Si es el mismo, no hace nada
contextoWeb = st.text_input("Pagina Web:")
if "contextoWeb" not in st.session_state:
    print("Se crea contextoWeb")
    st.session_state.contextoWeb = contextoWeb
else:
    if contextoWeb == st.session_state.contextoWeb:
        print("es el mismo contextoWeb")
    else:
        st.session_state.contextoWeb = contextoWeb
        print("Se actualiza contextoWeb")


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

#ipregunta del usuario hacerca del doc page
pregunta = st.chat_input("Pregunta: ")

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
    #Request
    try:
        response = requests.post(url_chatbot, json = question)
        if response.status_code == 200:
            with st.chat_message("ai"):
                st.markdown(response.json()['answer'])
                st.session_state.messages.append({"role": "ai", "content": response.json()['answer']}) #se guarda chat_history para streamlit
                st.session_state.chat_history.append(response.json()['answer']) #se guarda chat_history para chatbot
    except:
        with st.chat_message("assistant"):
            st.markdown("Error de servidor, intenta nuevamente")

else:
    with st.chat_message("assistant"):
            st.markdown("Favor de completar el campoo 'Pagina Web' y 'Pregunta'")




