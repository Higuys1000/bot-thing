import random
import discord
import aiohttp
from aiohttp import web
from discord.ext import commands
from discord import app_commands
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

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

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
    "https://tenor.com/view/ryu-ishigori-kurourushi-and-uro-takako-gif-10500026154609357939",
    "https://tenor.com/view/indian-meme-indian-guy-indian-meme-tuff-gif-17449687295227939133",
    "https://tenor.com/view/ryu-ryu-ishigori-yuta-yuta-okkotsu-jujutsu-kaisen-gif-8459438190665096786",
    "https://tenor.com/view/yuta-okkotsu-vs-kurourushi-it-recovers-gif-3802753654661782155",
    "https://tenor.com/view/jujutsu-kaisen-jjk-pseudo-geto-kills-mahito-gif-9807305680862769559",
    "https://tenor.com/view/hakari-kinji-hakari-punch-jjk-hakari-hakari-mad-hakari-angry-gif-5937175376042208357",
    "https://tenor.com/view/hasan-dog-hasan-piker-electrocuted-gif-2794498358389000074",
    "https://tenor.com/view/reze-chainsaw-man-reze-arc-choking-rain-gif-12346418835128647519",
    "https://tenor.com/view/gd-factory-clips-andre-drummond-andre-drummond-peace-sign-nba-nba-peace-sign-gif-13367487476147293282",
    "https://tenor.com/view/kawhi-kawhi-leonard-kawhi-thunder-kawhi-lightning-kawhi-intuit-dome-gif-13900975799455910081",
    "https://tenor.com/view/zeng-this-guy-right-here-this-right-here-point-out-point-gif-23913867",
    "https://tenor.com/view/lebron-james-lebron-dunk-thunder-in-your-face-gif-15586712",
    "https://tenor.com/view/itadori-angry-jujutsu-kaisen-episode12-gif-19653132",
    "https://tenor.com/view/todo-jjk-jujutsu-kaisen-shibuya-arc-mahito-gif-11933159284027340768",
    "https://tenor.com/view/d9luxe-gif-4267568862040013492",
    "https://tenor.com/view/kinblood-lebron-dunk-gif-12278440"
]

UNTIMEOUT_GIFS = [
    "https://tenor.com/view/doctor-manhattan-watchmen-marvel-gif-21030500",
    "https://klipy.com/gifs/doctor-manhattan-watchmen",
    "https://tenor.com/view/revive-gif-23866294",
    "https://tenor.com/view/kenjaku-jujutsu-kaisen-mahito-geto-suguru-geto-gif-3390342049104401664",
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
    "https://tenor.com/view/cat-cats-rigby-rigby-the-cat-rigby-cat-gif-12777307700590236451",
    "https://tenor.com/view/israel-israel-superhero-am-yisrael-chai-israeli-flag-gif-16069792012856888850",
    "https://tenor.com/view/american-gif-27543431",
    "https://tenor.com/view/peter-griffin-gif-12194285640126683264",
    "https://tenor.com/view/yuta-okkotsu-vs-ryu-ishigori-apply-gif-48656283840648220",
    "https://tenor.com/view/big-brain-cell-gif-11009529955506497046",
    "https://tenor.com/view/yourrage-chair-bounce-yourrage-bounce-yourrage-gif-6221615739239256499",
    "https://tenor.com/view/kirkified-kirk-charlie-kirk-jujutsu-kaisen-lobotomy-kaisen-gif-903841159067133314",
    "https://tenor.com/view/virtual-god-bless-god-bless-god-bless-blessing-gif-11439379459411225580",
    "https://tenor.com/view/yuta-yuta-okkotsu-rika-jujutsu-kaisen-yuta-jjk-gif-6106836881169266148",
    "https://tenor.com/view/naoya-zenin-naoya-meme-gif-6148282862012625994",
    "https://tenor.com/view/omni-man-sad-invincible-gif-9211102013467947727",
    "https://tenor.com/view/mercy-overwatch-come-here-gif-14280244",
    "https://tenor.com/view/lamelo-ball-lamelo-zesty-gif-3374658710119383750",
    "https://tenor.com/view/storm-rain-raining-gif-12250202288703677838",
    "https://tenor.com/view/death-of-the-self-gay-fluff-shigadeku-shigaraki-deku-gif-24033047",
    "https://tenor.com/view/gay-anime-anime-gay-gif-18237425560170880188"
]

CLASH_GIFS = [
    "https://tenor.com/view/gojo-satoru-sukuna-gif-14001663626498053725",
    "https://tenor.com/view/ryu-jjk-ryu-ishigori-granite-blast-yuta-yuta-okkotsu-gif-3023270638744891240",
    "https://tenor.com/view/naoya-zenin-sorcerer-grade-special-1-vs-maki-zenin-gif-14997796067865413406",
    "https://tenor.com/view/dio-vs-jotaro-gif-18462062",
    "https://tenor.com/view/jujutsu-kaisen-yuta-ryu-okkotsu-fight-gif-10244605119238677045",
]

CLASH_GIFS_GMM = [
    "https://tenor.com/view/gojo-domain-expansion-gif-19197982",
    "https://tenor.com/view/josuke-higashikata-josuke-crazy-diamond-stando-jotaro-gif-26746962",
    "https://tenor.com/view/ichigo-kurosaki-aizen-vs-ichigo-bleach-gif-14055522",
    "https://tenor.com/view/baki-slap-baki-slap-gif-2511379337117214059",
]

MIRACLE_BLOCK_GIF = "https://cdn.discordapp.com/attachments/1395472869991121078/1497282590267281448/runningtrue.gif"

CLASH_WINDOW_SECONDS = 5
TIMEOUT_SECONDS = 90

ROLE_COOLDOWNS = {
    "Bum": 18,
    "Rat": 9,
    "Chud": 4,
    "Otis BFF \u2764\ufe0f": 4,
    "Shit ass mod": 0,
    "Good Moderator Morning!": 0,
    "guh tester": 0
}

CLASH_TICKETS = {
    "Bum": 4,
    "Rat": 7,
    "Chud": 10,
    "Otis BFF \u2764\ufe0f": 10,
    "Shit ass mod": 10,
    "Good Moderator Morning!": 999
}

# =========================
# PER-SERVER DEFAULT COOLDOWN
# =========================

SERVER_SETTINGS_FILE = "server_settings.json"
DEFAULT_COOLDOWN_HOURS = 12.0
server_settings: dict[int, dict] = {}

# =========================
# VOTE SYSTEM
# =========================

VOTE_WEBHOOK_PORT = int(os.getenv("PORT", os.getenv("VOTE_WEBHOOK_PORT", "5000")))
VOTE_WEBHOOK_AUTH = os.getenv("VOTE_WEBHOOK_AUTH", "")
VOTE_DURATION_HOURS = 12.0
VOTE_DISCOUNT = 0.75

vote_timestamps: dict[int, datetime] = {}


def has_active_vote(user_id: int) -> bool:
    ts = vote_timestamps.get(user_id)
    if not ts:
        return False
    return datetime.utcnow() - ts < timedelta(hours=VOTE_DURATION_HOURS)


def vote_expires_in(user_id: int) -> timedelta | None:
    ts = vote_timestamps.get(user_id)
    if not ts:
        return None
    remaining = timedelta(hours=VOTE_DURATION_HOURS) - (datetime.utcnow() - ts)
    return remaining if remaining.total_seconds() > 0 else None


