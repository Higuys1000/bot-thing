import random
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import asyncio
import re
import traceback
import json

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

# =========================
# BINDING VOW SYSTEM
#
# A user may hold AT MOST ONE Binding Vow at a time.
# If they somehow hold multiple, all vows are ignored and they get a warning.
#
# Standard vows (kill_multiplier / save_multiplier):
#   kill_multiplier : float | None — multiplied into base kill cooldown.
#                     None = kill action is fully blocked.
#   save_multiplier : float | None — multiplied into base save cooldown.
#                     None = save action is fully blocked.
#   Result is clamped to >= 0 (so a CD can reach 0 = instant reuse).
#   apply_vow() returns -1.0 to signal a blocked action.
#
# Stack Vow (charge-based, handled separately):
#   - Cooldown is ×2 the user's base role cooldown.
#   - Kill and save each have their own pool of up to 3 charges.
#   - Each charge regenerates independently after one full CD period.
#   - A user can bank all 3 charges and spend them back-to-back.
# =========================

BINDING_VOWS = {
    "Destruction Vow": {
        "kill_multiplier": 3.0,
        "save_multiplier": 1.0,
        "description": "Kill CDs ×3",
    },
    "Healing Vow": {
        "kill_multiplier": None,   # Cannot kill — blocked entirely
        "save_multiplier": 0.02,   # ÷50
        "description": "Cannot kill / Save CDs ÷50",
    },
    "Hakari Vow": {
        # No multipliers — cooldown behavior is unchanged.
        # On kill: 36% chance to mute the target for 4m11s, 64% chance to mute yourself for 90s.
        # Save GIFs work normally with no special effect.
        "kill_multiplier": 1.0,
        "save_multiplier": 1.0,
        "description": "Kill GIFs: 36% mute target 4m11s / 64% mute yourself 90s",
    },
    "Stack Vow": {
        # Handled via charge system — multipliers not used here
        "description": "Kill & save CDs ×3, but bank up to 3 uses of each independently",
    },
}

STACK_VOW_MULTIPLIER = 3.0
STACK_VOW_MAX_CHARGES = 3

# Charge state for Stack Vow users.
# { user_id: { "kill": [datetime, ...], "save": [datetime, ...] } }
# Each datetime records when that charge was consumed.
# A charge regenerates after one full CD period has elapsed since consumption.
stack_vow_charges: dict[int, dict[str, list[datetime]]] = {}


def get_active_vow(author_roles: list[str]) -> str | None:
    """
    Returns the single Binding Vow the user holds, or None if they have none.
    Returns "CONFLICT" if they somehow hold multiple vows.
    """
    held = [vow for vow in BINDING_VOWS if vow in author_roles]
    if len(held) == 0:
        return None
    if len(held) == 1:
        return held[0]
    return "CONFLICT"


def apply_vow(base_cooldown_hours: float, action: str, vow_name: str | None) -> float:
    """
    Applies a standard Binding Vow multiplier to a base cooldown.
    Stack Vow is NOT handled here — use the stack_vow_* helpers instead.

    Returns -1.0 if the action is blocked by the vow.
    Result is otherwise clamped to >= 0.
    """
    if not vow_name or vow_name in ("CONFLICT", "Stack Vow") or vow_name not in BINDING_VOWS:
        return max(0.0, base_cooldown_hours)

    vow = BINDING_VOWS[vow_name]
    multiplier = vow["kill_multiplier"] if action == "kill" else vow["save_multiplier"]

    if multiplier is None:
        return -1.0  # Action blocked

    return max(0.0, base_cooldown_hours * multiplier)


def format_vow_label(vow_name: str | None) -> str:
    """Returns ' [Vow Name]' for display, or '' if no vow / conflict."""
    if not vow_name or vow_name == "CONFLICT":
        return ""
    return f" [{vow_name}]"


# ---- Stack Vow charge helpers ----

