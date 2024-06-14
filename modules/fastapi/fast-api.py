import sys
sys.path.append(".")
from fastapi import FastAPI
from modules.chatbot.chatbot_ollama import chatbotOllama
from modules.chatbot.chatbot_openia import chatbot_openia
from modules.chatbot.chatbot_with_doc_openia import chatBotOpeniaWithDocWeb_Fastapi
from modules.chatbot.dynamically_route import dynamically_route_based_on_input
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class InputRequest_chatbot(BaseModel):
    input_context: str
    input_question: str

class InputRequest_chatbot_with_doc(BaseModel):
    input_context: str
    input_question: str
    chat_history: list

    
@app.post("/chatbot_ollama")
async def ollama_question(request: InputRequest_chatbot):
    response = await chatbotOllama(request.input_context, request.input_question)
    return response


@app.post("/chatbot_openia")
async def ollama_question(request: InputRequest_chatbot):
    response = await chatbot_openia(request.input_context, request.input_question)
    return response

@app.post("/chatbot_openia_with_doc")
async def ollama_question(request: InputRequest_chatbot_with_doc):
    response = await chatBotOpeniaWithDocWeb_Fastapi(request.input_context, request.input_question, request.chat_history)
    return response

@app.post("/dynamically_route")
async def ollama_question(request: InputRequest_chatbot_with_doc):
    response = await dynamically_route_based_on_input(request.input_context, request.input_question, request.chat_history)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)