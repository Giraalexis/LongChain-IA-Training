import streamlit as st
import requests
import pandas as pd
import json


url_chatbot= "http://127.0.0.1:8001/dynamically_route" 

#Titulo
st.title("CHATBOT WITH DOC WEB")

# Sección fija para la entrada del contexto de la web
contextoWeb = st.text_input("Página Web:", key="contextoWeb")

#inizializa chat history streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

#inizializa chat history streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


#muestra chat history streamlit
for message in st.session_state.messages:
    if message["type"] == "text":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if message["type"] == "table":
        with st.chat_message(message["role"]):
            # Convertir el contenido almacenado a DataFrame
            df = pd.DataFrame(message["content"])
            st.dataframe(df)
    if message["type"] == "graphic":
        with st.chat_message(message["role"]):
            # Convertir el contenido almacenado a DataFrame
            df = pd.DataFrame(message["content"])
            st.line_chart(df)

# Captura la pregunta del usuario
pregunta = st.chat_input("Pregunta: ")

# Preparar la solicitud JSON para el chatbot
question = {
"input_context": contextoWeb,
"input_question": pregunta,
"chat_history": st.session_state.chat_history
}

if pregunta and contextoWeb:
    with st.chat_message("user"):
        st.markdown(pregunta)
        st.session_state.messages.append({"role": "user", "content": pregunta, "type": "text"}) #se guarda chat_history para streamlit
        st.session_state.chat_history.append(pregunta) #se guarda chat_history para chatbot
    #Request
    try:
        response = requests.post(url_chatbot, json = question)
        if response.status_code == 200:
            response = response.json()
            if response[0] == "Grafico" or response[0] == "Tabla":
                print("responde ia con tabla/grafico")
                # Convertir la cadena en un json
                data_list = json.loads(response[1])
                # Crear un DataFrame utilizando pandas
                df = pd.DataFrame(data_list)
                #muestra con streamlist
                if response[0] == "Tabla":
                    with st.chat_message("ai"):
                        st.dataframe(df)
                        st.session_state.messages.append({"role": "ai", "content": data_list, "type": "table"}) #se guarda chat_history para streamlit
                else:
                    with st.chat_message("ai"):
                        st.line_chart(df)
                        st.session_state.messages.append({"role": "ai", "content": data_list, "type": "graphic"}) #se guarda chat_history para streamlit

                #guarda chat_history
                st.session_state.chat_history.append(response[1]) #se guarda chat_history para chatbot
            else:
                print("responde ia contexto")
                with st.chat_message("ai"):
                    st.markdown(response[1])    
                    st.session_state.messages.append({"role": "ai", "content": response[1], "type": "text"}) #se guarda chat_history para streamlit
                    st.session_state.chat_history.append(response[1]) #se guarda chat_history para chatbot
    except:
        with st.chat_message("assistant"):
            st.markdown("Error de servidor, intenta nuevamente")

else:
    with st.chat_message("assistant"):
            st.markdown("Favor de completar el campoo 'Pagina Web' y 'Pregunta'")




