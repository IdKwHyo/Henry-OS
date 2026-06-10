from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.memory import Memory
from core.agent_runner import AgentRunner
from core.websocket_manager import ConnectionManager
from models.schemas import Message, AgentResponse
import os

memory = Memory()
runner = AgentRunner(memory)
manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await memory.initialize()
    yield
    await memory.close()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/chat")
async def chat(message: Message):
    """Synchronous chat endpoint for basic testing (REST)."""
    response = await runner.process(message.text, session_id=message.session_id)
    return AgentResponse(text=response)

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Stream agent steps back to client
            async for event in runner.process_stream(data, session_id):
                await manager.send_personal_message(event, session_id)
    except WebSocketDisconnect:
        manager.disconnect(session_id)

@app.get("/health")
def health():
    return {"status": "ok"}