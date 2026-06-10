from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, String, Text, DateTime, Float
from pgvector.sqlalchemy import Vector
import datetime
import os
import ollama

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://henry:henry@postgres:5432/henry")
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class MemoryEntry(Base):
    __tablename__ = "memories"
    id = Column(String, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(1024))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    importance = Column(Float, default=1.0)

class Memory:
    def __init__(self):
        self.embed_model = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")
    
    async def initialize(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def store(self, content: str, session_id: str = "default"):
        # Get embedding from Ollama
        emb = ollama.embeddings(model=self.embed_model, prompt=content)["embedding"]
        async with async_session() as session:
            entry = MemoryEntry(
                id=f"{session_id}-{datetime.datetime.utcnow().isoformat()}",
                content=content,
                embedding=emb,
            )
            session.add(entry)
            await session.commit()
    
    async def retrieve(self, query: str, k: int = 5):
        emb = ollama.embeddings(model=self.embed_model, prompt=query)["embedding"]
        async with async_session() as session:
            # pgvector similarity search
            result = await session.execute(
                """SELECT content, 1 - (embedding <=> :emb) AS similarity
                   FROM memories ORDER BY similarity DESC LIMIT :k""",
                {"emb": emb, "k": k}
            )
            rows = result.fetchall()
            return [row[0] for row in rows]
    
    async def close(self):
        await engine.dispose()