def apply_vote_discount(hours: float, user_id: int) -> float:
    if hours <= 0 or hours == -1.0:
        return hours
    if has_active_vote(user_id):
        return hours * VOTE_DISCOUNT
    return hours


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


def get_default_role(guild_id: int) -> int | None:
    return server_settings.get(guild_id, {}).get("default_role_id", None)


# =========================
# BINDING VOW SYSTEM
# =========================

BINDING_VOWS = {
    "Destruction Vow": {
        "kill_multiplier": 3.0,
        "save_multiplier": 1.0,
        "description": "Kill CDs \u00d73",
    },
    "Healing Vow": {
        "kill_multiplier": None,
        "save_multiplier": 0.02,
        "description": "Cannot kill / Save CDs \u00f750",
    },
    "Hakari Vow": {
        "kill_multiplier": 1.0,
        "save_multiplier": 1.0,
        "description": "Kill GIFs go through clash window. No clash: 36% mute target 4m11s / 64% mute yourself 90s. Win clash: 50/50 gamble.",
    },
    "Stack Vow": {
        "description": "Kill & save CDs \u00d72, but bank up to 3 uses of each independently",
    },
    "Miracle Vow": {
        "kill_multiplier": 2.5,
        "save_multiplier": 2.5,
        "description": "2.5x CD. Collect miracles when someone on CD tries to guh you, when you save someone, or when you get saved. 2 miracles = auto-block a guh. Max 6. You only deal 30s timeout.",
    },
    "Random Vow": {
        "kill_multiplier": 1.0,
        "save_multiplier": 1.0,
        "description": "After each kill, timeout duration is random and kill CD is randomized 1-21h. Save CD randomized 2-10h independently.",
    },
    "Bitchout Vow": {
        "kill_multiplier": None,
        "save_multiplier": None,
        "description": "Cannot kill or save anyone. Immune to being guhed (except by Good Moderator Morning).",
    },
    "Ragebait Vow": {
        "kill_multiplier": 1.0,
        "save_multiplier": 1.0,
        "description": "Kill GIFs don't timeout the target — instead adds 1.5x to their kill CD. Ragebait ability CD is 0.5x your role CD. Save works normally.",
    },
}

STACK_VOW_MULTIPLIER = 2.0
STACK_VOW_MAX_CHARGES = 3
stack_vow_charges: dict[int, dict[str, list[datetime]]] = {}
bot_start_time: datetime = datetime.utcnow()
# Track which users have been initialized post-restart for Stack Vow
stack_vow_initialized: set[int] = set()

MIRACLE_MAX = 6
MIRACLE_BLOCK_COST = 2
miracle_counts: dict[int, int] = {}

# { user_id: datetime } — last time a miracle was gained from a failed timeout
miracle_gain_cooldown: dict[int, datetime] = {}

MIRACLE_GAIN_COOLDOWN_HOURS = 1.0

# { user_id: { "kill": float | None, "save": float | None } }
random_vow_cds: dict[int, dict[str, float | None]] = {}

# { user_id: datetime } — last time Ragebait ability was used
ragebait_last_used: dict[int, datetime] = {}

# { user_id: float } — current kill CD multiplier added by Ragebait (stacks as hours added)
ragebait_kill_cd_added: dict[int, float] = {}


def get_active_vow(author_roles: list[str]) -> str | None:
    held = [vow for vow in BINDING_VOWS if vow in author_roles]
    if len(held) == 0:
        return None
    if len(held) == 1:
        return held[0]
    return "CONFLICT"


def apply_vow(base_cooldown_hours: float, action: str, vow_name: str | None) -> float:
    if not vow_name or vow_name in ("CONFLICT", "Stack Vow", "Random Vow", "Miracle Vow", "Bitchout Vow") or vow_name not in BINDING_VOWS:
        if vow_name == "Miracle Vow":
            return max(0.0, base_cooldown_hours * 2.5)
        if vow_name == "Bitchout Vow":
            return -1.0
        return max(0.0, base_cooldown_hours)
    vow = BINDING_VOWS[vow_name]
    multiplier = vow["kill_multiplier"] if action == "kill" else vow["save_multiplier"]
    if multiplier is None:
        return -1.0
    return max(0.0, base_cooldown_hours * multiplier)


def format_vow_label(vow_name: str | None) -> str:
    if not vow_name or vow_name == "CONFLICT":
        return ""
    return f" [{vow_name}]"


def _get_active_charge_timestamps(user_id: int, action: str, cd_hours: float, now: datetime) -> list[datetime]:
    user_data = stack_vow_charges.setdefault(user_id, {"kill": [], "save": []})
    # On first access after a restart, pre-consume 2 charges so user starts with 1
    init_key = f"{user_id}_{action}"
    if init_key not in stack_vow_initialized:
        stack_vow_initialized.add(init_key)
        if len(user_data[action]) == 0:
            # Pre-consume 2 charges using timestamps that won't expire for a full CD period
            user_data[action] = [now, now]
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


def get_miracle_count(user_id: int) -> int:
    return miracle_counts.get(user_id, 0)


def add_miracle(user_id: int) -> int:
    current = miracle_counts.get(user_id, 0)
    if current >= MIRACLE_MAX:
        return -1
    miracle_counts[user_id] = current + 1
    return miracle_counts[user_id]


def can_gain_miracle_from_failed_timeout(user_id: int) -> bool:
    """Returns True if the user can gain a miracle from a failed timeout (1h cooldown)."""
    last = miracle_gain_cooldown.get(user_id)
    if not last:
        return True
    return datetime.utcnow() - last >= timedelta(hours=MIRACLE_GAIN_COOLDOWN_HOURS)


def record_miracle_gain_from_failed_timeout(user_id: int):
    miracle_gain_cooldown[user_id] = datetime.utcnow()


def consume_miracles(user_id: int, amount: int):
    current = miracle_counts.get(user_id, 0)
    miracle_counts[user_id] = max(0, current - amount)


def get_ragebait_cd(user_id: int, base_cd: float) -> float:
    """Returns the ragebait ability cooldown (0.5x role CD)."""
    return base_cd * 0.5


def is_ragebait_on_cd(user_id: int, base_cd: float, now: datetime) -> bool:
    last = ragebait_last_used.get(user_id)
    if not last:
        return False
    return now - last < timedelta(hours=get_ragebait_cd(user_id, base_cd))


def get_ragebait_remaining(user_id: int, base_cd: float, now: datetime) -> timedelta:
    last = ragebait_last_used.get(user_id)
    if not last:
        return timedelta(0)
    cd = timedelta(hours=get_ragebait_cd(user_id, base_cd))
    return max(timedelta(0), cd - (now - last))


def get_random_vow_cd(user_id: int, action: str) -> float | None:
    return random_vow_cds.get(user_id, {}).get(action, None)


def set_random_vow_cd(user_id: int, action: str):
    if user_id not in random_vow_cds:
        random_vow_cds[user_id] = {"kill": None, "save": None}
    if action == "kill":
        # 1-21h, weighted towards lower values
        random_vow_cds[user_id]["kill"] = random.triangular(1.0, 21.0, 3.0)
    else:
        # 2-10h, weighted towards lower values
        random_vow_cds[user_id]["save"] = random.triangular(2.0, 10.0, 3.0)


