from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama #modelo ia
import asyncio

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
model = Ollama(model="llama3")
chain = prompt | model | parser



async def print_astream_events():
    async for event in chain.astream_events({"topic": "parrot"}, version="v1"):
        print(event)

async def print_async():
    async for chunk in chain.astream({"topic": "parrot"}):
        print(chunk, end="|", flush=True)

asyncio.run(print_astream_events())
asyncio.run(print_async())