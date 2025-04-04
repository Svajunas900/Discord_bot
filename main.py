import discord
from dotenv import load_dotenv
import os 

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


class Client(discord.Client):
  async def on_ready(self):
    print(f"Logged on as {self.user}!")
  

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(DISCORD_TOKEN)