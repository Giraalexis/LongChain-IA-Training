from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder #permite añadir un listado de menajes en el prompt
from dotenv import load_dotenv

async def chatbot_openia(system_context,user_question,chat_history):

    #api key
    load_dotenv()
    #model
    model = ChatOpenAI()
    #prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_context),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}") 
    ])
    #return cadena
    output_parser = StrOutputParser()

    #chain
    chain = prompt | model | output_parser

    #pregunta
    response = chain.invoke({
        'input': user_question,
        'chat_history': chat_history
    })
    #respuesta
    print(response)
    return response

#chatbot_openia("definicion corta","gatos")