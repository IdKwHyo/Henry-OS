import discord
import httpx
import asyncio
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

async def query_backend(message: str, session_id: str = "discord") -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BACKEND_URL}/chat",
                                 json={"text": message, "session_id": session_id})
        return resp.json()["text"]

@bot.event
async def on_ready():
    print(f"Discord gateway logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Simple command: !henry <query>
    if message.content.startswith("!henry"):
        query = message.content[7:].strip()
        if query:
            async with message.channel.typing():
                response = await query_backend(query, f"discord-{message.guild.id}")
                await message.channel.send(response)
        else:
            await message.channel.send("What would you like me to do?")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("DISCORD_BOT_TOKEN not set, Discord gateway disabled.")
        # Keep running indefinitely so container doesn't stop
        asyncio.get_event_loop().run_forever()