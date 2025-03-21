import os
import discord
from discord import app_commands
import google.generativeai as genai

# Configure API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# System instructions for Gemini
SYSTEM_INSTRUCTIONS = """You are a helpful Coding AI assistant.
- Provide clear and concise explanations of coding concepts
- Maintain a friendly and professional tone
- Avoid harmful, inappropriate, or unethical content
- Admit uncertainty when unsure and suggest further resources
- Format code using appropriate syntax for the programming language: 
```language
  // your code here
```"""


# Set up Discord bot
class Client(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.default())
    self.tree = app_commands.CommandTree(self)

  async def setup_hook(self):
    await self.tree.sync()


client = Client()


@client.event
async def on_ready():
  print(f'Logged in as {client.user}')


@client.tree.command(name="ask", description="Ask C0-D3 a Coding Question")
async def ask(interaction: discord.Interaction, question: str):
  await interaction.response.defer()

  try:
    # Add instruction to keep response short
    prompt = f"{SYSTEM_INSTRUCTIONS}\nIMPORTANT: Keep your response under 4000 characters.\n\nUser: {question}"
    response = model.generate_content(prompt)
    await interaction.followup.send(response.text[:2000])
  except Exception as e:
    await interaction.followup.send(f"Error: {str(e)}")


if __name__ == "__main__":
  client.run(DISCORD_TOKEN)
