import sys
sys.path.append(".")
from langchain_openai import ChatOpenAI #llm openia
from dotenv import load_dotenv #variables de entorno
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from modules.chatbot.chatbot_with_doc_openia import chatBotOpeniaWithDocWeb_Fastapi
from modules.chatbot.chatbot_openia import chatbot_openia
from modules.chatbot.chatbot_gen_dictionary_openia import chatbot_gen_dicionary_openia
import validators #para validar URL

async def dynamically_route_based_on_input(system_context, user_question, chat_history):
    #carga variables de entonrno
    load_dotenv()
    #modelo llm
    model = ChatOpenAI()
    #prompt
    prompt = ChatPromptTemplate.from_template('''
        Evalúa la siguiente pregunta del usuario y determina si se está solicitando un 'Grafico', una 'Tabla', o si es algo 'Otro'.
        Solo responde con una de las siguientes palabras: 'Grafico', 'Tabla', 'Otro'.

        Ejemplos:
        - Gráfico: "genera un gráfico", "grafica esta tabla", "construye un gráfico", "muestra un gráfico de la tabla anterior"
        - Tabla: "genera una tabla", "construye una tabla", "compara los valores en una tabla", "muestra los datos en formato tabular"
        - Otro: "¿qué significa esto?", "descríbeme la tabla/grafico generado", "explica los datos", "dame más información sobre los valores"

        Basándote en los ejemplos anteriores, clasifica la siguiente pregunta del usuario:

        <user_question>
        {user_question}
        </user_question>
    ''')

    #chain
    chain = prompt | model | StrOutputParser()
    #pregunta dinamica
    res_dyna = chain.invoke({
        'user_question': user_question,
    })
    print(res_dyna)
    #Se llama a flujo correspondiente
    if res_dyna == "Grafico" or res_dyna == "Tabla":
        print("#devuelve un diccionario segun un docweb")
        res = await chatbot_gen_dicionary_openia(system_context,user_question,chat_history)  
    else:
        if es_url(system_context):
            print("##responde en base a un docweb(URL)")
            res = await chatBotOpeniaWithDocWeb_Fastapi(system_context, user_question, chat_history) 
        else:
            print("#responde en base a un contexto general")
            res = await chatbot_openia(system_context, user_question, chat_history) 
    return [res_dyna, res]



def es_url(valor):
    if validators.url(valor):
        return True
    return False