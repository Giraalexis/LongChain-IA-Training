from langchain_community.llms import Ollama #modelo ia
from langchain_core.prompts import ChatPromptTemplate #prompt de langchain
from deep_translator import GoogleTranslator #traductor de idiomas
from langchain_core.output_parsers import StrOutputParser #convierte la salida del chat en cadena


def chatbotOllama(system_context,user_question):
    #prompt:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_context),
        ("user", "{input}")
    ])
    #modelo llm:
    llm = Ollama(model="llama3")
    #return cadena
    output_parser = StrOutputParser()
    #chain
    chain = prompt | llm | output_parser
    #pregunta al bot:
    response = chain.invoke({'input': user_question})
    #Traductor, para traducir la respuesta de ingles a español
    translated = GoogleTranslator(source='auto', target='es').translate(response)
    #mostrar resultado
    print(translated)

#ejemplo
chatbotOllama(input("system input: "), input("question input: "))