def roll_random_vow_timeout() -> int:
    # 10s-8m (480s), weighted towards lower end
    return int(random.triangular(10, 480, 30))


# =========================
# OTHER CONFIG
# =========================

MODLOG_CHANNEL = "modlog"
last_kill_used: dict[int, datetime] = {}
last_save_used: dict[int, datetime] = {}
pending_clashes: dict[int, dict] = {}


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


def is_on_cooldown(user_id: int, action: str, effective_cd: float, now: datetime) -> bool:
    if effective_cd <= 0:
        return False
    last = last_kill_used.get(user_id) if action == "kill" else last_save_used.get(user_id)
    if not last:
        return False
    # If ragebait override exists for kill, use that CD instead
    if action == "kill" and user_id in ragebait_kill_cd_added:
        override_cd = ragebait_kill_cd_added[user_id]
        elapsed = now - last
        if elapsed >= timedelta(hours=override_cd):
            del ragebait_kill_cd_added[user_id]  # expired, clear it
            return now - last < timedelta(hours=effective_cd)
        return True
    return now - last < timedelta(hours=effective_cd)


def pick_clash_gif(attacker_roles: list[str], defender_roles: list[str]) -> str:
    if "Good Moderator Morning!" in attacker_roles or "Good Moderator Morning!" in defender_roles:
        return random.choice(CLASH_GIFS_GMM)
    return random.choice(CLASH_GIFS)


def is_gmm_clash(attacker_roles: list[str], defender_roles: list[str]) -> bool:
    return "Good Moderator Morning!" in attacker_roles or "Good Moderator Morning!" in defender_roles


async def log_error(guild, label: str, error: Exception):
    tb = traceback.format_exc()
    print(f"[ERROR] {label}: {error}\n{tb}")
    modlog = discord.utils.get(guild.text_channels, name=MODLOG_CHANNEL)
    if modlog:
        tb_trimmed = tb[-1500:] if len(tb) > 1500 else tb
        await modlog.send(
            f"\u26a0\ufe0f **Bot Error \u2014 {label}**\n"
            f"```{type(error).__name__}: {error}\n\n{tb_trimmed}```"
        )


# =========================
# SHARED LOGIC
# =========================

def build_help_embed(guild_id: int) -> discord.Embed:
    default_cd = get_default_cooldown(guild_id)
    default_role_id = get_default_role(guild_id)
    embed = discord.Embed(title="Bot Help", color=discord.Color.blurple())
    embed.add_field(
        name="How it works",
        value=(
            "Reply to someone's message with a **kill GIF** to time them out (90s).\n"
            "Reply to a timed-out user's message with a **save GIF** to free them early.\n"
            "If the target replies with a kill GIF within 5 seconds, a **Clash** happens \u2014 "
            "whoever has more clash tickets wins."
        ),
        inline=False
    )
    default_role_str = f"<@&{default_role_id}>" if default_role_id else "none set (everyone can use GIFs)"
    embed.add_field(
        name="Access & Cooldowns",
        value=(
            f"Default role to use GIFs: {default_role_str}\n"
            f"Default cooldown: **{default_cd}h**\n"
            "*Role-specific cooldowns are configured per server.*"
        ),
        inline=False
    )
    vow_lines = "\n".join(
        f"**{name}** \u2014 {data['description']}"
        for name, data in BINDING_VOWS.items()
    )
    embed.add_field(name="Binding Vows", value=vow_lines, inline=False)
    embed.add_field(
        name="\U0001f4e5 Vote for a Cooldown Discount",
        value=(
            "Vote for the bot to get **25% off your cooldowns** for 12 hours!\n"
            "[Click here to vote](https://discordbotlist.com/bots/funnything/upvote)"
        ),
        inline=False
    )
    embed.add_field(
        name="Commands",
        value=(
            "`/help` or `!help` \u2014 show this message\n"
            "`/vote` or `!vote` \u2014 get the vote link for a 25% cooldown discount\n"
            "`/cooldown` or `@bot` \u2014 check your current cooldown status\n"
            "`/cooldowns [hours]` or `!cooldowns [hours]` \u2014 view or set the default cooldown *(mods only)*\n"
            "`/setdefaultrole [@role]` or `!setdefaultrole [@role]` \u2014 set the role needed to use GIFs *(mods only)*\n"
            "`/setdefaultrole clear` or `!setdefaultrole clear` \u2014 remove the role requirement *(mods only)*"
        ),
        inline=False
    )
    return embed


