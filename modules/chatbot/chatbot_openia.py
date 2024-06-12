from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

async def chatbot_openia(system_context,user_question):

    #api key
    load_dotenv()
    #model
    model = ChatOpenAI()
    #prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_context),
        ("user", "{input}") 
    ])
    #return cadena
    output_parser = StrOutputParser()

    #chain
    chain = prompt | model | output_parser

    #pregunta
    response = chain.invoke({'input': user_question})
    #respuesta
    print(response)
    return response

#chatbot_openia("definicion corta","gatos")