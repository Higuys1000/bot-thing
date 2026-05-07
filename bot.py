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
    "https://tenor.com/view/yuta-yuta-okkotsu-jujutsu-kaisen-jjk-anime-gif-18377052283740449128",
    "https://tenor.com/view/mahito-mechamaru-jujutsu-kaisen-fight-jjk-gif-13293311021769477196",
    "https://tenor.com/view/naoya-jujutsu-kaisen-jujutsu-kaisen-season-3-maki-maki-zenin-gif-13642749527516671169",
    "https://tenor.com/view/fnaf-fnaf4-freddy-freddy-fazbear-nightmare-freddy-gif-24525113",
    "https://tenor.com/view/gojo-gojo-satoru-gojo-season-2-hip-thrust-reaction-gif-10399129046512126318",
    "https://tenor.com/view/megumi-fushiguro-fushi-guro-megumi-fushiguro-mahoraga-gif-92941122665464082",
    "https://tenor.com/view/gojo-geto-suguru-gojo-satoru-kenjaku-prison-realm-gif-5425478000746110355",
    "https://tenor.com/view/killer-queen-bites-the-dust-gif-22628088",
    "https://tenor.com/view/kokichi-muta-vs-mahito-strong-gif-720433162054802054",
    "https://tenor.com/view/dhruv-dhruv-lakdawalla-yuta-yuta-jjk-jujutsu-kaisen-gif-5938354836642012188",
    "https://tenor.com/view/david-martinez-mag-dump-blick-david-blicktinez-cyberpunk-gif-15887120100692089819",
    "https://tenor.com/view/sukuna-mahoraga-feint-cleave-dismantle-gif-13544783209250889853",
    "https://tenor.com/view/l-fap-los-gif-4732809238593749211",
    "https://tenor.com/view/goku-black-goku-black-shush-zamasu-gif-5057528923283903671",
    "https://klipy.com/gifs/bowser-fart-3",
    "https://tenor.com/view/jujutsu-kaisen-jjk-anime-capped-through-the-dome-gif-14392986505181725674",
    "https://tenor.com/view/punch-gif-11426619910221365543",
    "https://tenor.com/view/naoya-naoya-zenin-choso-jujutsu-kaisen-anime-gif-7928374921195313568",
    "https://tenor.com/view/maki-zenin-perfect-preparation-jjk-jujutsu-kaisen-jjk-s3-gif-9326251013866579573",
    "https://tenor.com/view/homelander-the-boys-black-noir-homelander-kill-homelander-and-black-noir-gif-26428738",
    "https://tenor.com/view/move-move-outta-way-get-the-fuck-out-of-my-way-push-past-push-person-over-gif-1520289070937279009",
    "https://tenor.com/view/makima-bang-gif-21311375",
    "https://tenor.com/view/open-season-shaw-deer-run-over-meme-gif-12251156658227451666",
    "https://tenor.com/view/mahito-curse-yuji-black-flash-kokusen-gif-15575468419961292171",
    "https://tenor.com/view/baki-yujiro-hanma-yujiro-gif-17873266028238581190",
    "https://tenor.com/view/jjk-jjk-s2-jjk-season-2-jujutsu-kaisen-jujutsu-kaisen-s2-gif-7964484372484357392",
    "https://tenor.com/view/chainsaw-man-kon-katana-man-samurai-sword-katana-devil-gif-27183536",
    "https://tenor.com/view/israel-palpatine-netanyahu-benjamin-netanyahu-star-wars-gif-3844839225312481092",
    "https://tenor.com/view/epstein-diddy-epstein-vs-diddy-domain-expansion-gif-16007208464559825312",
    "https://tenor.com/view/sinisterbart-ryomen-sukuna-jjk-gojo-satoru-gojo-gif-3626682422769793141",
    "https://tenor.com/view/baby-screaming-polvo-fuego-fire-baby-meme-gif-10034606886425990272",
    "https://tenor.com/view/vaporized-family-guy-joe-swanson-death-gif-3135054252562901052",
    "https://tenor.com/view/yuji-jjk-yuji12-gif-678454138725285911",
    "https://tenor.com/view/megumi-fushiguro-fushiguro-megumi-megumi-fushiguro-toji-fushiguro-gif-14764636942047131755",
    "https://tenor.com/view/nanami-nanami-kento-haruta-shigemo-haruta-shigemo-gif-17001883660336100989",
    "https://tenor.com/view/reggie-megumi-divine-dog-totality-jujutsu-kaisen-gif-16803502898948526832",
    "https://tenor.com/view/megumi-reggie-star-max-elephant-jujutsu-kaisen-gif-17848841313289141645",
    "https://tenor.com/view/hazenoki-iori-iori-hazenoki-reggie-reggie-star-gif-15470925985641586022",
    "https://tenor.com/view/ryu-ishigori-kurourushi-and-uro-takako-gif-10500026154609357939"
]