def _get_active_charge_timestamps(user_id: int, action: str, cd_hours: float, now: datetime) -> list[datetime]:
    """
    Returns the list of still-on-cooldown charge timestamps for the given action.
    Expired charges (older than one CD period) are pruned in-place.
    """
    user_data = stack_vow_charges.setdefault(user_id, {"kill": [], "save": []})
    regen_window = timedelta(hours=cd_hours)
    active = [t for t in user_data[action] if now - t < regen_window]
    user_data[action] = active
    return active


def stack_vow_available_charges(user_id: int, action: str, cd_hours: float, now: datetime) -> int:
    """Returns how many charges the user can spend right now."""
    active = _get_active_charge_timestamps(user_id, action, cd_hours, now)
    return max(0, STACK_VOW_MAX_CHARGES - len(active))


def stack_vow_consume_charge(user_id: int, action: str, now: datetime):
    """Records that the user spent one charge at the given time."""
    user_data = stack_vow_charges.setdefault(user_id, {"kill": [], "save": []})
    user_data[action].append(now)


def stack_vow_next_regen(user_id: int, action: str, cd_hours: float, now: datetime) -> timedelta | None:
    """
    Returns the time until the next charge regenerates.
    Returns None if the user is already at max charges.
    """
    active = _get_active_charge_timestamps(user_id, action, cd_hours, now)
    if not active:
        return None  # Already at max — no regen pending
    oldest = min(active)
    regen_at = oldest + timedelta(hours=cd_hours)
    return max(timedelta(0), regen_at - now)


# =========================
# OTHER CONFIG
# =========================

DEGLOVE_ROLES = {"Shit ass mod", "Good Moderator Morning!"}

DEADLY_SENTENCES_CHANNEL = "deadly-sentences"
MODLOG_CHANNEL = "modlog"
BANNED_ROLE_NAME = "Banned"

DEGLOVINGS_FILE = "active_deglovings.json"

def save_deglovings():
    data = {
        str(member_id): {
            "role_ids": entry["role_ids"],
            "message_id": entry["message_id"],
            "channel_id": entry["channel_id"],
            "reglove_at": entry["reglove_at"],
        }
        for member_id, entry in active_deglovings.items()
    }
    with open(DEGLOVINGS_FILE, "w") as f:
        json.dump(data, f)

def load_deglovings():
    if not os.path.exists(DEGLOVINGS_FILE):
        return {}
    with open(DEGLOVINGS_FILE, "r") as f:
        return json.load(f)

# { member_id: { "role_ids": [int], "message_id": int, "channel_id": int, "task": Task, "reglove_at": str } }
active_deglovings = {}

# Fully independent cooldown timers — kill and save never affect each other.
last_kill_used: dict[int, datetime] = {}
last_save_used: dict[int, datetime] = {}


# =========================
# ERROR LOGGING HELPER
# =========================

async def log_error(guild, label: str, error: Exception):
    tb = traceback.format_exc()
    print(f"[ERROR] {label}: {error}\n{tb}")
    modlog = discord.utils.get(guild.text_channels, name=MODLOG_CHANNEL)
    if modlog:
        tb_trimmed = tb[-1500:] if len(tb) > 1500 else tb
        await modlog.send(
            f"⚠️ **Bot Error — {label}**\n"
            f"```{type(error).__name__}: {error}\n\n{tb_trimmed}```"
        )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    saved = load_deglovings()
    for member_id_str, entry in saved.items():
        member_id = int(member_id_str)
        reglove_at = datetime.fromisoformat(entry["reglove_at"])
        now = datetime.utcnow()
        remaining = (reglove_at - now).total_seconds()

        active_deglovings[member_id] = {
            "role_ids": entry["role_ids"],
            "message_id": entry["message_id"],
            "channel_id": entry["channel_id"],
            "reglove_at": entry["reglove_at"],
            "task": None,
        }

        async def scheduled_reglove(mid=member_id, secs=max(remaining, 0)):
            try:
                await asyncio.sleep(secs)
                guild = bot.guilds[0] if bot.guilds else None
                if guild and mid in active_deglovings:
                    member = guild.get_member(mid)
                    if member:
                        channel_id = active_deglovings[mid].get("channel_id")
                        announce_channel = guild.get_channel(channel_id) if channel_id else None
                        await reglove_member(guild, member, announce_channel)
                    else:
                        active_deglovings.pop(mid, None)
                        save_deglovings()
            except asyncio.CancelledError:
                pass
            except Exception as e:
                guild = bot.guilds[0] if bot.guilds else None
                if guild:
                    await log_error(guild, f"on_ready scheduled_reglove for {mid}", e)

        task = asyncio.create_task(scheduled_reglove())
        active_deglovings[member_id]["task"] = task
        print(f"[on_ready] Rebuilt deglove timer for member {member_id}, {max(remaining, 0):.0f}s remaining")


