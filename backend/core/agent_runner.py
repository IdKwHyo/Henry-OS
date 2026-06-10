import ollama
import json
import asyncio
from typing import AsyncGenerator
from core.tools import Tools
from models.schemas import StreamEvent

SYSTEM_PROMPT = """You are Henry, a highly capable technical AI operating system. 
You have tools: browser (web search), memory (recall/remember), and coding. 
Respond concisely, use tools when necessary. Always output JSON with "action" and "content" fields."""

class AgentRunner:
    def __init__(self, memory):
        self.memory = memory
        self.tools = Tools()
    
    async def process(self, user_input: str, session_id: str = "default") -> str:
        # Simple single-turn agent loop
        # Retrieve relevant memories
        memories = await self.memory.retrieve(user_input)
        context = "\n".join([f"Memory: {m}" for m in memories])
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nUser: {user_input}"}
        ]
        
        # Use Ollama with tool support (simplified)
        response = ollama.chat(
            model="qwen2.5:14b",  # same as env or hardcoded
            messages=messages,
            format="json",
            options={"temperature": 0.3}
        )
        try:
            ai_msg = json.loads(response["message"]["content"])
            action = ai_msg.get("action", "respond")
            content = ai_msg.get("content", response["message"]["content"])
        except:
            action = "respond"
            content = response["message"]["content"]
        
        # Execute action if tool
        if action == "browser":
            content = await self.tools.browser_search(content)
        elif action == "remember":
            await self.memory.store(content, session_id)
            content = "Memory stored."
        
        # Store interaction
        await self.memory.store(f"User: {user_input} | Henry: {content}", session_id)
        return content
    
    async def process_stream(self, user_input: str, session_id: str = "default") -> AsyncGenerator[StreamEvent, None]:
        # Stream events to WebSocket
        yield StreamEvent(type="thinking", content="Processing...", agent="henry")
        memories = await self.memory.retrieve(user_input)
        yield StreamEvent(type="memory", content=f"Retrieved {len(memories)} memories", agent="atlas")
        
        # ... same logic as process() but yield intermediate events
        # (simplified: just yield tool calls and response)
        response = await self.process(user_input, session_id)  # non-streaming for MVP
        yield StreamEvent(type="response", content=response, agent="henry")