UNTIMEOUT_GIFS = [
    "https://tenor.com/view/doctor-manhattan-watchmen-marvel-gif-21030500",
    "https://klipy.com/gifs/doctor-manhattan-watchmen",
    "https://tenor.com/view/revive-gif-23866294",
    "https://tenor.com/view/kenjaku-jujutsu-kaisen-mahito-geto-suguru-geto-gif-3390342049104401664"
    "https://tenor.com/view/todo-jjk-jujutsu-kaisen-shibuya-arc-mahito-gif-11933159284027340768",
    "https://tenor.com/view/the-boys-homelander-season-5-tung-tung-tung-sahur-tung-tung-sahur-gif-7005128074439649595",
    "https://tenor.com/view/he-has-me-gif-13654467562542512739",
    "https://tenor.com/view/ryomen-sukuna-sukuna-ryomen-sukuna-ryomen-megumi-fushiguro-gif-6088274754816185868",
    "https://tenor.com/view/jjk-jujutsu-kaisen-yuta-yuta-okkotsu-okkotsu-gif-5353918859104233890",
    "https://tenor.com/view/higuruma-jjk-jujutsu-kaisen-jujutsukaisen-retrial-gif-5462736760420847458",
    "https://tenor.com/view/overwatch-gif-9248765",
    "https://tenor.com/view/jjk-jujutsu-kaisen-season-2-nobara-kugisaki-itadori-yuji-gif-2211818749172123653",
    "https://tenor.com/view/lol-gif-23256631",
    "https://tenor.com/view/ohmmm-cartman-gif-10082733958201247483",
    "https://tenor.com/view/thumbs-up-gif-12921332806977950807",
    "https://tenor.com/view/ryu-ryu-ishigori-yuta-yuta-okkotsu-jujutsu-kaisen-gif-8459438190665096786",
    "https://tenor.com/view/cat-cats-rigby-rigby-the-cat-rigby-cat-gif-12777307700590236451",
    "https://tenor.com/view/israel-israel-superhero-am-yisrael-chai-israeli-flag-gif-16069792012856888850",
    "https://tenor.com/view/american-gif-27543431",
    "https://tenor.com/view/peter-griffin-gif-12194285640126683264",
    "https://tenor.com/view/yuta-okkotsu-vs-ryu-ishigori-apply-gif-48656283840648220",
    "https://tenor.com/view/big-brain-cell-gif-11009529955506497046",
    "https://tenor.com/view/yourrage-chair-bounce-yourrage-bounce-yourrage-gif-6221615739239256499"
]

CLASH_GIF = "https://tenor.com/view/gojo-satoru-sukuna-gif-14001663626498053725"
CLASH_WINDOW_SECONDS = 5

TIMEOUT_SECONDS = 90

ROLE_COOLDOWNS = {
    "Bum": 18,
    "Rat": 9,
    "Chud": 4,
    "Otis BFF ❤️": 4,
    "Shit ass mod": 0,
    "Good Moderator Morning!": 0
}

