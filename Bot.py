import discord
from discord.ext import commands
import mysql.connector

# Initialize Discord bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to MySQL database
db = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_mysql_database"
)

# Function to check if the server is authenticated
def is_authenticated(guild_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM auth_tokens WHERE guild_id = %s", (guild_id,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Event: Message received
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the server is authenticated
    if is_authenticated(message.guild.id):
        if message.content.lower() == "!hello":
            await message.channel.send(f"Hello world {message.guild.name}")
    else:
        await message.channel.send("This server is not authenticated.")

    await bot.process_commands(message)

# Run the bot
bot.run("your_discord_bot_token")
