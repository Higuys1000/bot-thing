import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True  # REQUIRED for reaction events

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_GIF = "https://klipy.com/gifs/drmanhattan-watchman"
TIMEOUT_SECONDS = 60

# Role-based cooldowns (in hours)
ROLE_COOLDOWNS = {
    "Bum": 18,
    "Rat": 9,
    "Chud": 4,
    "Otis BFF ❤️": 4,
    "Good Moderator Morning!": 0
}

last_used = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.reference or TARGET_GIF not in message.content:
        await bot.process_commands(message)
        return

    replied_message = await message.channel.fetch_message(message.reference.message_id)
    member_to_timeout = message.guild.get_member(replied_message.author.id)

    # Get user's valid roles
    author_roles = [role.name for role in message.author.roles]
    valid_roles = [r for r in author_roles if r in ROLE_COOLDOWNS]

    # No valid role → deny
    if not valid_roles:
        await message.channel.send(
            f"{message.author.mention}, you don't have permission to use this GIF!"
        )
        return

    # Pick BEST role (lowest cooldown)
    best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
    cooldown_hours = ROLE_COOLDOWNS[best_role]

    now = datetime.utcnow()
    last = last_used.get(message.author.id)

    # Cooldown check (skip if 0)
    if cooldown_hours > 0 and last:
        if now - last < timedelta(hours=cooldown_hours):
            remaining = timedelta(hours=cooldown_hours) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, ({best_role}) you can use the GIF again in {str(remaining).split('.')[0]}"
            )
            return

    try:
        await member_to_timeout.timeout(
            discord.utils.utcnow() + timedelta(seconds=TIMEOUT_SECONDS)
        )

        last_used[message.author.id] = now

        await message.channel.send(
            f"{member_to_timeout.mention} has been timed out for {TIMEOUT_SECONDS}s by {message.author.mention} lmao"
        )

    except Exception as e:
        await message.channel.send(
            f"Failed to timeout {member_to_timeout.mention}: {e}"
        )

    await bot.process_commands(message)  # allow commands to still work


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    emoji_map = {
        "🫃": "MPREG",
        "🤰": "WPREG",
        "🧑‍🍼": "PREG"
    }

    emoji_str = str(reaction.emoji)

    if emoji_str in emoji_map:
        label = emoji_map[emoji_str]
        await reaction.message.channel.send(
            f"{user.mention} JUST USED {label} EMOJI GO KILL THEM"
        )


bot.run(os.getenv("TOKEN"))
