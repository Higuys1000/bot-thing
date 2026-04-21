import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# TIMEOUT GIFS
TARGET_GIFS = [
    "https://tenor.com/view/jujutsu-kaisen-inumaki-toge-toge-inumaki-inumaki-toge-gif-2839387565091272519",
    "https://klipy.com/gifs/drmanhattan-watchman",
    "https://klipy.com/gifs/blue-lock-gagamaru",
    "https://tenor.com/view/jjk-jujutsu-kaisen-jjk-fight-jujutsu-kaisen-fight-yuji-itadori-gif-13410355612590763521",
    "https://tenor.com/view/toji-kick-gif-12937973716924321908"
    "https://tenor.com/view/toji-kick-gif-12937973716924321908"
    "https://tenor.com/view/nanami-shigemo-jjk-jujutsu-kaisen-jjk-season-2-gif-9821210930918976877"
]

UNTIMEOUT_GIFS = [
    "https://tenor.com/view/doctor-manhattan-watchmen-marvel-gif-21030500",
    "https://klipy.com/gifs/doctor-manhattan-watchmen"
    "https://tenor.com/view/revive-gif-23866294"
    "https://tenor.com/view/kenjaku-jujutsu-kaisen-mahito-geto-suguru-geto-gif-3390342049104401664"
]

TIMEOUT_SECONDS = 90

ROLE_COOLDOWNS = {
    "Bum": 18,
    "Rat": 9,
    "Chud": 4,
    "Otis BFF ❤️": 4,
    "Shit ass mod": 0,
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

    # Must be a reply
    if not message.reference:
        await bot.process_commands(message)
        return

    content = message.content

    # Check if it's any relevant GIF
    if not (any(gif in content for gif in TARGET_GIFS) or any(gif in content for gif in UNTIMEOUT_GIFS)):
        await bot.process_commands(message)
        return

    replied_message = await message.channel.fetch_message(message.reference.message_id)
    member_to_timeout = message.guild.get_member(replied_message.author.id)

    if not member_to_timeout:
        return

    # ROLE CHECK
    author_roles = [role.name for role in message.author.roles]
    valid_roles = [r for r in author_roles if r in ROLE_COOLDOWNS]

    if not valid_roles:
        await message.channel.send(
            f"{message.author.mention}, you don't have permission to use this GIF!"
        )
        return

    # BEST ROLE (lowest cooldown)
    best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
    cooldown_hours = ROLE_COOLDOWNS[best_role]

    now = datetime.utcnow()
    last = last_used.get(message.author.id)

    # SHARED COOLDOWN CHECK
    if cooldown_hours > 0 and last:
        if now - last < timedelta(hours=cooldown_hours):
            remaining = timedelta(hours=cooldown_hours) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, ({best_role}) you can use a GIF again in {str(remaining).split('.')[0]}"
            )
            return

    # =========================
    # UNTIMEOUT LOGIC
    # =========================
    if any(gif in content for gif in UNTIMEOUT_GIFS):
        if not member_to_timeout.timed_out_until:
            await message.channel.send("They're not even timed out bro 💀")
            return

        now_discord = discord.utils.utcnow()
        remaining = member_to_timeout.timed_out_until - now_discord

        if remaining.total_seconds() <= 90:
            try:
                await member_to_timeout.timeout(None)

                last_used[message.author.id] = now  # shared cooldown trigger

                await message.channel.send(
                    f"{member_to_timeout.mention} has been freed early by {message.author.mention}"
                )
            except Exception as e:
                await message.channel.send(f"Failed to remove timeout: {e}")
        else:
            await message.channel.send(
                f"Too long left on timeout ({int(remaining.total_seconds())}s). Can't save them."
            )

        return

    # =========================
    # TIMEOUT LOGIC
    # =========================
    if any(gif in content for gif in TARGET_GIFS):
        try:
            await member_to_timeout.timeout(
                discord.utils.utcnow() + timedelta(seconds=TIMEOUT_SECONDS)
            )

            last_used[message.author.id] = now  # shared cooldown trigger

            await message.channel.send(
                f"{member_to_timeout.mention} has been timed out for {TIMEOUT_SECONDS}s by {message.author.mention} lmao"
            )

        except Exception as e:
            await message.channel.send(
                f"Failed to timeout {member_to_timeout.mention}: {e}"
            )

    await bot.process_commands(message)


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
