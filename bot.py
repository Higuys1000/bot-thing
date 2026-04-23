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
    "https://tenor.com/view/toji-kick-gif-12937973716924321908",
    "https://tenor.com/view/nanami-shigemo-jjk-jujutsu-kaisen-jjk-season-2-gif-9821210930918976877",
    "https://tenor.com/view/thragg-invincible-thragg-grabbing-mark-thragg-chasing-mark-blaziful-gif-9903393455394604140",
    "https://tenor.com/view/joe-swanson-gets-sent-to-the-shadow-realm-gif-12569580727382074039"
]

# UNTIMEOUT GIFS
UNTIMEOUT_GIFS = [
    "https://tenor.com/view/doctor-manhattan-watchmen-marvel-gif-21030500",
    "https://klipy.com/gifs/doctor-manhattan-watchmen",
    "https://tenor.com/view/revive-gif-23866294",
    "https://tenor.com/view/kenjaku-jujutsu-kaisen-mahito-geto-suguru-geto-gif-3390342049104401664"
]

TIMEOUT_SECONDS = 90

# BASE ROLE COOLDOWNS (HOURS)
ROLE_COOLDOWNS = {
    "Bum": 18,
    "Rat": 9,
    "Chud": 4,
    "Otis BFF ❤️": 4,
    "Shit ass mod": 0,
    "Good Moderator Morning!": 0,
    "Binding Vow": 0  # handled separately
}

# TRACK COOLDOWNS SEPARATELY
last_kill_used = {}
last_save_used = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def get_best_role(member):
    role_names = [role.name for role in member.roles]
    valid = [r for r in role_names if r in ROLE_COOLDOWNS]

    if not valid:
        return None

    # Binding Vow overrides everything
    if "Binding Vow" in valid:
        return "Binding Vow"

    return min(valid, key=lambda r: ROLE_COOLDOWNS[r])

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # BOT MENTION → SHOW COOLDOWN
    if bot.user in message.mentions:
        role = get_best_role(message.author)

        if not role:
            await message.channel.send(
                f"{message.author.mention}, you have to get to level 25 to use me!"
            )
            return

        now = datetime.utcnow()

        # Binding Vow display
        if role == "Binding Vow":
            kill_last = last_kill_used.get(message.author.id)
            save_last = last_save_used.get(message.author.id)

            kill_cd = timedelta(hours=30)
            save_cd = timedelta(minutes=10)

            kill_ready = not kill_last or now - kill_last >= kill_cd
            save_ready = not save_last or now - save_last >= save_cd

            await message.channel.send(
                f"{message.author.mention} (Binding Vow)\n"
                f"Kill: {'READY' if kill_ready else str(kill_cd - (now - kill_last)).split('.')[0]}\n"
                f"Save: {'READY' if save_ready else str(save_cd - (now - save_last)).split('.')[0]}"
            )
            return

        # NORMAL ROLES
        cooldown_hours = ROLE_COOLDOWNS[role]
        last = last_kill_used.get(message.author.id)

        if cooldown_hours == 0:
            await message.channel.send(
                f"{message.author.mention}, ({role}) no cooldown lol"
            )
            return

        if not last or now - last >= timedelta(hours=cooldown_hours):
            await message.channel.send(
                f"{message.author.mention}, ({role}) ready."
            )
        else:
            remaining = timedelta(hours=cooldown_hours) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, ({role}) cooldown: {str(remaining).split('.')[0]}"
            )
        return

    # MUST BE REPLY
    if not message.reference:
        await bot.process_commands(message)
        return

    content = message.content

    if not (any(g in content for g in TARGET_GIFS) or any(g in content for g in UNTIMEOUT_GIFS)):
        await bot.process_commands(message)
        return

    replied_message = await message.channel.fetch_message(message.reference.message_id)
    member = message.guild.get_member(replied_message.author.id)

    if not member:
        return

    role = get_best_role(message.author)

    if not role:
        await message.channel.send(
            f"{message.author.mention}, you have to get to level 25 to use this!"
        )
        return

    now = datetime.utcnow()

    # =========================
    # UNTIMEOUT (SAVE)
    # =========================
    if any(g in content for g in UNTIMEOUT_GIFS):

        if role == "Binding Vow":
            cooldown = timedelta(minutes=10)
            last = last_save_used.get(message.author.id)

            if last and now - last < cooldown:
                remaining = cooldown - (now - last)
                await message.channel.send(
                    f"{message.author.mention} save cooldown: {str(remaining).split('.')[0]}"
                )
                return
        else:
            cooldown = timedelta(hours=ROLE_COOLDOWNS[role])
            last = last_save_used.get(message.author.id)

            if ROLE_COOLDOWNS[role] > 0 and last and now - last < cooldown:
                remaining = cooldown - (now - last)
                await message.channel.send(
                    f"{message.author.mention} cooldown: {str(remaining).split('.')[0]}"
                )
                return

        if not member.timed_out_until:
            await message.channel.send("They're not timed out 💀")
            return

        remaining = member.timed_out_until - discord.utils.utcnow()

        if remaining.total_seconds() <= 90:
            try:
                await member.timeout(None)
                last_save_used[message.author.id] = now

                await message.channel.send(
                    f"{member.mention} saved by {message.author.mention}"
                )
            except Exception as e:
                await message.channel.send(f"Failed: {e}")
        else:
            await message.channel.send("Too long left.")

        return

    # =========================
    # TIMEOUT (KILL)
    # =========================
    if any(g in content for g in TARGET_GIFS):

        if role == "Binding Vow":
            cooldown = timedelta(hours=30)
            last = last_kill_used.get(message.author.id)

            if last and now - last < cooldown:
                remaining = cooldown - (now - last)
                await message.channel.send(
                    f"{message.author.mention} kill cooldown: {str(remaining).split('.')[0]}"
                )
                return
        else:
            cooldown = timedelta(hours=ROLE_COOLDOWNS[role])
            last = last_kill_used.get(message.author.id)

            if ROLE_COOLDOWNS[role] > 0 and last and now - last < cooldown:
                remaining = cooldown - (now - last)
                await message.channel.send(
                    f"{message.author.mention} cooldown: {str(remaining).split('.')[0]}"
                )
                return

        try:
            await member.timeout(
                discord.utils.utcnow() + timedelta(seconds=TIMEOUT_SECONDS)
            )

            last_kill_used[message.author.id] = now

            await message.channel.send(
                f"{member.mention} timed out by {message.author.mention}"
            )
        except:
            await message.channel.send("Can't timeout them.")

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

    if str(reaction.emoji) in emoji_map:
        await reaction.message.channel.send(
            f"{user.mention} USED {emoji_map[str(reaction.emoji)]} GO KILL THEM"
        )


bot.run(os.getenv("TOKEN"))
