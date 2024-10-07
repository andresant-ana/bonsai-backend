from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    id: str
    title: str
    messages: List[Message]

class ConversationUpdate(BaseModel):
    title: Optional[str] = None

conversations = {}
company_document = ""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(file: UploadFile) -> str:
    return file.file.read().decode("utf-8")

def get_ai_response(messages: List[Message]) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m.role, "content": m.content} for m in messages] + [
            {"role": "system", "content": f"Você é um assistente AI para a seguinte empresa:\n{company_document}"}
        ]
    )
    return response.choices[0].message.content

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    global company_document
    company_document = read_file(file)
    return {"message": "Documento da empresa carregado com sucesso"}

@app.get("/document")
async def get_document():
    if not company_document:
        raise HTTPException(status_code=404, detail="Nenhum documento carregado")
    return {"document": company_document}

@app.delete("/document")
async def delete_document():
    global company_document
    company_document = ""
    return {"message": "Documento da empresa removido com sucesso"}

@app.post("/conversations")
async def create_conversation(conversation: Conversation):
    conversations[conversation.id] = conversation
    return conversation

@app.get("/conversations")
async def list_conversations():
    return list(conversations.values())

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return conversations[conversation_id]

@app.put("/conversations/{conversation_id}")
async def update_conversation(conversation_id: str, update: ConversationUpdate):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    if update.title:
        conversations[conversation_id].title = update.title
    return conversations[conversation_id]

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    del conversations[conversation_id]
    return {"message": "Conversa removida com sucesso"}

@app.post("/conversations/{conversation_id}/messages")
async def add_message(conversation_id: str, message: Message):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    conversations[conversation_id].messages.append(message)
    ai_response = get_ai_response(conversations[conversation_id].messages)
    ai_message = Message(role="assistant", content=ai_response)
    conversations[conversation_id].messages.append(ai_message)
    return ai_message

@app.put("/conversations/{conversation_id}/messages/{message_index}")
async def edit_message(conversation_id: str, message_index: int, message: Message):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    if message_index >= len(conversations[conversation_id].messages):
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    conversations[conversation_id].messages[message_index] = message
    # Recalcula a resposta da IA
    ai_response = get_ai_response(conversations[conversation_id].messages[:message_index+1])
    ai_message = Message(role="assistant", content=ai_response)
    if message_index + 1 < len(conversations[conversation_id].messages):
        conversations[conversation_id].messages[message_index + 1] = ai_message
    else:
        conversations[conversation_id].messages.append(ai_message)
    return ai_message

# Inicia o servidor com o comando: uvicorn app:app --reload