CLASH_TICKETS = {
    "Bum": 1,
    "Rat": 2,
    "Chud": 3,
    "Otis BFF ❤️": 3,
    "Shit ass mod": 3,
    "Good Moderator Morning!": 999
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

STACK_VOW_MULTIPLIER = 2.0
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

# Pending clashes: { attacker_message_id: { "attacker": Member, "defender": Member, "channel": TextChannel, "timeout_duration": int, "attacker_vow_str": str, "task": Task } }
pending_clashes: dict[int, dict] = {}


# =========================
# CLASH HELPERS
# =========================

def get_clash_tickets(member_roles: list[str]) -> int:
    """Returns the clash ticket count for a member based on their best role."""
    best = 0
    for role_name in member_roles:
        tickets = CLASH_TICKETS.get(role_name, 0)
        if tickets > best:
            best = tickets
    return best if best > 0 else 1  # Default to 1 if no clash role found


def resolve_clash(attacker_tickets: int, defender_tickets: int) -> bool:
    """Returns True if attacker wins, False if defender wins."""
    total = attacker_tickets + defender_tickets
    return random.randint(1, total) <= attacker_tickets


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
    # BOT MENTION → SHOW COOLDOWN STATUS
    # =========================
    if bot.user in message.mentions:
        valid_roles = [r for r in author_roles if r in ROLE_COOLDOWNS]

        if not valid_roles:
            await message.channel.send(
                f"{message.author.mention}, you don't have any cooldown role."
            )
            return

        best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
        base_cd = ROLE_COOLDOWNS[best_role]
        vow = get_active_vow(author_roles)
        vow_str = format_vow_label(vow)
        now = datetime.utcnow()
        user_id = message.author.id

        if vow == "CONFLICT":
            await message.channel.send(
                f"{message.author.mention}, ⚠️ you have multiple Binding Vow roles — "
                f"vows are being ignored until this is resolved."
            )
            return

        if base_cd == 0:
            await message.channel.send(
                f"{message.author.mention}, ({best_role}{vow_str}) you have no cooldown 😈"
            )
            return

        # --- Stack Vow: show charge status ---
        if vow == "Stack Vow":
            sv_cd = base_cd * STACK_VOW_MULTIPLIER

            def charge_status(action: str) -> str:
                available = stack_vow_available_charges(user_id, action, sv_cd, now)
                next_regen = stack_vow_next_regen(user_id, action, sv_cd, now)
                charge_pips = "🟢" * available + "🔴" * (STACK_VOW_MAX_CHARGES - available)
                if next_regen:
                    return f"{charge_pips} (next regen in **{str(next_regen).split('.')[0]}**)"
                return charge_pips

            await message.channel.send(
                f"{message.author.mention}, ({best_role} [Stack Vow]) CD: {sv_cd:.4g}h per charge\n"
                f"☠️ Kill charges: {charge_status('kill')}\n"
                f"💚 Save charges: {charge_status('save')}"
            )
            return

        # --- Standard vows: show independent kill/save cooldowns ---
        kill_cd = apply_vow(base_cd, "kill", vow)
        save_cd = apply_vow(base_cd, "save", vow)
        last_kill = last_kill_used.get(user_id)
        last_save = last_save_used.get(user_id)

        def format_cd(hours: float, last: datetime | None) -> str:
            if hours == -1.0:
                return "blocked 🚫"
            if hours <= 0:
                return "ready instantly ✅"
            td = timedelta(hours=hours)
            if not last or now - last >= td:
                return "ready ✅"
            remaining = td - (now - last)
            return f"**{str(remaining).split('.')[0]}** remaining"

        if kill_cd == save_cd and last_kill == last_save:
            # Both timers are identical — show a single line for cleanliness
            await message.channel.send(
                f"{message.author.mention}, ({best_role}{vow_str}) cooldown: {format_cd(kill_cd, last_kill)}"
            )
        else:
            await message.channel.send(
                f"{message.author.mention}, ({best_role}{vow_str})\n"
                f"☠️ Kill CD: {format_cd(kill_cd, last_kill)}\n"
                f"💚 Save CD: {format_cd(save_cd, last_save)}"
            )
        return

    # MUST BE A REPLY TO TRIGGER GIF ACTIONS
    if not message.reference:
        await bot.process_commands(message)
        return

    content = message.content
    is_kill_gif = any(gif in content for gif in TARGET_GIFS)
    is_save_gif = any(gif in content for gif in UNTIMEOUT_GIFS)

    # =========================
    # CLASH CHECK — defender replying to a pending clash
    # =========================
    if is_kill_gif and message.reference.message_id in pending_clashes:
        clash_data = pending_clashes.pop(message.reference.message_id, None)
        if clash_data and message.author.id == clash_data["defender"].id:
            # Cancel the pending timeout task
            clash_data["task"].cancel()

            attacker = clash_data["attacker"]
            defender = clash_data["defender"]
            timeout_duration = clash_data["timeout_duration"]
            attacker_vow_str = clash_data["attacker_vow_str"]

            attacker_roles = [r.name for r in attacker.roles]
            defender_roles = [r.name for r in defender.roles]
            attacker_tickets = get_clash_tickets(attacker_roles)
            defender_tickets = get_clash_tickets(defender_roles)

            # Stamp cooldown for defender
            now = datetime.utcnow()
            last_kill_used[defender.id] = now

            await message.channel.send(CLASH_GIF)

            attacker_wins = resolve_clash(attacker_tickets, defender_tickets)
            if attacker_wins:
                loser = defender
                winner = attacker
            else:
                loser = attacker
                winner = defender

            await asyncio.sleep(3)

            try:
                await loser.timeout(
                    discord.utils.utcnow() + timedelta(seconds=timeout_duration)
                )
                await message.channel.send(
                    f"{winner.mention} WON\n{loser.mention} get timed out"
                )
            except Exception as e:
                await log_error(message.guild, f"clash: timeout {loser}", e)

            await bot.process_commands(message)
            return

    if not (is_kill_gif or is_save_gif):
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
    base_cd = ROLE_COOLDOWNS[best_role]
    vow = get_active_vow(author_roles)
    now = datetime.utcnow()
    user_id = message.author.id
    action = "kill" if is_kill_gif else "save"

    if vow == "CONFLICT":
        await message.channel.send(
            f"{message.author.mention}, ⚠️ you have multiple Binding Vow roles — "
            f"vows are being ignored until this is resolved."
        )
        vow = None

    # =========================
    # STACK VOW: charge-based cooldown check
    # =========================
    if vow == "Stack Vow":
        sv_cd = base_cd * STACK_VOW_MULTIPLIER
        available = stack_vow_available_charges(user_id, action, sv_cd, now)

        if available == 0:
            next_regen = stack_vow_next_regen(user_id, action, sv_cd, now)
            await message.channel.send(
                f"{message.author.mention}, [Stack Vow] no {action} charges left — "
                f"next charge in **{str(next_regen).split('.')[0]}**"
            )
            return

        # Charge available — consume it and proceed to the action
        stack_vow_consume_charge(user_id, action, now)
        remaining_after = available - 1
        vow_str = f" [Stack Vow | {remaining_after}/{STACK_VOW_MAX_CHARGES} {action} charges left]"

    # =========================
    # STANDARD VOW: multiplier-based cooldown check
    # =========================
    else:
        effective_cd = apply_vow(base_cd, action, vow)
        vow_str = format_vow_label(vow)

        # Vow blocks this action entirely
        if effective_cd == -1.0:
            await message.channel.send(
                f"{message.author.mention}, your {vow} forbids you from killing. 🩹"
            )
            return

        # Check and enforce the independent timer for this specific action
        last = last_kill_used.get(user_id) if action == "kill" else last_save_used.get(user_id)

        if effective_cd > 0 and last:
            if now - last < timedelta(hours=effective_cd):
                remaining = timedelta(hours=effective_cd) - (now - last)
                await message.channel.send(
                    f"{message.author.mention}, ({best_role}{vow_str}) cooldown remaining: "
                    f"{str(remaining).split('.')[0]}"
                )
                return

        # Stamp only the timer for this action — the other is unaffected
        if action == "kill":
            last_kill_used[user_id] = now
        else:
            last_save_used[user_id] = now

    # =========================
    # SAVE GIF → UNTIMEOUT
    # =========================
    if is_save_gif:
        if not member_to_timeout.timed_out_until:
            await message.channel.send("They're not even timed out bro 💀")
            return

        remaining = member_to_timeout.timed_out_until - discord.utils.utcnow()

        if remaining.total_seconds() <= 90:
            try:
                await member_to_timeout.timeout(None)
                await message.channel.send(
                    f"{member_to_timeout.mention} has been freed early by "
                    f"{message.author.mention}{vow_str}"
                )
            except Exception as e:
                await message.channel.send("Failed to remove timeout.")
                await log_error(
                    message.guild,
                    f"untimeout: remove timeout from {member_to_timeout}",
                    e
                )
        else:
            await message.channel.send(
                f"Too long left on timeout ({int(remaining.total_seconds())}s). Can't save them."
            )

        await bot.process_commands(message)
        return

    # =========================
    # KILL GIF → TIMEOUT (with clash window)
    # =========================
    if is_kill_gif:
        timeout_duration = 180 if vow == "Destruction Vow" else TIMEOUT_SECONDS

        # Hakari Vow: gamble on every kill — 36% hit, 64% self-mute
        if vow == "Hakari Vow":
            if random.random() < 0.36:
                try:
                    await member_to_timeout.timeout(
                        discord.utils.utcnow() + timedelta(seconds=251)
                    )
                    await message.channel.send(
                        f"🎰 **JACKPOT!** {member_to_timeout.mention} has been muted for 4m11s "
                        f"by {message.author.mention} [Hakari Vow] lmao"
                    )
                except Exception as e:
                    await message.channel.send(f"Failed to timeout {member_to_timeout.mention}.")
                    await log_error(message.guild, f"hakari win: timeout {member_to_timeout}", e)
            else:
                author_member = message.guild.get_member(message.author.id)
                if author_member:
                    try:
                        await author_member.timeout(
                            discord.utils.utcnow() + timedelta(seconds=90)
                        )
                        await message.channel.send(
                            f"💀 {message.author.mention} [Hakari Vow] lost the gamble and muted themselves for 90s lmaooo"
                        )
                    except Exception as e:
                        await message.channel.send("Failed to apply self-mute.")
                        await log_error(message.guild, f"hakari loss: timeout {author_member}", e)
                else:
                    await message.channel.send("Couldn't find you in the server to apply the self-mute??")
        else:
            # Register pending clash and wait CLASH_WINDOW_SECONDS before timing out
            attacker = message.author
            defender = member_to_timeout
            kill_message_id = message.id

            async def clash_or_timeout():
                try:
                    await asyncio.sleep(CLASH_WINDOW_SECONDS)
                    # If still pending (no clash happened), apply timeout normally
                    if kill_message_id in pending_clashes:
                        pending_clashes.pop(kill_message_id, None)
                        try:
                            await defender.timeout(
                                discord.utils.utcnow() + timedelta(seconds=timeout_duration)
                            )
                            await message.channel.send(
                                f"{defender.mention} has been timed out for {timeout_duration}s "
                                f"by {attacker.mention}{vow_str} lmao"
                            )
                        except Exception as e:
                            await message.channel.send(f"Failed to timeout {defender.mention}.")
                            await log_error(message.guild, f"timeout: apply timeout to {defender}", e)
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    await log_error(message.guild, f"clash_or_timeout for {defender}", e)

            task = asyncio.create_task(clash_or_timeout())
            pending_clashes[kill_message_id] = {
                "attacker": attacker,
                "defender": defender,
                "channel": message.channel,
                "timeout_duration": timeout_duration,
                "attacker_vow_str": vow_str,
                "task": task,
            }

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
    if isinstance(error, commands.CommandNotFound):
        return
    await log_error(ctx.guild, f"command error in #{ctx.channel.name} by {ctx.author}", error)


bot.run(os.getenv("TOKEN"))
