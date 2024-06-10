import streamlit as st
import requests

url_chatbot= "http://127.0.0.1:8000/chatbot_openia"

st.title("CHATBOT")
pregunta = st.chat_input("Pregunta: ")
question = {
"input_context": "",
"input_question": pregunta
}

#inizializa chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#muestra chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)
        st.session_state.messages.append({"role": "user", "content": pregunta})
    response = requests.post(url_chatbot, json = question)
    if response.status_code == 200:
        with st.chat_message("ai"):
            st.markdown(response.json())
            st.session_state.messages.append({"role": "ai", "content": response.json()})
    else:
        with st.chat_message("assistant"):
            st.markdown("Error de servidor, intenta nuevamente")
