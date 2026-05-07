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
    "Bum": 4,
    "Rat": 7,
    "Chud": 10,
    "Otis BFF ❤️": 10,
    "Shit ass mod": 10,
    "Good Moderator Morning!": 999
}

# =========================
# PER-SERVER DEFAULT COOLDOWN
#
# Stored in server_settings.json as { "guild_id": { "default_cooldown": float } }
# Used when a user has none of the named roles in ROLE_COOLDOWNS.
# Mods (anyone with manage_guild or manage_roles) can change it with !cooldowns <hours>.
# Default is 12 hours.
# =========================

SERVER_SETTINGS_FILE = "server_settings.json"
DEFAULT_COOLDOWN_HOURS = 12.0

# { guild_id (int): { "default_cooldown": float } }
server_settings: dict[int, dict] = {}


def load_server_settings():
    if not os.path.exists(SERVER_SETTINGS_FILE):
        return {}
    with open(SERVER_SETTINGS_FILE, "r") as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}


def save_server_settings():
    with open(SERVER_SETTINGS_FILE, "w") as f:
        json.dump({str(k): v for k, v in server_settings.items()}, f, indent=2)


def get_default_cooldown(guild_id: int) -> float:
    return server_settings.get(guild_id, {}).get("default_cooldown", DEFAULT_COOLDOWN_HOURS)


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
        "description": "Kill & save CDs ×2, but bank up to 3 uses of each independently",
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
    held = [vow for vow in BINDING_VOWS if vow in author_roles]
    if len(held) == 0:
        return None
    if len(held) == 1:
        return held[0]
    return "CONFLICT"


def apply_vow(base_cooldown_hours: float, action: str, vow_name: str | None) -> float:
    if not vow_name or vow_name in ("CONFLICT", "Stack Vow") or vow_name not in BINDING_VOWS:
        return max(0.0, base_cooldown_hours)

    vow = BINDING_VOWS[vow_name]
    multiplier = vow["kill_multiplier"] if action == "kill" else vow["save_multiplier"]

    if multiplier is None:
        return -1.0  # Action blocked

    return max(0.0, base_cooldown_hours * multiplier)


def format_vow_label(vow_name: str | None) -> str:
    if not vow_name or vow_name == "CONFLICT":
        return ""
    return f" [{vow_name}]"


# ---- Stack Vow charge helpers ----

def _get_active_charge_timestamps(user_id: int, action: str, cd_hours: float, now: datetime) -> list[datetime]:
    user_data = stack_vow_charges.setdefault(user_id, {"kill": [], "save": []})
    regen_window = timedelta(hours=cd_hours)
    active = [t for t in user_data[action] if now - t < regen_window]
    user_data[action] = active
    return active


def stack_vow_available_charges(user_id: int, action: str, cd_hours: float, now: datetime) -> int:
    active = _get_active_charge_timestamps(user_id, action, cd_hours, now)
    return max(0, STACK_VOW_MAX_CHARGES - len(active))


def stack_vow_consume_charge(user_id: int, action: str, now: datetime):
    user_data = stack_vow_charges.setdefault(user_id, {"kill": [], "save": []})
    user_data[action].append(now)


def stack_vow_next_regen(user_id: int, action: str, cd_hours: float, now: datetime) -> timedelta | None:
    active = _get_active_charge_timestamps(user_id, action, cd_hours, now)
    if not active:
        return None
    oldest = min(active)
    regen_at = oldest + timedelta(hours=cd_hours)
    return max(timedelta(0), regen_at - now)


# =========================
# OTHER CONFIG
# =========================

MODLOG_CHANNEL = "modlog"

# Fully independent cooldown timers — kill and save never affect each other.
last_kill_used: dict[int, datetime] = {}
last_save_used: dict[int, datetime] = {}

# Pending clashes: { attacker_message_id: { "attacker": Member, "defender": Member, "channel": TextChannel, "timeout_duration": int, "attacker_vow_str": str, "task": Task } }
pending_clashes: dict[int, dict] = {}


# =========================
# CLASH HELPERS
# =========================

def get_clash_tickets(member_roles: list[str]) -> int:
    best = 0
    for role_name in member_roles:
        tickets = CLASH_TICKETS.get(role_name, 0)
        if tickets > best:
            best = tickets
    return best if best > 0 else 1


def resolve_clash(attacker_tickets: int, defender_tickets: int) -> bool:
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
    global server_settings
    server_settings = load_server_settings()
    print(f"Logged in as {bot.user}")


# =========================
# !cooldowns COMMAND
# Mods can set the default cooldown (in hours) for users with no recognized role.
# =========================

@bot.command(name="cooldowns")
async def set_cooldown(ctx, hours: str = None):
    # Check mod permissions
    if not ctx.author.guild_permissions.manage_roles and not ctx.author.guild_permissions.manage_guild:
        await ctx.send(f"{ctx.author.mention}, you need the Manage Roles permission to change the default cooldown.")
        return

    if hours is None:
        current = get_default_cooldown(ctx.guild.id)
        await ctx.send(f"Current default cooldown for users with no role: **{current}h**\nUsage: `!cooldowns <hours>` (e.g. `!cooldowns 6`)")
        return

    try:
        new_cd = float(hours)
        if new_cd < 0:
            raise ValueError
    except ValueError:
        await ctx.send("Invalid value. Usage: `!cooldowns <hours>` — must be a non-negative number (e.g. `!cooldowns 6` or `!cooldowns 0.5`)")
        return

    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["default_cooldown"] = new_cd
    save_server_settings()

    await ctx.send(f"✅ Default cooldown for roleless users set to **{new_cd}h**")