def parse_duration(duration_str):
    match = re.fullmatch(r"(\d+)(s|m|h|d)", duration_str.strip().lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return value * multipliers[unit]


async def reglove_member(guild, member, announce_channel):
    entry = active_deglovings.pop(member.id, None)
    if not entry:
        return
    save_deglovings()

    task = entry.get("task")
    if task and not task.done():
        task.cancel()

    saved_role_ids = entry.get("role_ids", [])
    message_id = entry.get("message_id")
    channel_id = entry.get("channel_id")

    banned_role = discord.utils.get(guild.roles, name=BANNED_ROLE_NAME)
    if banned_role and banned_role in member.roles:
        try:
            await member.remove_roles(banned_role, reason="Deglove period ended")
        except Exception as e:
            await log_error(guild, f"reglove: remove Banned role from {member}", e)

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
            await modlog.send(
                f"⚠️ **Reglove warning:** No roles could be restored for {member.mention}. "
                f"Saved IDs: `{saved_role_ids}`"
            )

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
    author_roles = {role.name for role in ctx.author.roles}

    if not (author_roles & DEGLOVE_ROLES):
        await ctx.send(f"{ctx.author.mention}, you don't have permission to deglove.")
        return

    if not ctx.message.reference:
        await ctx.send("You need to reply to someone's message to deglove them.")
        return

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

    if member.id in active_deglovings:
        await ctx.send(f"{member.mention} is already degloved.")
        return

    banned_role = discord.utils.get(ctx.guild.roles, name=BANNED_ROLE_NAME)
    if not banned_role:
        await ctx.send(f'Could not find a role named "{BANNED_ROLE_NAME}". Make sure it exists.')
        return

    bot_top_role = ctx.guild.me.top_role
    saved_role_ids = [
        r.id for r in member.roles
        if r != ctx.guild.default_role and not r.managed and r < bot_top_role
    ]
    print(f"[deglove] Saving role IDs for {member}: {saved_role_ids}")

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

    active_deglovings[member.id] = {
        "role_ids": saved_role_ids,
        "message_id": message_id,
        "channel_id": channel_id,
        "task": None,
        "reglove_at": (datetime.utcnow() + timedelta(seconds=seconds)).isoformat(),
    }
    save_deglovings()

    async def scheduled_reglove():
        try:
            await asyncio.sleep(seconds)
            if member.id in active_deglovings:
                await reglove_member(ctx.guild, member, ctx.channel)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            await log_error(ctx.guild, f"scheduled_reglove for {member}", e)

    task = asyncio.create_task(scheduled_reglove())
    active_deglovings[member.id]["task"] = task


@bot.command(name="reglove")
async def reglove(ctx):
    author_roles = {role.name for role in ctx.author.roles}

    if not (author_roles & DEGLOVE_ROLES):
        await ctx.send(f"{ctx.author.mention}, you don't have permission to reglove.")
        return

    if not ctx.message.reference:
        await ctx.send("You need to reply to the message of the person you want to reglove.")
        return

    try:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    except Exceptio