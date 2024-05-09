import getpass
import os
from langchain_openai import ChatOpenAI
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

#api key
key = json.load(open('./utils/api_key.json', encoding='utf-8'))
os.environ[key["API_KEY"]["OPEN_IA"]] = getpass.getpass()
#model
model = ChatOpenAI(model="gpt-3.5-turbo-0125")
#prompt
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
#return cadena
output_parser = StrOutputParser()

#chain
chain = prompt | model | output_parser

#pregunta
response = chain.invoke({"topic": "ice cream"})
#respuesta
print(response)