def build_cooldown_status(member: discord.Member, guild_id: int) -> str:
    author_roles = [role.name for role in member.roles]
    valid_roles = [r for r in author_roles if r in ROLE_COOLDOWNS]
    default_cd = get_default_cooldown(guild_id)

    if valid_roles:
        best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
        base_cd = ROLE_COOLDOWNS[best_role]
        role_label = best_role
    else:
        base_cd = default_cd
        role_label = f"default ({default_cd}h)"

    vow = get_active_vow(author_roles)
    vow_str = format_vow_label(vow)
    now = datetime.utcnow()
    user_id = member.id

    if vow == "CONFLICT":
        return (
            f"{member.mention}, \u26a0\ufe0f you have multiple Binding Vow roles \u2014 "
            "vows are being ignored until this is resolved."
        )

    if base_cd == 0:
        return f"{member.mention}, ({role_label}{vow_str}) you have no cooldown \U0001f608"

    if vow == "Stack Vow":
        sv_cd = base_cd * STACK_VOW_MULTIPLIER

        def charge_status(action: str) -> str:
            available = stack_vow_available_charges(user_id, action, sv_cd, now)
            next_regen = stack_vow_next_regen(user_id, action, sv_cd, now)
            charge_pips = "\U0001f7e2" * available + "\U0001f534" * (STACK_VOW_MAX_CHARGES - available)
            if next_regen:
                return f"{charge_pips} (next regen in **{str(next_regen).split('.')[0]}**)"
            return charge_pips

        return (
            f"{member.mention}, ({role_label} [Stack Vow]) CD: {sv_cd:.4g}h per charge\n"
            f"\u2620\ufe0f Kill charges: {charge_status('kill')}\n"
            f"\U0001f49a Save charges: {charge_status('save')}"
        )

    if vow == "Miracle Vow":
        miracles = get_miracle_count(user_id)
        kill_cd = apply_vote_discount(base_cd * 2.5, user_id)
        save_cd = apply_vote_discount(base_cd * 2.5, user_id)
        last_kill = last_kill_used.get(user_id)
        last_save = last_save_used.get(user_id)

        def format_cd_miracle(hours: float, last: datetime | None) -> str:
            td = timedelta(hours=hours)
            if not last or now - last >= td:
                return "ready \u2705"
            remaining = td - (now - last)
            return f"**{str(remaining).split('.')[0]}** remaining"

        return (
            f"{member.mention}, ({role_label} [Miracle Vow]) \u2728 Miracles: {miracles}/{MIRACLE_MAX}\n"
            f"\u2620\ufe0f Kill CD: {format_cd_miracle(kill_cd, last_kill)}\n"
            f"\U0001f49a Save CD: {format_cd_miracle(save_cd, last_save)}"
        )

    if vow == "Random Vow":
        kill_cd_val = get_random_vow_cd(user_id, "kill")
        save_cd_val = get_random_vow_cd(user_id, "save")
        last_kill = last_kill_used.get(user_id)
        last_save = last_save_used.get(user_id)

        def format_random_cd(cd_val: float | None, last: datetime | None) -> str:
            if cd_val is None or not last:
                return "ready \u2705"
            td = timedelta(hours=cd_val)
            if now - last >= td:
                return "ready \u2705"
            remaining = td - (now - last)
            return f"**{str(remaining).split('.')[0]}** remaining (rolled {cd_val:.2f}h)"

        return (
            f"{member.mention}, ({role_label} [Random Vow])\n"
            f"\u2620\ufe0f Kill CD: {format_random_cd(kill_cd_val, last_kill)}\n"
            f"\U0001f49a Save CD: {format_random_cd(save_cd_val, last_save)}"
        )

    if vow == "Bitchout Vow":
        return f"{member.mention}, you're a bitch but a guh free bitch atleast"

    if vow == "Ragebait Vow":
        ragebait_cd = get_ragebait_cd(user_id, base_cd)
        save_cd = apply_vote_discount(base_cd, user_id)
        last_save = last_save_used.get(user_id)

        def format_ragebait_cd(hours: float, last: datetime | None) -> str:
            if not last or now - last >= timedelta(hours=hours):
                return "ready \u2705"
            remaining = timedelta(hours=hours) - (now - last)
            return f"**{str(remaining).split('.')[0]}** remaining"

        ragebait_remaining = get_ragebait_remaining(user_id, base_cd, now)
        ragebait_status = "ready \u2705" if ragebait_remaining.total_seconds() == 0 else f"**{str(ragebait_remaining).split('.')[0]}** remaining"
        return (
            f"{member.mention}, ({role_label} [Ragebait Vow])\n"
            f"\U0001f621 Ragebait CD ({ragebait_cd:.4g}h): {ragebait_status}\n"
            f"\U0001f49a Save CD ({base_cd}h): {format_ragebait_cd(save_cd, last_save)}"
        )

    kill_cd = apply_vote_discount(apply_vow(base_cd, "kill", vow), user_id)
    save_cd = apply_vote_discount(apply_vow(base_cd, "save", vow), user_id)
    last_kill = last_kill_used.get(user_id)
    last_save = last_save_used.get(user_id)
    voted = has_active_vote(user_id)
    vote_label = " \U0001f4e5 25% off" if voted else ""

    def format_cd(hours: float, last: datetime | None) -> str:
        if hours == -1.0:
            return "blocked \U0001f6ab"
        if hours <= 0:
            return "ready instantly \u2705"
        td = timedelta(hours=hours)
        if not last or now - last >= td:
            return "ready \u2705"
        remaining = td - (now - last)
        return f"**{str(remaining).split('.')[0]}** remaining"

    if kill_cd == save_cd and last_kill == last_save:
        return f"{member.mention}, ({role_label}{vow_str}{vote_label}) cooldown: {format_cd(kill_cd, last_kill)}"
    return (
        f"{member.mention}, ({role_label}{vow_str}{vote_label})\n"
        f"\u2620\ufe0f Kill CD: {format_cd(kill_cd, last_kill)}\n"
        f"\U0001f49a Save CD: {format_cd(save_cd, last_save)}"
    )


# =========================
# STARTUP
# =========================

@bot.event
async def on_ready():
    global server_settings
    server_settings = load_server_settings()
    print(f"Logged in as {bot.user}")
    print("Slash commands are registered globally. Use !sync to push any changes to Discord.")
    await start_webhook_server()


@bot.command(name="sync")
@commands.is_owner()
async def sync_commands(ctx):
    await ctx.send("Syncing slash commands globally... this can take up to an hour to show everywhere.")
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"\u2705 Synced {len(synced)} slash command(s) globally.")
    except Exception as e:
        await ctx.send(f"\u274c Sync failed: {e}")


# =========================
# PREFIX COMMANDS
# =========================

@bot.command(name="help")
async def prefix_help(ctx):
    await ctx.send(embed=build_help_embed(ctx.guild.id))


@bot.command(name="cooldowns")
async def prefix_cooldowns(ctx, hours: str = None):
    if not ctx.author.guild_permissions.manage_roles and not ctx.author.guild_permissions.manage_guild:
        await ctx.send(f"{ctx.author.mention}, you need the Manage Roles permission to change the default cooldown.")
        return
    if hours is None:
        current = get_default_cooldown(ctx.guild.id)
        await ctx.send(f"Current default cooldown: **{current}h**\nUsage: `!cooldowns <hours>`")
        return
    try:
        new_cd = float(hours)
        if new_cd < 0:
            raise ValueError
    except ValueError:
        await ctx.send("Invalid value. Must be a non-negative number (e.g. `!cooldowns 6` or `!cooldowns 0.5`)")
        return
    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["default_cooldown"] = new_cd
    save_server_settings()
    await ctx.send(f"\u2705 Default cooldown for roleless users set to **{new_cd}h**")


@bot.command(name="setdefaultrole")
async def prefix_setdefaultrole(ctx, *, role_input: str = None):
    if not ctx.author.guild_permissions.manage_roles and not ctx.author.guild_permissions.manage_guild:
        await ctx.send(f"{ctx.author.mention}, you need the Manage Roles permission to do that.")
        return
    if not role_input:
        current_id = get_default_role(ctx.guild.id)
        if current_id:
            role = ctx.guild.get_role(current_id)
            role_str = role.mention if role else f"unknown role (ID {current_id})"
        else:
            role_str = "none (everyone can use GIFs)"
        await ctx.send(f"Current default GIF role: {role_str}\nUsage: `!setdefaultrole @Role` or `!setdefaultrole clear`")
        return
    if role_input.strip().lower() == "clear":
        if ctx.guild.id in server_settings:
            server_settings[ctx.guild.id].pop("default_role_id", None)
            save_server_settings()
        await ctx.send("\u2705 Default role requirement cleared. Everyone can now use GIFs.")
        return
    role = None
    if ctx.message.role_mentions:
        role = ctx.message.role_mentions[0]
    else:
        role = discord.utils.find(lambda r: r.name.lower() == role_input.lower(), ctx.guild.roles)
    if not role:
        await ctx.send("Couldn't find that role. Try mentioning it with @, or use `!setdefaultrole clear` to remove the requirement.")
        return
    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["default_role_id"] = role.id
    save_server_settings()
    await ctx.send(f"\u2705 Default GIF role set to **{role.name}**. Only members with this role (or a named cooldown role) can use GIFs.")


# =========================
# SLASH COMMANDS
# =========================

@bot.tree.command(name="help", description="Show how the bot works, all cooldowns, vows, and commands")
async def slash_help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_help_embed(interaction.guild_id))


@bot.tree.command(name="cooldown", description="Check your current kill and save cooldown status")
async def slash_cooldown(interaction: discord.Interaction):
    msg = build_cooldown_status(interaction.user, interaction.guild_id)
    await interaction.response.send_message(msg)


