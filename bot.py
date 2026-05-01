import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import asyncio
import re
import traceback

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

    "https://tenor.com/fNMtMSKEIch.gif",

    "https://tenor.com/view/goku-black-goku-black-shush-zamasu-gif-5057528923283903671"
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

# Roles allowed to use !deglove and !reglove
DEGLOVE_ROLES = {"Shit ass mod", "Good Moderator Morning!"}

# Channel names
DEADLY_SENTENCES_CHANNEL = "deadly-sentences"
MODLOG_CHANNEL = "modlog"

# Banned role name to assign during deglove
BANNED_ROLE_NAME = "Banned"

# Stores active deglovings:
# { member_id: { "role_ids": [int], "message_id": int, "channel_id": int, "task": Task } }
active_deglovings = {}

last_used = {}


# =========================
# ERROR LOGGING HELPER
# =========================

async def log_error(guild, label: str, error: Exception):
    """Sends an error message to #modlog and prints to console."""
    tb = traceback.format_exc()
    print(f"[ERROR] {label}: {error}\n{tb}")
    modlog = discord.utils.get(guild.text_channels, name=MODLOG_CHANNEL)
    if modlog:
        # Truncate traceback if it's very long
        tb_trimmed = tb[-1500:] if len(tb) > 1500 else tb
        await modlog.send(
            f"⚠️ **Bot Error — {label}**\n"
            f"```{type(error).__name__}: {error}\n\n{tb_trimmed}```"
        )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


