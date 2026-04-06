import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Needed for timeouts

bot = commands.Bot(command_prefix="!", intents=intents)

# The GIF that triggers the timeout
TARGET_GIF = "https://klipy.com/gifs/drmanhattan-watchman"

# Timeout duration in seconds
TIMEOUT_SECONDS = 60

# Role that is allowed to use this feature
ALLOWED_ROLES = ["Bum", "Otis BFF ❤️"]

# Dictionary to store last used timestamp per user
last_used = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Must be a reply
    if message.reference:
        replied_message = await message.channel.fetch_message(message.reference.message_id)
        member_to_timeout = message.guild.get_member(replied_message.author.id)

        # Check if message contains the target GIF
        if TARGET_GIF in message.content:

            # Check if author has the role
            author_roles = [role.name for role in message.author.roles]
            if not any(role in author_roles for role in ALLOWED_ROLES):
                await message.channel.send(f"{message.author.mention}, you don't have permission to use this GIF!")
                return

            # Check cooldown (once per 24h)
            now = datetime.utcnow()
            last = last_used.get(message.author.id)
            if last and now - last < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last)
                await message.channel.send(
                    f"{message.author.mention}, you can use the GIF again in {str(remaining).split('.')[0]}"
                )
                return

            try:
                # Timeout the user
                # Timeout the user (timezone-aware)
                await member_to_timeout.timeout(discord.utils.utcnow() + timedelta(seconds=TIMEOUT_SECONDS))
                last_used[message.author.id] = now
                await message.channel.send(
                    f"{member_to_timeout.mention} has been timed out for {TIMEOUT_SECONDS} seconds by {message.author.mention} 💀"
                )
            except Exception as e:
                await message.channel.send(f"Failed to timeout {member_to_timeout.mention}: {e}")

    await bot.process_commands(message)
bot.run(os.getenv("TOKEN"))