@bot.tree.command(name="cooldowns", description="View or set the default cooldown for roleless users (mods only)")
@app_commands.describe(hours="New default cooldown in hours (e.g. 6 or 0.5). Leave blank to view current value.")
async def slash_cooldowns(interaction: discord.Interaction, hours: float = None):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need the Manage Roles permission to change the default cooldown.", ephemeral=True)
        return
    if hours is None:
        current = get_default_cooldown(interaction.guild_id)
        await interaction.response.send_message(f"Current default cooldown: **{current}h**\nUse `/cooldowns hours:<value>` to change it.", ephemeral=True)
        return
    if hours < 0:
        await interaction.response.send_message("Cooldown must be a non-negative number.", ephemeral=True)
        return
    if interaction.guild_id not in server_settings:
        server_settings[interaction.guild_id] = {}
    server_settings[interaction.guild_id]["default_cooldown"] = hours
    save_server_settings()
    await interaction.response.send_message(f"\u2705 Default cooldown for roleless users set to **{hours}h**")


@bot.tree.command(name="setdefaultrole", description="Set the role required to use GIFs (mods only)")
@app_commands.describe(role="The role to require. Leave blank to view current setting.")
async def slash_setdefaultrole(interaction: discord.Interaction, role: discord.Role = None):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need the Manage Roles permission to do that.", ephemeral=True)
        return
    if role is None:
        current_id = get_default_role(interaction.guild_id)
        if current_id:
            role_obj = interaction.guild.get_role(current_id)
            role_str = role_obj.mention if role_obj else f"unknown role (ID {current_id})"
        else:
            role_str = "none (everyone can use GIFs)"
        await interaction.response.send_message(f"Current default GIF role: {role_str}", ephemeral=True)
        return
    if interaction.guild_id not in server_settings:
        server_settings[interaction.guild_id] = {}
    server_settings[interaction.guild_id]["default_role_id"] = role.id
    save_server_settings()
    await interaction.response.send_message(f"\u2705 Default GIF role set to **{role.name}**.")


