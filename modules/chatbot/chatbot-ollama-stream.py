from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama #modelo ia
import asyncio

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
model = Ollama(model="llama3")
chain = prompt | model | parser


async def print_async():
    async for chunk in chain.astream({"topic": "parrot"}):
        print(chunk, end="|", flush=True)

asyncio.run(print_async())