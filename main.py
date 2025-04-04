import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os 


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


class Client(commands.Bot):
  async def on_ready(self):
    print(f"Logged on as {self.user}!")

    try:
      guild = discord.Object(id=1357615188332777613)
      synced = await self.tree.sync(guild=guild)
      print(f"Synced {len(synced)} commands to guild {guild.id}")
    except Exception as e:
      print(f"Error syncing commands: {e}")
  
  async def on_message(self, message):
    if message.author == self.user:
      return
    if message.content.startswith("hello"):
      await message.channel.send(f"Hi there {message.author}")
  
  async def on_reaction_add(self, reaction, user):
    await reaction.message.channel.send("You reacted")

  async def on_voice_state_update(self, member, before, after):
    if after.channel:
        print(f"{member} joined {after.channel}")
        voice_client = discord.utils.get(client.voice_clients, guild=member.guild)
        print(voice_client)
        if voice_client is None:
          channel = after.channel
          await channel.connect()
    if before.channel:
        print(f"{member} left {before.channel}")
        voice_client = discord.utils.get(client.voice_clients, guild=member.guild)
        if voice_client is not None:
          channel = before.channel
          
          await voice_client.disconnect()


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1357615188332777613)


@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
  await interaction.response.send_message("Hi there!")


@client.tree.command(name="printer", description="I will print whatever you give me", guild=GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
  await interaction.response.send_message(printer)


@client.tree.command(name="embed", description="I'm embed", guild=GUILD_ID)
async def embed(interaction: discord.Interaction):
  embed = discord.Embed(title="I'm title", description="I'm description")
  embed.add_field(name="THis is title", value="Hello", inline=True)
  await interaction.response.send_message(embed=embed)


class View(discord.ui.View):
  @discord.ui.button(label="Click me!", style=discord.ButtonStyle.red, emoji="🔥")
  async def button_callback(self, button, interaction):
    await button.response.send_message("You have clicked the button!")

  @discord.ui.button(label="2nd Button", style=discord.ButtonStyle.blurple, emoji="😃")
  async def two_button_callback(self, button, interaction):
    await button.response.send_message("This is the second button!")

  @discord.ui.button(label="3rd Button", style=discord.ButtonStyle.green, emoji="👻")
  async def three_button_callback(self, button, interaction):
    await button.response.send_message("This is the third button!")


@client.tree.command(name="button", description="Displaying a button", guild=GUILD_ID)
async def myButton(interaction: discord.Interaction):
  await interaction.response.send_message(view=View())


@client.tree.command(name="listen", description="Listens for your voice", guild=GUILD_ID)
async def creepyVoice(interaction: discord.Interaction):
  await interaction.channel.voice_channels


client.run(DISCORD_TOKEN)