@bot.tree.command(name="cleardefaultrole", description="Remove the role requirement for using GIFs (mods only)")
async def slash_cleardefaultrole(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need the Manage Roles permission to do that.", ephemeral=True)
        return
    if interaction.guild_id in server_settings:
        server_settings[interaction.guild_id].pop("default_role_id", None)
        save_server_settings()
    await interaction.response.send_message("\u2705 Default role requirement cleared. Everyone can now use GIFs.")


# =========================
# VOTE COMMANDS
# =========================

VOTE_EMBED_COLOR = discord.Color.gold()


def build_vote_embed(user_id: int) -> discord.Embed:
    embed = discord.Embed(
        title="\U0001f4e5 Vote for a Cooldown Discount!",
        description=(
            "Vote for the bot on Discord Bot List and get **25% off your cooldowns** for 12 hours!\n\n"
            "[\U0001f517 Click here to vote](https://discordbotlist.com/bots/funnything/upvote)"
        ),
        color=VOTE_EMBED_COLOR,
        url="https://discordbotlist.com/bots/funnything/upvote"
    )
    if has_active_vote(user_id):
        expires = vote_expires_in(user_id)
        expires_str = str(expires).split('.')[0] if expires else "soon"
        embed.add_field(name="\u2705 Your vote is active!", value=f"You have 25% off your cooldowns. Expires in **{expires_str}**.", inline=False)
    else:
        embed.add_field(name="No active vote", value="Vote now to unlock your discount!", inline=False)
    return embed


@bot.command(name="vote")
async def prefix_vote(ctx):
    await ctx.send(embed=build_vote_embed(ctx.author.id))


@bot.tree.command(name="vote", description="Get the vote link for 25% off your cooldowns for 12 hours")
async def slash_vote(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_vote_embed(interaction.user.id))


# =========================
# VOTE WEBHOOK SERVER
# =========================

async def handle_dbl_webhook(request: web.Request) -> web.Response:
    auth = request.headers.get("Authorization", "")
    if VOTE_WEBHOOK_AUTH and auth != VOTE_WEBHOOK_AUTH:
        return web.Response(status=401, text="Unauthorized")
    try:
        data = await request.json()
    except Exception:
        return web.Response(status=400, text="Bad request")
    user_id_str = data.get("id") or data.get("user")
    if not user_id_str:
        return web.Response(status=400, text="No user ID in payload")
    try:
        user_id = int(user_id_str)
    except ValueError:
        return web.Response(status=400, text="Invalid user ID")
    vote_timestamps[user_id] = datetime.utcnow()
    print(f"[vote] Recorded vote for user {user_id}")
    try:
        user = await bot.fetch_user(user_id)
        if user:
            dm_embed = discord.Embed(
                title="\U0001f4e5 Thanks for voting!",
                description=(
                    "You now have **25% off your cooldowns** for the next 12 hours. Nice.\n\n"
                    "[Vote again after 12 hours](https://discordbotlist.com/bots/funnything/upvote)"
                ),
                color=VOTE_EMBED_COLOR
            )
            await user.send(embed=dm_embed)
    except Exception as e:
        print(f"[vote] Could not DM user {user_id}: {e}")
    return web.Response(status=200, text="OK")


async def start_webhook_server():
    app = web.Application()
    app.router.add_post("/dbl-webhook", handle_dbl_webhook)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", VOTE_WEBHOOK_PORT)
    await site.start()
    print(f"[vote] Webhook server listening on port {VOTE_WEBHOOK_PORT}")


# =========================
# MESSAGE EVENT
# =========================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_roles = [role.name for role in message.author.roles]

    if bot.user in message.mentions:
        valid_roles_for_mention = [r for r in author_roles if r in ROLE_COOLDOWNS]
        default_role_id_for_mention = get_default_role(message.guild.id)
        has_named_role_mention = bool(valid_roles_for_mention)
        has_required_role_mention = (
            default_role_id_for_mention is not None and
            any(r.id == default_role_id_for_mention for r in message.author.roles)
        )
        if default_role_id_for_mention is not None and not has_named_role_mention and not has_required_role_mention:
            required_role = message.guild.get_role(default_role_id_for_mention)
            role_name = required_role.name if required_role else "the required role"
            await message.channel.send(f"{message.author.mention}, you can only use GIFs if you have the **{role_name}** role.")
            return
        msg = build_cooldown_status(message.author, message.guild.id)
        await message.channel.send(msg)
        return

    if not message.reference:
        await bot.process_commands(message)
        return

    content = message.content
    is_kill_gif = any(gif in content for gif in TARGET_GIFS)
    is_save_gif = any(gif in content for gif in UNTIMEOUT_GIFS)

    # =========================
    # CLASH CHECK
    # =========================
    if is_kill_gif and message.reference.message_id in pending_clashes:
        clash_data = pending_clashes.get(message.reference.message_id)
        if clash_data and message.author.id == clash_data["defender"].id:
            defender = clash_data["defender"]
            defender_roles = [r.name for r in defender.roles]
            defender_vow = get_active_vow(defender_roles)
            valid_defender_roles = [r for r in defender_roles if r in ROLE_COOLDOWNS]
            default_cd = get_default_cooldown(message.guild.id)

            if valid_defender_roles:
                defender_best_role = min(valid_defender_roles, key=lambda r: ROLE_COOLDOWNS[r])
                defender_base_cd = ROLE_COOLDOWNS[defender_best_role]
            else:
                defender_base_cd = default_cd

            now = datetime.utcnow()

            if defender_vow == "Stack Vow":
                sv_cd = defender_base_cd * STACK_VOW_MULTIPLIER
                defender_available = stack_vow_available_charges(defender.id, "kill", sv_cd, now)
                defender_on_cd = defender_available == 0
                defender_cd_penalized = False
            elif defender_vow == "Random Vow":
                rv_cd = get_random_vow_cd(defender.id, "kill")
                last_kill = last_kill_used.get(defender.id)
                if rv_cd is None or last_kill is None:
                    defender_on_cd = False
                    defender_cd_penalized = False
                elif now - last_kill <= timedelta(seconds=CLASH_WINDOW_SECONDS + 1):
                    defender_on_cd = False
                    defender_cd_penalized = False
                else:
                    defender_on_cd = False  # can still clash but penalized
                    defender_cd_penalized = now - last_kill < timedelta(hours=rv_cd)
            elif defender_vow == "Bitchout Vow":
                defender_on_cd = True
                defender_cd_penalized = False
            elif defender_vow == "Miracle Vow":
                miracle_cd = apply_vote_discount(defender_base_cd * 2.5, defender.id)
                last_kill = last_kill_used.get(defender.id)
                if last_kill is None:
                    defender_on_cd = False
                    defender_cd_penalized = False
                elif now - last_kill <= timedelta(seconds=CLASH_WINDOW_SECONDS + 1):
                    defender_on_cd = False
                    defender_cd_penalized = False
                else:
                    defender_on_cd = False
                    defender_cd_penalized = now - last_kill < timedelta(hours=miracle_cd)
            else:
                effective_defender_cd = apply_vote_discount(apply_vow(defender_base_cd, "kill", defender_vow), defender.id)
                if effective_defender_cd <= 0:
                    defender_on_cd = False
                    defender_cd_penalized = False
                else:
                    last_kill = last_kill_used.get(defender.id)
                    if last_kill is None:
                        defender_on_cd = False
                        defender_cd_penalized = False
                    elif now - last_kill <= timedelta(seconds=CLASH_WINDOW_SECONDS + 1):
                        defender_on_cd = False
                        defender_cd_penalized = False
                    else:
                        still_on_cd = now - last_kill < timedelta(hours=effective_defender_cd)
                        defender_on_cd = False
                        defender_cd_penalized = still_on_cd

            if defender_on_cd:
                await bot.process_commands(message)
                return

            pending_clashes.pop(message.reference.message_id, None)
            clash_data["task"].cancel()

            attacker = clash_data["attacker"]
            timeout_duration = clash_data["timeout_duration"]
            attacker_vow = clash_data.get("attacker_vow")

            attacker_roles = [r.name for r in attacker.roles]
            attacker_tickets = get_clash_tickets(attacker_roles)
            defender_tickets = get_clash_tickets(defender_roles)

            # Apply penalty if defender was on CD (50% reduced win tickets)
            if defender_cd_penalized:
                defender_tickets = max(1, defender_tickets // 2)

            # Stamp CD for both attacker and defender
            last_kill_used[defender.id] = now
            last_kill_used[attacker.id] = now
            if attacker_vow == "Random Vow":
                set_random_vow_cd(attacker.id, "kill")
            if defender_vow == "Random Vow":
                set_random_vow_cd(defender.id, "kill")

            clash_gif = pick_clash_gif(attacker_roles, defender_roles)
            await message.channel.send(clash_gif)

            gmm_clash = is_gmm_clash(attacker_roles, defender_roles)
            if gmm_clash:
                await message.channel.send("can't clash with someone that strong buddy")

            attacker_wins = resolve_clash(attacker_tickets, defender_tickets)
            loser = defender if attacker_wins else attacker
            winner = attacker if attacker_wins else defender

            await asyncio.sleep(3)

            # If defender was on CD and wins, loser doesn't get timed out but CD resets
            if defender_cd_penalized and not attacker_wins:
                last_kill_used[loser.id] = now
                await message.channel.send(f"{winner.mention} WON (on CD clash)\n{loser.mention} escapes timeout but CD resets")
                await bot.process_commands(message)
                return

            if attacker_wins and attacker_vow == "Hakari Vow":
                if random.random() < 0.50:
                    try:
                        await defender.timeout(discord.utils.utcnow() + timedelta(seconds=251))
                        await message.channel.send(f"\U0001f3b0 **JACKPOT! (clash)** {defender.mention} muted for 4m11s by {attacker.mention} [Hakari Vow]")
                    except Exception as e:
                        await log_error(message.guild, f"hakari clash win: timeout {defender}", e)
                else:
                    try:
                        await attacker.timeout(discord.utils.utcnow() + timedelta(seconds=90))
                        await message.channel.send(f"\U0001f480 {attacker.mention} [Hakari Vow] won the clash but lost the gamble \u2014 muted 90s lmaooo")
                    except Exception as e:
                        await log_error(message.guild, f"hakari clash loss self: timeout {attacker}", e)
            elif not attacker_wins and defender_vow == "Hakari Vow":
                if random.random() < 0.50:
                    try:
                        await attacker.timeout(discord.utils.utcnow() + timedelta(seconds=251))
                        await message.channel.send(f"\U0001f3b0 **JACKPOT! (clash)** {attacker.mention} muted for 4m11s by {defender.mention} [Hakari Vow]")
                    except Exception as e:
                        await log_error(message.guild, f"hakari clash win: timeout {attacker}", e)
                else:
                    try:
                        await defender.timeout(discord.utils.utcnow() + timedelta(seconds=90))
                        await message.channel.send(f"\U0001f480 {defender.mention} [Hakari Vow] won the clash but lost the gamble \u2014 muted 90s lmaooo")
                    except Exception as e:
                        await log_error(message.guild, f"hakari clash loss self: timeout {defender}", e)
            else:
                # Miracle Vow winner deals 30s; Random Vow winner deals random duration
                if attacker_wins and attacker_vow == "Miracle Vow":
                    actual_duration = 30
                elif not attacker_wins and defender_vow == "Miracle Vow":
                    actual_duration = 30
                elif attacker_wins and attacker_vow == "Random Vow":
                    actual_duration = roll_random_vow_timeout()
                    set_random_vow_cd(attacker.id, "kill")
                elif not attacker_wins and defender_vow == "Random Vow":
                    actual_duration = roll_random_vow_timeout()
                    set_random_vow_cd(defender.id, "kill")
                else:
                    actual_duration = timeout_duration
                try:
                    await loser.timeout(discord.utils.utcnow() + timedelta(seconds=actual_duration))
                    await message.channel.send(f"{winner.mention} WON\n{loser.mention} get timed out")
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
    default_role_id = get_default_role(message.guild.id)

    has_named_role = bool(valid_roles)
    has_required_role = (
        default_role_id is not None and
        any(r.id == default_role_id for r in message.author.roles)
    )

    if default_role_id is not None and not has_named_role and not has_required_role:
        required_role = message.guild.get_role(default_role_id)
        role_name = required_role.name if required_role else "the required role"
        await message.channel.send(f"{message.author.mention}, you need the **{role_name}** role to use GIFs!")
        return

    if valid_roles:
        best_role = min(valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
        base_cd = ROLE_COOLDOWNS[best_role]
        role_label = best_role
    else:
        base_cd = default_cd
        role_label = f"default ({default_cd}h)"

    vow = get_active_vow(author_roles)
    now = datetime.utcnow()
    user_id = message.author.id
    action = "kill" if is_kill_gif else "save"

    if vow == "CONFLICT":
        await message.channel.send(
            f"{message.author.mention}, \u26a0\ufe0f you have multiple Binding Vow roles \u2014 "
            "vows are being ignored until this is resolved."
        )
        vow = None

    # =========================
    # BITCHOUT VOW
    # =========================
    if is_kill_gif:
        defender_roles = [r.name for r in member_to_timeout.roles]
        defender_vow = get_active_vow(defender_roles)
        if defender_vow == "Bitchout Vow" and "Good Moderator Morning!" not in author_roles:
            await message.channel.send(f"{member_to_timeout.mention} has **Bitchout Vow** \u2014 they're immune to guhs!")
            return

    if vow == "Bitchout Vow":
        if action == "kill":
            await message.channel.send("you're a bitch but a guh free bitch atleast")
        else:
            await message.channel.send(f"{message.author.mention}, your **Bitchout Vow** forbids you from saving. \U0001fa79")
        return

    # =========================
    # STACK VOW
    # =========================
    if vow == "Stack Vow":
        sv_cd = base_cd * STACK_VOW_MULTIPLIER
        available = stack_vow_available_charges(user_id, action, sv_cd, now)
        if available == 0:
            next_regen = stack_vow_next_regen(user_id, action, sv_cd, now)
            await message.channel.send(
                f"{message.author.mention}, [Stack Vow] no {action} charges left \u2014 "
                f"next charge in **{str(next_regen).split('.')[0]}**"
            )
            return
        stack_vow_consume_charge(user_id, action, now)
        remaining_after = available - 1
        vow_str = f" [Stack Vow | {remaining_after}/{STACK_VOW_MAX_CHARGES} {action} charges left]"

    # =========================
    # RANDOM VOW
    # =========================
    elif vow == "Random Vow":
        rv_cd = get_random_vow_cd(user_id, action)
        last = last_kill_used.get(user_id) if action == "kill" else last_save_used.get(user_id)
        if rv_cd is not None and last is not None and now - last < timedelta(hours=rv_cd):
            remaining = timedelta(hours=rv_cd) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, [Random Vow] cooldown remaining: **{str(remaining).split('.')[0]}** (rolled {rv_cd:.2f}h)"
            )
            return
        vow_str = " [Random Vow]"

    # =========================
    # MIRACLE VOW
    # =========================
    elif vow == "Miracle Vow":
        miracle_cd = apply_vote_discount(base_cd * 2.5, user_id)
        last = last_kill_used.get(user_id) if action == "kill" else last_save_used.get(user_id)
        if last and now - last < timedelta(hours=miracle_cd):
            remaining = timedelta(hours=miracle_cd) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, [Miracle Vow] cooldown remaining: **{str(remaining).split('.')[0]}**"
            )
            return
        vow_str = " [Miracle Vow]"

    elif vow == "Ragebait Vow":
        # Save uses normal role CD; kill ability CD is checked inside the kill gif section
        if action == "save":
            save_cd = apply_vote_discount(base_cd, user_id)
            last = last_save_used.get(user_id)
            if last and now - last < timedelta(hours=save_cd):
                remaining = timedelta(hours=save_cd) - (now - last)
                await message.channel.send(
                    f"{message.author.mention}, [Ragebait Vow] save cooldown remaining: **{str(remaining).split('.')[0]}**"
                )
                return
        vow_str = " [Ragebait Vow]"

    # =========================
    # STANDARD VOW
    # =========================
    else:
        effective_cd = apply_vote_discount(apply_vow(base_cd, action, vow), user_id)
        vow_str = format_vow_label(vow)
        vote_label = " \U0001f4e5 25% off" if has_active_vote(user_id) else ""

        if effective_cd == -1.0:
            await message.channel.send(f"{message.author.mention}, your {vow} forbids you from this action. \U0001fa79")
            return

        last = last_kill_used.get(user_id) if action == "kill" else last_save_used.get(user_id)

        if effective_cd > 0 and last:
            if now - last < timedelta(hours=effective_cd):
                remaining = timedelta(hours=effective_cd) - (now - last)

                # Miracle Vow: ANY attacker on CD trying to guh a Miracle Vow person gets them a miracle
                if is_kill_gif:
                    target_roles = [r.name for r in member_to_timeout.roles]
                    target_vow = get_active_vow(target_roles)
                    if target_vow == "Miracle Vow":
                        if not can_gain_miracle_from_failed_timeout(member_to_timeout.id):
                            await message.channel.send(
                                f"{message.author.mention}, ({role_label}{vow_str}) cooldown remaining: {str(remaining).split('.')[0]}"
                            )
                            return
                        new_count = add_miracle(member_to_timeout.id)
                        record_miracle_gain_from_failed_timeout(member_to_timeout.id)
                        if new_count == -1:
                            await message.channel.send(
                                f"{message.author.mention}, ({role_label}{vow_str}) cooldown remaining: {str(remaining).split('.')[0]}\n"
                                f"{member_to_timeout.mention} is already at max miracles ({MIRACLE_MAX}/{MIRACLE_MAX})!"
                            )
                        else:
                            await message.channel.send(
                                f"{message.author.mention}, ({role_label}{vow_str}) cooldown remaining: {str(remaining).split('.')[0]}\n"
                                f"\u2728 {member_to_timeout.mention} got a miracle! They now have **{new_count}/{MIRACLE_MAX}** miracles."
                            )
                        return

                await message.channel.send(
                    f"{message.author.mention}, ({role_label}{vow_str}{vote_label}) cooldown remaining: "
                    f"{str(remaining).split('.')[0]}"
                )
                return

        if action == "kill":
            last_kill_used[user_id] = now
        # Save CD stamped only on successful save below

    # Also check miracle for attacker vows on CD (Stack, Random, Miracle vows on CD trying to guh Miracle Vow target)
    # This is handled above for standard vow. For Stack/Random/Miracle we need to check before returning on CD.
    # The CD checks for Stack/Random/Miracle vows return early above, so we add miracle checks there:

    # =========================
    # SAVE GIF
    # =========================
    if is_save_gif:
        if not member_to_timeout.timed_out_until:
            await message.channel.send("They're not even timed out bro \U0001f480")
            if action == "save":
                if vow == "Stack Vow":
                    user_data = stack_vow_charges.get(user_id, {})
                    if user_data.get("save"):
                        user_data["save"].pop()
                elif vow != "Random Vow":
                    last_save_used.pop(user_id, None)
            return

        remaining = member_to_timeout.timed_out_until - discord.utils.utcnow()
        if remaining.total_seconds() <= 90:
            try:
                await member_to_timeout.timeout(None)
                # Stamp save CD only on successful save
                if vow == "Random Vow":
                    last_save_used[user_id] = now
                    set_random_vow_cd(user_id, "save")
                elif vow == "Miracle Vow":
                    last_save_used[user_id] = now
                elif vow == "Ragebait Vow":
                    last_save_used[user_id] = now
                elif vow != "Stack Vow":
                    last_save_used[user_id] = now
                await message.channel.send(
                    f"{member_to_timeout.mention} has been freed early by "
                    f"{message.author.mention}{vow_str}"
                )
                # Miracle Vow saver gains a miracle
                if vow == "Miracle Vow":
                    new_count = add_miracle(user_id)
                    if new_count == -1:
                        await message.channel.send(f"{message.author.mention} is already at max miracles ({MIRACLE_MAX}/{MIRACLE_MAX})!")
                    else:
                        await message.channel.send(f"\u2728 {message.author.mention} got a miracle for saving! They now have **{new_count}/{MIRACLE_MAX}** miracles.")
                saved_roles = [r.name for r in member_to_timeout.roles]
                saved_vow = get_active_vow(saved_roles)
                if saved_vow == "Miracle Vow":
                    new_count = add_miracle(member_to_timeout.id)
                    if new_count == -1:
                        await message.channel.send(f"{member_to_timeout.mention} is already at max miracles ({MIRACLE_MAX}/{MIRACLE_MAX})!")
                    else:
                        await message.channel.send(f"\u2728 {member_to_timeout.mention} got a miracle from being saved! They now have **{new_count}/{MIRACLE_MAX}** miracles.")
            except Exception as e:
                await message.channel.send("Failed to remove timeout.")
                await log_error(message.guild, f"untimeout: remove timeout from {member_to_timeout}", e)
        else:
            await message.channel.send(f"Too long left on timeout ({int(remaining.total_seconds())}s). Can't save them.")
        await bot.process_commands(message)
        return

    # =========================
    # KILL GIF
    # =========================
    if is_kill_gif:
        # Ragebait Vow: instead of timing out, adds 1.5x to target's kill CD
        if vow == "Ragebait Vow":
            ragebait_cd = get_ragebait_cd(user_id, base_cd)
            if is_ragebait_on_cd(user_id, base_cd, now):
                remaining = get_ragebait_remaining(user_id, base_cd, now)
                await message.channel.send(
                    f"{message.author.mention}, [Ragebait Vow] ability on cooldown: **{str(remaining).split('.')[0]}**"
                )
                return
            # Apply 1.5x kill CD to target
            target_roles = [r.name for r in member_to_timeout.roles]
            target_valid_roles = [r for r in target_roles if r in ROLE_COOLDOWNS]
            if target_valid_roles:
                target_best = min(target_valid_roles, key=lambda r: ROLE_COOLDOWNS[r])
                target_base_cd = ROLE_COOLDOWNS[target_best]
            else:
                target_base_cd = get_default_cooldown(message.guild.id)
            added_hours = target_base_cd * 0.5
            # Stamp their kill CD as if they just used it, then add 0.5x base on top
            last_kill_used[member_to_timeout.id] = now
            ragebait_kill_cd_added[member_to_timeout.id] = target_base_cd + added_hours
            ragebait_last_used[user_id] = now
            await message.channel.send(
                f"{message.author.mention} [Ragebait Vow] raged at {member_to_timeout.mention}! "
                f"Their kill CD has been extended by {added_hours:.2g}h."
            )
            await bot.process_commands(message)
            return

        timeout_duration = 180 if vow == "Destruction Vow" else TIMEOUT_SECONDS

        if vow == "Random Vow":
            last_kill_used[user_id] = now
        elif vow == "Miracle Vow":
            last_kill_used[user_id] = now

        attacker = message.author
        defender = member_to_timeout
        kill_message_id = message.id
        attacker_vow = vow

        # Miracle block check
        defender_roles_list = [r.name for r in defender.roles]
        defender_vow_check = get_active_vow(defender_roles_list)
        if defender_vow_check == "Miracle Vow":
            miracles = get_miracle_count(defender.id)
            if miracles >= MIRACLE_BLOCK_COST:
                consume_miracles(defender.id, MIRACLE_BLOCK_COST)
                await message.channel.send(
                    f"{MIRACLE_BLOCK_GIF}\n"
                    f"\u2728 {defender.mention}'s miracle blocked the guh! {MIRACLE_BLOCK_COST} miracles consumed. They now have **{get_miracle_count(defender.id)}/{MIRACLE_MAX}** miracles."
                )
                if vow == "Random Vow":
                    last_kill_used.pop(user_id, None)
                elif vow == "Stack Vow":
                    user_data = stack_vow_charges.get(user_id, {})
                    if user_data.get("kill"):
                        user_data["kill"].pop()
                elif vow != "Miracle Vow":
                    last_kill_used.pop(user_id, None)
                await bot.process_commands(message)
                return

        async def clash_or_timeout():
            try:
                await asyncio.sleep(CLASH_WINDOW_SECONDS)
                if kill_message_id in pending_clashes:
                    pending_clashes.pop(kill_message_id, None)
                    if attacker_vow == "Miracle Vow":
                        actual_duration = 30
                    elif attacker_vow == "Random Vow":
                        actual_duration = roll_random_vow_timeout()
                        set_random_vow_cd(user_id, "kill")
                    else:
                        actual_duration = timeout_duration
                    try:
                        await defender.timeout(discord.utils.utcnow() + timedelta(seconds=actual_duration))
                        await message.channel.send(
                            f"{defender.mention} has been timed out for {actual_duration}s "
                            f"by {attacker.mention}{vow_str} lmao"
                        )
                    except Exception as e:
                        await message.channel.send(f"Failed to timeout {defender.mention}.")
                        await log_error(message.guild, f"timeout: apply timeout to {defender}", e)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                await log_error(message.guild, f"clash_or_timeout for {defender}", e)

        if vow == "Hakari Vow":
            async def hakari_or_timeout():
                try:
                    await asyncio.sleep(CLASH_WINDOW_SECONDS)
                    if kill_message_id in pending_clashes:
                        pending_clashes.pop(kill_message_id, None)
                        if random.random() < 0.36:
                            try:
                                await defender.timeout(discord.utils.utcnow() + timedelta(seconds=251))
                                await message.channel.send(
                                    f"\U0001f3b0 **JACKPOT!** {defender.mention} has been muted for 4m11s "
                                    f"by {attacker.mention} [Hakari Vow] lmao"
                                )
                            except Exception as e:
                                await log_error(message.guild, f"hakari win: timeout {defender}", e)
                        else:
                            try:
                                await attacker.timeout(discord.utils.utcnow() + timedelta(seconds=90))
                                await message.channel.send(
                                    f"\U0001f480 {attacker.mention} [Hakari Vow] lost the gamble and muted themselves for 90s lmaooo"
                                )
                            except Exception as e:
                                await log_error(message.guild, f"hakari loss: timeout {attacker}", e)
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    await log_error(message.guild, f"hakari_or_timeout for {defender}", e)

            task = asyncio.create_task(hakari_or_timeout())
        else:
            task = asyncio.create_task(clash_or_timeout())

        pending_clashes[kill_message_id] = {
            "attacker": attacker,
            "defender": defender,
            "channel": message.channel,
            "timeout_duration": timeout_duration,
            "attacker_vow_str": vow_str,
            "attacker_vow": attacker_vow,
            "task": task,
        }

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    emoji_map = {
        "\U0001fac3": "MPREG",
        "\U0001f930": "WPREG",
        "\U0001f9d1\u200d\U0001f37c": "PREG"
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
