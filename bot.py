import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_GIFS = [

    "https://tenor.com/view/jujutsu-kaisen-inumaki-toge-toge-inumaki-inumaki-toge-gif-2839387565091272519",

    "https://klipy.com/gifs/drmanhattan-watchman",

    "https://klipy.com/gifs/blue-lock-gagamaru",

    "https://tenor.com/view/jjk-jujutsu-kaisen-jjk-fight-jujutsu-kaisen-fight-yuji-itadori-gif-13410355612590763521",

    "https://tenor.com/view/toji-kick-gif-12937973716924321908",

    "https://tenor.com/view/nanami-shigemo-jjk-jujutsu-kaisen-jjk-season-2-gif-9821210930918976877",

    "https://tenor.com/view/thragg-invincible-thragg-grabbing-mark-thragg-chasing-mark-blaziful-gif-9903393455394604140",

    "https://tenor.com/view/joe-swanson-gets-sent-to-the-shadow-realm-gif-12569580727382074039",

   "https://tenor.com/view/avatar-eyes-mark-philips-rdcworld1-i-have-awoken-rdc-gif-11037312579902835094",

    "https://tenor.com/view/xenoverse-goku-super-saiyan-angry-dbz-gif-1416275111944307575",

    "https://tenor.com/v3Hf08v2vRk.gif",

    "https://tenor.com/pZ9FvlIB584.gif",

    "https://tenor.com/view/naoya-jujutsu-kaisen-jujutsu-kaisen-season-3-maki-maki-zenin-gif-13642749527516671169",

    "https://tenor.com/bO4gv.gif",

    "https://tenor.com/view/gojo-gojo-satoru-gojo-season-2-hip-thrust-reaction-gif-10399129046512126318",

    "https://tenor.com/g1PMKnVanu.gif",

    "https://tenor.com/gCWUsSmNiKZ.gif",

    "https://tenor.com/bG6Lk.gif",

    "https://tenor.com/1nKPZe19HC.gif",

    "https://tenor.com/hePTjbsH6wO.gif",

    "https://tenor.com/s5LleKfiFIt.gif",

    "https://tenor.com/qiJpIenIjHB.gif",

    "https://tenor.com/fNMtMSKEIch.gif"

]

# UNTIMEOUT GIFS

UNTIMEOUT_GIFS = [

    "https://tenor.com/view/doctor-manhattan-watchmen-marvel-gif-21030500",

    "https://klipy.com/gifs/doctor-manhattan-watchmen",

    "https://tenor.com/view/revive-gif-23866294",

    "https://tenor.com/view/kenjaku-jujutsu-kaisen-mahito-geto-suguru-geto-gif-3390342049104401664"

    "https://tenor.com/onF9Vf3cHMO.gif",

    "https://tenor.com/ivDIWgkDkDv.gif",

    "https://tenor.com/qqPLKMoUvl1.gif",

    "https://tenor.com/hpUwFpPR9uO.gif",

    "https://tenor.com/gxFat3FEapG.gif",

    "https://tenor.com/gFHyueznjs6.gif",

    "https://tenor.com/MYbN.gif",

    "https://tenor.com/cNyjFADRNTl.gif",

    "https://tenor.com/bJKg7.gif",

    "https://tenor.com/maZbVIbE3Pr.gif",

    "https://tenor.com/pyF0khnkBOB.gif",

    "https://tenor.com/view/ryu-ryu-ishigori-yuta-yuta-okkotsu-jujutsu-kaisen-gif-8459438190665096786"

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

SPECIAL_ROLE = "GregVow"

last_used = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_roles = [role.name for role in message.author.roles]

    # =========================
    # BOT MENTION → SHOW COOLDOWN
    # =========================
    if bot.user in message.mentions:
        valid_roles = [r for r in author_roles if r in ROLE_COOLDOWNS]

        if not valid_roles:
            await message.channel.send(
                f"{message.author.mention}, you don't have any cooldown role."
            )
            return

        best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
        cooldown_hours = ROLE_COOLDOWNS[best_role]

        # Apply GregVow modifier
        if SPECIAL_ROLE in author_roles:
            cooldown_hours *= 2

        now = datetime.utcnow()
        last = last_used.get(message.author.id)

        if cooldown_hours == 0:
            await message.channel.send(
                f"{message.author.mention}, ({best_role}) you have no cooldown 😈"
            )
            return

        if not last or now - last >= timedelta(hours=cooldown_hours):
            await message.channel.send(
                f"{message.author.mention}, ({best_role}) you're ready to use a GIF."
            )
        else:
            remaining = timedelta(hours=cooldown_hours) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, ({best_role}) cooldown remaining: {str(remaining).split('.')[0]}"
            )

        return

    # MUST BE A REPLY
    if not message.reference:
        await bot.process_commands(message)
        return

    content = message.content

    if not (any(gif in content for gif in TARGET_GIFS) or any(gif in content for gif in UNTIMEOUT_GIFS)):
        await bot.process_commands(message)
        return

    replied_message = await message.channel.fetch_message(message.reference.message_id)
    member_to_timeout = message.guild.get_member(replied_message.author.id)

    if not member_to_timeout:
        return

    valid_roles = [r for r in author_roles if r in ROLE_COOLDOWNS]

    if not valid_roles:
        await message.channel.send(
            f"{message.author.mention}, you don't have permission to use this GIF!"
        )
        return

    best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
    cooldown_hours = ROLE_COOLDOWNS[best_role]

    # Apply GregVow modifier
    is_special = SPECIAL_ROLE in author_roles
    if is_special:
        cooldown_hours *= 3

    now = datetime.utcnow()
    last = last_used.get(message.author.id)

    if cooldown_hours > 0 and last:
        if now - last < timedelta(hours=cooldown_hours):
            remaining = timedelta(hours=cooldown_hours) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, ({best_role}) cooldown remaining: {str(remaining).split('.')[0]}"
            )
            return

    # =========================
    # UNTIMEOUT
    # =========================
    if any(gif in content for gif in UNTIMEOUT_GIFS):
        if not member_to_timeout.timed_out_until:
            await message.channel.send("They're not even timed out bro 💀")
            return

        remaining = member_to_timeout.timed_out_until - discord.utils.utcnow()

        if remaining.total_seconds() <= 90:
            try:
                await member_to_timeout.timeout(None)
                last_used[message.author.id] = now

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
    # TIMEOUT
    # =========================
    if any(gif in content for gif in TARGET_GIFS):
        try:
            duration = 180 if is_special else TIMEOUT_SECONDS

            await member_to_timeout.timeout(
                discord.utils.utcnow() + timedelta(seconds=duration)
            )

            last_used[message.author.id] = now

            await message.channel.send(
                f"{member_to_timeout.mention} has been timed out for {duration}s by {message.author.mention} lmao"
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

    if str(reaction.emoji) in emoji_map:
        await reaction.message.channel.send(
            f"{user.mention} JUST USED {emoji_map[str(reaction.emoji)]} EMOJI GO KILL THEM"
        )


bot.run(os.getenv("TOKEN"))
