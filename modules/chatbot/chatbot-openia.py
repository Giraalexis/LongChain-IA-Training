import getpass
import os
from langchain_openai import ChatOpenAI
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

#api key
key = json.load(open('./utils/api_key.json', encoding='utf-8'))
#model
model = ChatOpenAI(api_key=key["API_KEY"]["OPEN_IA"])
#prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "dime una corta definicion"),
    ("user", "{input}") 
])
#return cadena
output_parser = StrOutputParser()

#chain
chain = prompt | model | output_parser

#pregunta
response = chain.invoke({"input": "gatos"})
#respuesta
print(response)