# =========================
# !help COMMAND
# =========================

@bot.command(name="help")
async def help_command(ctx):
    default_cd = get_default_cooldown(ctx.guild.id)

    embed = discord.Embed(
        title="Bot Help",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="How it works",
        value=(
            "Reply to someone's message with a **kill GIF** to time them out (90s).\n"
            "Reply to a timed-out user's message with a **save GIF** to free them early.\n"
            "If the target replies with a kill GIF within 5 seconds, a **Clash** happens — "
            "whoever has more clash tickets wins."
        ),
        inline=False
    )

    role_lines = "\n".join(
        f"**{role}** — {cd}h CD" if cd > 0 else f"**{role}** — no cooldown 😈"
        for role, cd in ROLE_COOLDOWNS.items()
    )
    embed.add_field(
        name="Role Cooldowns",
        value=role_lines,
        inline=False
    )

    embed.add_field(
        name="No matching role?",
        value=f"Default cooldown: **{default_cd}h** (mods can change this with `!cooldowns <hours>`)",
        inline=False
    )

    clash_lines = "\n".join(
        f"**{role}** — {tickets} tickets"
        for role, tickets in CLASH_TICKETS.items()
    )
    embed.add_field(
        name="Clash Tickets",
        value=clash_lines + "\n*No role: 1 ticket*",
        inline=False
    )

    vow_lines = "\n".join(
        f"**{name}** — {data['description']}"
        for name, data in BINDING_VOWS.items()
    )
    embed.add_field(
        name="Binding Vows",
        value=vow_lines,
        inline=False
    )

    embed.add_field(
        name="Commands",
        value=(
            "`!help` — show this message\n"
            "`@bot` — check your current cooldown status\n"
            "`!cooldowns [hours]` — view or set the default cooldown *(mods only)*"
        ),
        inline=False
    )

    await ctx.send(embed=embed)


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
        default_cd = get_default_cooldown(message.guild.id)

        # Determine base CD: use best role if available, otherwise server default
        if valid_roles:
            best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
            base_cd = ROLE_COOLDOWNS[best_role]
            role_label = best_role
        else:
            best_role = None
            base_cd = default_cd
            role_label = f"default ({default_cd}h)"

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
                f"{message.author.mention}, ({role_label}{vow_str}) you have no cooldown 😈"
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
                f"{message.author.mention}, ({role_label} [Stack Vow]) CD: {sv_cd:.4g}h per charge\n"
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
            await message.channel.send(
                f"{message.author.mention}, ({role_label}{vow_str}) cooldown: {format_cd(kill_cd, last_kill)}"
            )
        else:
            await message.channel.send(
                f"{message.author.mention}, ({role_label}{vow_str})\n"
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
            clash_data["task"].cancel()

            attacker = clash_data["attacker"]
            defender = clash_data["defender"]
            timeout_duration = clash_data["timeout_duration"]
            attacker_vow_str = clash_data["attacker_vow_str"]

            attacker_roles = [r.name for r in attacker.roles]
            defender_roles = [r.name for r in defender.roles]
            attacker_tickets = get_clash_tickets(attacker_roles)
            defender_tickets = get_clash_tickets(defender_roles)

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
    default_cd = get_default_cooldown(message.guild.id)

    # Determine base CD and label
    if valid_roles:
        best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
        base_cd = ROLE_COOLDOWNS[best_role]
        role_label = best_role
    else:
        best_role = None
        base_cd = default_cd
        role_label = f"default ({default_cd}h)"

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

        stack_vow_consume_charge(user_id, action, now)
        remaining_after = available - 1
        vow_str = f" [Stack Vow | {remaining_after}/{STACK_VOW_MAX_CHARGES} {action} charges left]"

    # =========================
    # STANDARD VOW: multiplier-based cooldown check
    # =========================
    else:
        effective_cd = apply_vow(base_cd, action, vow)
        vow_str = format_vow_label(vow)

        if effective_cd == -1.0:
            await message.channel.send(
                f"{message.author.mention}, your {vow} forbids you from killing. 🩹"
            )
            return

        last = last_kill_used.get(user_id) if action == "kill" else last_save_used.get(user_id)

        if effective_cd > 0 and last:
            if now - last < timedelta(hours=effective_cd):
                remaining = timedelta(hours=effective_cd) - (now - last)
                await message.channel.send(
                    f"{message.author.mention}, ({role_label}{vow_str}) cooldown remaining: "
                    f"{str(remaining).split('.')[0]}"
                )
                return

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
            attacker = message.author
            defender = member_to_timeout
            kill_message_id = message.id

            async def clash_or_timeout():
                try:
                    await asyncio.sleep(CLASH_WINDOW_SECONDS)
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
