from fastapi import FastAPI
from chatbot_ollama import chatbotOllama
from chatbot_openia import chatbot_openia
from chatbot_with_doc_openia import chatBotOpeniaWithDocWeb_Fastapi
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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)