def parse_duration(duration_str):
    """
    Parses a duration string like '10m', '2h', '1d', '30s' into total seconds.
    Returns None if the format is invalid.
    """
    match = re.fullmatch(r"(\d+)(s|m|h|d)", duration_str.strip().lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return value * multipliers[unit]


async def reglove_member(guild, member, announce_channel):
    """Restores a member's roles after deglove ends (or is cut short by !reglove)."""
    entry = active_deglovings.pop(member.id, None)
    if not entry:
        return

    # Cancel the scheduled task if it's still running
    task = entry.get("task")
    if task and not task.done():
        task.cancel()

    saved_role_ids = entry.get("role_ids", [])
    message_id = entry.get("message_id")
    channel_id = entry.get("channel_id")

    # Remove Banned role
    banned_role = discord.utils.get(guild.roles, name=BANNED_ROLE_NAME)
    if banned_role and banned_role in member.roles:
        try:
            await member.remove_roles(banned_role, reason="Deglove period ended")
        except Exception as e:
            await log_error(guild, f"reglove: remove Banned role from {member}", e)

    # Re-fetch role objects fresh from the guild by ID to avoid stale references
    bot_top_role = guild.me.top_role
    roles_to_restore = []
    for role_id in saved_role_ids:
        role = guild.get_role(role_id)
        if role is None:
            print(f"[reglove] Role ID {role_id} no longer exists in guild, skipping")
            continue
        if role.managed:
            continue
        if role >= bot_top_role:
            print(f"[reglove] Skipping role above bot's top role: {role.name}")
            continue
        roles_to_restore.append(role)

    if roles_to_restore:
        try:
            await member.add_roles(*roles_to_restore, reason="Deglove period ended")
            print(f"[reglove] Restored {len(roles_to_restore)} roles to {member}")
        except Exception as e:
            await log_error(guild, f"reglove: restore roles for {member}", e)
    else:
        msg = f"[reglove] No restorable roles found for {member} (saved IDs: {saved_role_ids})"
        print(msg)
        modlog = discord.utils.get(guild.text_channels, name=MODLOG_CHANNEL)
        if modlog:
            await modlog.send(f"⚠️ **Reglove warning:** No roles could be restored for {member.mention}. Saved IDs: `{saved_role_ids}`")

    # Delete the sentence message — fetch fresh by ID so the reference isn't stale
    if channel_id and message_id:
        try:
            sentence_channel = guild.get_channel(channel_id)
            if sentence_channel:
                sentence_message = await sentence_channel.fetch_message(message_id)
                await sentence_message.delete()
            else:
                raise ValueError(f"Channel ID {channel_id} not found in guild")
        except Exception as e:
            await log_error(guild, f"reglove: delete sentence message {message_id}", e)

    if announce_channel:
        await announce_channel.send(f"{member.mention} has been regloved. Roles restored.")


@bot.command(name="deglove")
async def deglove(ctx, duration: str = None, *, reason: str = None):
    """
    Usage (as a reply): !deglove <duration> <reason>
    Duration format: 30s, 10m, 2h, 1d
    Requires "Shit ass mod" or "Good Moderator Morning!" role.
    """
    author_roles = {role.name for role in ctx.author.roles}

    # Permission check
    if not (author_roles & DEGLOVE_ROLES):
        await ctx.send(f"{ctx.author.mention}, you don't have permission to deglove.")
        return

    # Must be a reply
    if not ctx.message.reference:
        await ctx.send("You need to reply to someone's message to deglove them.")
        return

    # Duration required
    if not duration:
        await ctx.send("Usage: `!deglove <duration> <reason>` (e.g. `!deglove 10m being annoying`)")
        return

    seconds = parse_duration(duration)
    if seconds is None:
        await ctx.send("Invalid duration format. Use `30s`, `10m`, `2h`, or `1d`.")
        return

    if not reason:
        await ctx.send("Please provide a reason. Usage: `!deglove <duration> <reason>`")
        return

    # Get the target member
    try:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    except Exception as e:
        await ctx.send("Couldn't fetch the replied message.")
        await log_error(ctx.guild, "deglove: fetch replied message", e)
        return

    member = ctx.guild.get_member(replied_message.author.id)

    if not member:
        await ctx.send("Couldn't find that member in the server.")
        return

    if member.bot:
        await ctx.send("You can't deglove a bot.")
        return

    # Check if already degloved
    if member.id in active_deglovings:
        await ctx.send(f"{member.mention} is already degloved.")
        return

    # Get Banned role
    banned_role = discord.utils.get(ctx.guild.roles, name=BANNED_ROLE_NAME)
    if not banned_role:
        await ctx.send(f'Could not find a role named "{BANNED_ROLE_NAME}". Make sure it exists.')
        return

    # Save role IDs (not objects) — avoids stale references when the timer fires later
    bot_top_role = ctx.guild.me.top_role
    saved_role_ids = [
        r.id for r in member.roles
        if r != ctx.guild.default_role and not r.managed and r < bot_top_role
    ]
    print(f"[deglove] Saving role IDs for {member}: {saved_role_ids}")

    # Remove all saveable roles
    roles_to_remove = [ctx.guild.get_role(rid) for rid in saved_role_ids]
    roles_to_remove = [r for r in roles_to_remove if r]
    if roles_to_remove:
        try:
            await member.remove_roles(*roles_to_remove, reason=f"Degloved by {ctx.author}")
        except discord.Forbidden as e:
            await ctx.send("I don't have permission to remove that member's roles.")
            await log_error(ctx.guild, f"deglove: remove roles from {member}", e)
            return
        except Exception as e:
            await ctx.send("Something went wrong removing roles.")
            await log_error(ctx.guild, f"deglove: remove roles from {member}", e)
            return

    # Add Banned role
    try:
        await member.add_roles(banned_role, reason=f"Degloved by {ctx.author}: {reason}")
    except discord.Forbidden as e:
        await ctx.send("I don't have permission to assign the Banned role.")
        await log_error(ctx.guild, f"deglove: add Banned role to {member}", e)
        if roles_to_remove:
            await member.add_roles(*roles_to_remove, reason="Deglove failed, restoring roles")
        return
    except Exception as e:
        await ctx.send("Something went wrong assigning the Banned role.")
        await log_error(ctx.guild, f"deglove: add Banned role to {member}", e)
        return

    # Post in #deadly-sentences — store message ID and channel ID, not the object
    sentence_channel = discord.utils.get(ctx.guild.text_channels, name=DEADLY_SENTENCES_CHANNEL)
    message_id = None
    channel_id = None
    if sentence_channel:
        try:
            sentence_message = await sentence_channel.send(
                f"🩸 **DEGLOVED** 🩸\n"
                f"**{member.display_name}** has been degloved by {ctx.author.mention}\n"
                f"**Duration:** {duration}\n"
                f"**Reason:** {reason}"
            )
            message_id = sentence_message.id
            channel_id = sentence_channel.id
        except Exception as e:
            await log_error(ctx.guild, "deglove: send deadly-sentences message", e)
    else:
        await ctx.send(f'Warning: Could not find channel "{DEADLY_SENTENCES_CHANNEL}" to post the sentence.')

    await ctx.send("https://klipy.com/gifs/gojo-geto-suguru-2--k01KQGSQKMYQQE758SGTJ41WF3X")
    await ctx.send(f"{member.mention} has been sealed for {duration}")

    # Store entry first, then create task
    active_deglovings[member.id] = {
        "role_ids": saved_role_ids,
        "message_id": message_id,
        "channel_id": channel_id,
        "task": None,
    }

    async def scheduled_reglove():
        try:
            await asyncio.sleep(seconds)
            if member.id in active_deglovings:
                await reglove_member(ctx.guild, member, ctx.channel)
        except asyncio.CancelledError:
            pass  # Task was cancelled by !reglove, that's fine
        except Exception as e:
            await log_error(ctx.guild, f"scheduled_reglove for {member}", e)

    task = asyncio.create_task(scheduled_reglove())
    active_deglovings[member.id]["task"] = task


@bot.command(name="reglove")
async def reglove(ctx):
    """
    Usage (as a reply): !reglove
    Cuts a deglove short early and restores the member's roles.
    Requires "Shit ass mod" or "Good Moderator Morning!" role.
    """
    author_roles = {role.name for role in ctx.author.roles}

    # Permission check
    if not (author_roles & DEGLOVE_ROLES):
        await ctx.send(f"{ctx.author.mention}, you don't have permission to reglove.")
        return

    # Must be a reply
    if not ctx.message.reference:
        await ctx.send("You need to reply to the message of the person you want to reglove.")
        return

    try:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    except Exception as e:
        await ctx.send("Couldn't fetch the replied message.")
        await log_error(ctx.guild, "reglove: fetch replied message", e)
        return

    member = ctx.guild.get_member(replied_message.author.id)

    if not member:
        await ctx.send("Couldn't find that member in the server.")
        return

    if member.id not in active_deglovings:
        await ctx.send(f"{member.mention} isn't currently degloved.")
        return

    try:
        await reglove_member(ctx.guild, member, ctx.channel)
    except Exception as e:
        await log_error(ctx.guild, f"reglove command for {member}", e)


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

    try:
        replied_message = await message.channel.fetch_message(message.reference.message_id)
    except Exception as e:
        await log_error(message.guild, "on_message: fetch replied message", e)
        await bot.process_commands(message)
        return

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
                await message.channel.send(f"Failed to remove timeout.")
                await log_error(message.guild, f"untimeout: remove timeout from {member_to_timeout}", e)
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
            await message.channel.send(f"Failed to timeout {member_to_timeout.mention}.")
            await log_error(message.guild, f"timeout: apply timeout to {member_to_timeout}", e)

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


@bot.event
async def on_command_error(ctx, error):
    """Catches any unhandled command errors and logs them to #modlog."""
    # Ignore expected non-errors
    if isinstance(error, commands.CommandNotFound):
        return
    await log_error(ctx.guild, f"command error in #{ctx.channel.name} by {ctx.author}", error)


bot.run(os.getenv("TOKEN"))
