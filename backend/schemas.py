from pydantic import BaseModel

class Message(BaseModel):
    text: str
    session_id: str = "default"

class AgentResponse(BaseModel):
    text: str

class StreamEvent(BaseModel):
    type: str  # thinking, tool_call, response, memory
    content: str
    agent: str = "henry"