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
    "https://tenor.com/view/fujinvfx-maki-maki-zenin-jujutsu-kaisen-jjk-gif-11607407997389549481",
    "https://tenor.com/view/nanami-punch-jujutsu-kaisen-shibuya-3-dontdox-gif-7014352537901038364",
    "https://tenor.com/view/fnaf-fnaf4-freddy-freddy-fazbear-nightmare-freddy-gif-24525113",
    "https://tenor.com/view/gojo-gojo-satoru-gojo-season-2-hip-thrust-reaction-gif-10399129046512126318",
    "https://tenor.com/view/megumi-fushiguro-fushi-guro-megumi-fushiguro-mahoraga-gif-92941122665464082",
    "https://tenor.com/view/gojo-geto-suguru-gojo-satoru-kenjaku-prison-realm-gif-5425478000746110355",
    "https://tenor.com/view/killer-queen-bites-the-dust-gif-22628088",
    "https://tenor.com/view/drake-stealing-gif-7426561037579652441",
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
    "https://tenor.com/view/kinblood-lebron-dunk-gif-12278440",
    "https://tenor.com/view/nanako-gif-366179704676552608",
    "https://tenor.com/view/sukuna-jujutsu-kaisen-kneel-down-jjk-sukuna-ryomen-gif-17856271175806049937",
    "https://cdn.discordapp.com/attachments/1501576319597674547/1501657404528656454/image0.gif",
    "https://cdn.discordapp.com/attachments/1460734437485576234/1460734876323152024/image0.gif",
    "https://tenor.com/view/osamason-osamason-lazer-tuff-nettspend-pluggnb-gif-781443353793945495",
    "https://tenor.com/view/cockroach-flying-at-you-gif-8185461940091837006",
    "https://media.discordapp.net/attachments/1085769531575771159/1202383944872501338/togif.gif",
    "https://cdn.discordapp.com/attachments/1489398429191770252/1489799839116951672/tojirio.gif",
    "https://tenor.com/view/can-haramba-stop-the-gta-v-plane-harambe-airplane-gorilla-gif-16789079"
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

"https://tenor.com/view/asda-gif-17942224497192232341",
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

"https://cdn.discordapp.com/attachments/1501576319597674547/1501657150697771100/image0.gif",
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

# =========================
# DEFAULT ROLE CONFIG
# =========================

DEFAULT_ROLE_COOLDOWNS = {
    "Bum": 18,
    "Rat": 9,
    "Chud": 4,
    "Otis BFF ❤️": 4,
    "Shit ass mod": 0,
    "Good Moderator Morning!": 0,
}

DEFAULT_CLASH_TICKETS = {
    "Bum": 4,
    "Rat": 7,
    "Chud": 10,
    "Otis BFF ❤️": 10,
    "Shit ass mod": 10,
    "Good Moderator Morning!": 999
}

GMM_ROLE = "Good Moderator Morning!"


def get_role_cooldowns(guild_id: int) -> dict[str, float]:
    raw = server_settings.get(guild_id, {}).get("role_cooldowns", None)
    if not raw:
        return DEFAULT_ROLE_COOLDOWNS
    return {name: data[1] for name, data in raw.items()}


def get_clash_tickets_map(guild_id: int) -> dict[str, int]:
    raw = server_settings.get(guild_id, {}).get("clash_tickets", None)
    if not raw:
        return DEFAULT_CLASH_TICKETS
    return raw


# =========================
# PER-SERVER SETTINGS
# =========================

SERVER_SETTINGS_FILE = "server_settings.json"
DEFAULT_COOLDOWN_HOURS = 12.0
server_settings: dict[int, dict] = {}

# =========================
# VOTE SYSTEM
# vote_timestamps stays global — a vote applies across all servers
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


def load_server_settings() -> dict:
    # Try Redis first
    try:
        raw = redis.get("server_settings")
        if raw:
            data = json.loads(raw)
            print("[server_settings] Loaded from Redis.")
            return {int(k): v for k, v in data.items()}
    except Exception as e:
        print(f"[server_settings] Redis load failed: {e}")
    # Fall back to local file
    if os.path.exists(SERVER_SETTINGS_FILE):
        with open(SERVER_SETTINGS_FILE, "r") as f:
            raw = json.load(f)
        return {int(k): v for k, v in raw.items()}
    return {}


def save_server_settings():
    data = {str(k): v for k, v in server_settings.items()}
    try:
        redis.set("server_settings", json.dumps(data))
    except Exception as e:
        print(f"[server_settings] Redis save failed: {e}")
    try:
        with open(SERVER_SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[server_settings] Local file save failed: {e}")


def get_default_cooldown(guild_id: int) -> float:
    return server_settings.get(guild_id, {}).get("default_cooldown", DEFAULT_COOLDOWN_HOURS)


def get_default_role(guild_id: int) -> int | None:
    return server_settings.get(guild_id, {}).get("default_role_id", None)


# =========================
# COOLDOWN PERSISTENCE (Redis)
# Keys are "guild_id:user_id" strings for per-server separation.
# vote_timestamps, miracle_counts, miracle_gain_cooldown, ragebait_last_used,
# random_vow_cds, and stack_vow_charges are also keyed per-server.
# =========================

from upstash_redis import Redis

redis = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

# All per-server cooldown dicts: key = (guild_id, user_id)
last_kill_used: dict[tuple[int, int], datetime] = {}
last_save_used: dict[tuple[int, int], datetime] = {}
miracle_counts: dict[tuple[int, int], int] = {}
miracle_gain_cooldown: dict[tuple[int, int], datetime] = {}
ragebait_last_used: dict[tuple[int, int], datetime] = {}
random_vow_cds: dict[tuple[int, int], dict[str, float | None]] = {}
stack_vow_charges: dict[tuple[int, int], dict[str, list[datetime]]] = {}

# vote_timestamps stays global (a vote applies everywhere)


def _gk(guild_id: int, user_id: int) -> str:
    """Encode a (guild_id, user_id) pair as a storable string key."""
    return f"{guild_id}:{user_id}"


def _parse_gk(key: str) -> tuple[int, int]:
    g, u = key.split(":", 1)
    return int(g), int(u)


def load_cooldowns():
    try:
        raw = redis.get("cooldowns")
        if not raw:
            print("[cooldowns] No saved cooldowns found in Redis.")
            return
        data = json.loads(raw)
    except Exception as e:
        print(f"[cooldowns] Failed to load from Redis: {e}")
        return

    for k, ts in data.get("last_kill_used", {}).items():
        last_kill_used[_parse_gk(k)] = datetime.fromisoformat(ts)
    for k, ts in data.get("last_save_used", {}).items():
        last_save_used[_parse_gk(k)] = datetime.fromisoformat(ts)
    for k, count in data.get("miracle_counts", {}).items():
        miracle_counts[_parse_gk(k)] = count
    for k, ts in data.get("miracle_gain_cooldown", {}).items():
        miracle_gain_cooldown[_parse_gk(k)] = datetime.fromisoformat(ts)
    for k, ts in data.get("ragebait_last_used", {}).items():
        ragebait_last_used[_parse_gk(k)] = datetime.fromisoformat(ts)
    for k, cds in data.get("random_vow_cds", {}).items():
        random_vow_cds[_parse_gk(k)] = cds
    for k, ts in data.get("vote_timestamps", {}).items():
        vote_timestamps[int(k)] = datetime.fromisoformat(ts)
    for k, charges in data.get("stack_vow_charges", {}).items():
        stack_vow_charges[_parse_gk(k)] = {
            "kill": [datetime.fromisoformat(t) for t in charges.get("kill", [])],
            "save": [datetime.fromisoformat(t) for t in charges.get("save", [])],
        }
    print(f"[cooldowns] Loaded {len(data.get('last_kill_used', {}))} kill CD entries.")


def save_cooldowns():
    def dt_gk(d):
        return {_gk(*k): v.isoformat() for k, v in d.items()}

    data = {
        "last_kill_used": dt_gk(last_kill_used),
        "last_save_used": dt_gk(last_save_used),
        "miracle_counts": {_gk(*k): v for k, v in miracle_counts.items()},
        "miracle_gain_cooldown": dt_gk(miracle_gain_cooldown),
        "ragebait_last_used": dt_gk(ragebait_last_used),
        "random_vow_cds": {_gk(*k): v for k, v in random_vow_cds.items()},
        "vote_timestamps": {str(k): v.isoformat() for k, v in vote_timestamps.items()},
        "stack_vow_charges": {
            _gk(*k): {
                "kill": [t.isoformat() for t in charges["kill"]],
                "save": [t.isoformat() for t in charges["save"]],
            }
            for k, charges in stack_vow_charges.items()
        },
    }
    try:
        redis.set("cooldowns", json.dumps(data))
    except Exception as e:
        print(f"[cooldowns] Failed to save to Redis: {e}")


# =========================
# BINDING VOW SYSTEM
# =========================

BINDING_VOWS = {
    "Destruction Vow": {
        "kill_multiplier": 3.0,
        "save_multiplier": 1.0,
        "description": "Kill CDs ×3",
    },
    "Healing Vow": {
        "kill_multiplier": None,
        "save_multiplier": 0.002,
        "description": "Cannot kill / Save CDs ÷500",
    },
    "Hakari Vow": {
        "kill_multiplier": 1.0,
        "save_multiplier": 1.0,
        "description": "Kill GIFs go through clash window. No clash: 36% mute target 4m11s / 64% mute yourself 90s. Win clash: 50/50 gamble.",
    },
    "Stack Vow": {
        "description": "Kill & save CDs ×2, but bank up to 3 uses of each independently",
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
        "description": "Kill GIFs don't timeout the target — instead puts their kill guh on CD for their normal duration. Ragebait ability CD is 1h. Save works normally.",
    },
}

STACK_VOW_MULTIPLIER = 2.0
STACK_VOW_MAX_CHARGES = 3

MIRACLE_MAX = 6
MIRACLE_BLOCK_COST = 2

MIRACLE_GAIN_COOLDOWN_HOURS = 1.0
RAGEBAIT_COOLDOWN_HOURS = 1.0


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


# =========================
# STACK VOW HELPERS  (guild_id, user_id) keyed
# =========================

def _get_active_charge_timestamps(guild_id: int, user_id: int, action: str, cd_hours: float, now: datetime) -> list[datetime]:
    key = (guild_id, user_id)
    user_data = stack_vow_charges.setdefault(key, {"kill": [], "save": []})
    regen_window = timedelta(hours=cd_hours)
    active = [t for t in user_data[action] if now - t < regen_window]
    user_data[action] = active
    return active


def stack_vow_available_charges(guild_id: int, user_id: int, action: str, cd_hours: float, now: datetime) -> int:
    active = _get_active_charge_timestamps(guild_id, user_id, action, cd_hours, now)
    return max(0, STACK_VOW_MAX_CHARGES - len(active))


def stack_vow_consume_charge(guild_id: int, user_id: int, action: str, now: datetime):
    key = (guild_id, user_id)
    user_data = stack_vow_charges.setdefault(key, {"kill": [], "save": []})
    user_data[action].append(now)


def stack_vow_next_regen(guild_id: int, user_id: int, action: str, cd_hours: float, now: datetime) -> timedelta | None:
    active = _get_active_charge_timestamps(guild_id, user_id, action, cd_hours, now)
    if not active:
        return None
    oldest = min(active)
    regen_at = oldest + timedelta(hours=cd_hours)
    return max(timedelta(0), regen_at - now)


# =========================
# MIRACLE HELPERS
# =========================

def get_miracle_count(guild_id: int, user_id: int) -> int:
    return miracle_counts.get((guild_id, user_id), 0)


def add_miracle(guild_id: int, user_id: int) -> int:
    key = (guild_id, user_id)
    current = miracle_counts.get(key, 0)
    if current >= MIRACLE_MAX:
        return -1
    miracle_counts[key] = current + 1
    return miracle_counts[key]


def can_gain_miracle_from_failed_timeout(guild_id: int, user_id: int) -> bool:
    last = miracle_gain_cooldown.get((guild_id, user_id))
    if not last:
        return True
    return datetime.utcnow() - last >= timedelta(hours=MIRACLE_GAIN_COOLDOWN_HOURS)


def record_miracle_gain_from_failed_timeout(guild_id: int, user_id: int):
    miracle_gain_cooldown[(guild_id, user_id)] = datetime.utcnow()


def consume_miracles(guild_id: int, user_id: int, amount: int):
    key = (guild_id, user_id)
    current = miracle_counts.get(key, 0)
    miracle_counts[key] = max(0, current - amount)


# =========================
# RAGEBAIT HELPERS
# =========================

def is_ragebait_on_cd(guild_id: int, user_id: int, now: datetime) -> bool:
    last = ragebait_last_used.get((guild_id, user_id))
    if not last:
        return False
    return now - last < timedelta(hours=RAGEBAIT_COOLDOWN_HOURS)


def get_ragebait_remaining(guild_id: int, user_id: int, now: datetime) -> timedelta:
    last = ragebait_last_used.get((guild_id, user_id))
    if not last:
        return timedelta(0)
    return max(timedelta(0), timedelta(hours=RAGEBAIT_COOLDOWN_HOURS) - (now - last))


# =========================
# RANDOM VOW HELPERS
# =========================

def get_random_vow_cd(guild_id: int, user_id: int, action: str) -> float | None:
    return random_vow_cds.get((guild_id, user_id), {}).get(action, None)


def set_random_vow_cd(guild_id: int, user_id: int, action: str):
    key = (guild_id, user_id)
    if key not in random_vow_cds:
        random_vow_cds[key] = {"kill": None, "save": None}
    if action == "kill":
        random_vow_cds[key]["kill"] = random.triangular(1.0, 21.0, 3.0)
    else:
        random_vow_cds[key]["save"] = random.triangular(2.0, 10.0, 3.0)


def roll_random_vow_timeout() -> int:
    return int(random.triangular(10, 480, 30))


# =========================
# OTHER CONFIG
# =========================

MODLOG_CHANNEL = "modlog"
pending_clashes: dict[int, dict] = {}
clash_head_lookup: dict[int, int] = {}
active_setup_sessions: dict[int, int] = {}


def get_clash_tickets(member_roles: list[str], guild_id: int) -> int:
    tickets_map = get_clash_tickets_map(guild_id)
    best = 0
    for role_name in member_roles:
        tickets = tickets_map.get(role_name, 0)
        if tickets > best:
            best = tickets
    return best if best > 0 else 1


def resolve_clash(attacker_tickets: int, defender_tickets: int) -> bool:
    total = attacker_tickets + defender_tickets
    return random.randint(1, total) <= attacker_tickets


def pick_clash_gif(all_roles: list[list[str]]) -> str:
    for roles in all_roles:
        if GMM_ROLE in roles:
            return random.choice(CLASH_GIFS_GMM)
    return random.choice(CLASH_GIFS)


def any_gmm(all_roles: list[list[str]]) -> bool:
    return any(GMM_ROLE in roles for roles in all_roles)


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


async def try_timeout(member: discord.Member, until, channel: discord.TextChannel, label: str = "") -> bool:
    bot_member = channel.guild.me
    if not bot_member.guild_permissions.moderate_members:
        await channel.send("bot needs timeout perms")
        return False
    if member.top_role >= bot_member.top_role:
        await channel.send("bot cant mute someone with higher level")
        return False
    try:
        await member.timeout(until)
        return True
    except discord.Forbidden:
        await channel.send("bot needs timeout perms")
        return False
    except Exception as e:
        await log_error(channel.guild, label or f"timeout {member}", e)
        return False


async def try_untimeout(member: discord.Member, channel: discord.TextChannel, label: str = "") -> bool:
    bot_member = channel.guild.me
    if not bot_member.guild_permissions.moderate_members:
        await channel.send("bot needs timeout perms")
        return False
    try:
        await member.timeout(None)
        return True
    except discord.Forbidden:
        await channel.send("bot needs timeout perms")
        return False
    except Exception as e:
        await channel.send(f"❌ Failed to free {member.mention}.")
        await log_error(channel.guild, label or f"untimeout {member}", e)
        return False


# =========================
# SETUP HELPERS
# =========================

def build_setup_summary(guild_id: int) -> str:
    raw = server_settings.get(guild_id, {}).get("role_cooldowns", None)
    tickets_raw = server_settings.get(guild_id, {}).get("clash_tickets", None)
    if not raw:
        lines = [f"**{name}**: {cd}h CD, {DEFAULT_CLASH_TICKETS.get(name, 1)} tickets"
                 for name, cd in DEFAULT_ROLE_COOLDOWNS.items()]
        return "*(using defaults)*\n" + "\n".join(lines)
    lines = []
    for role_name, data in raw.items():
        role_id, cd = data
        tickets = (tickets_raw or {}).get(role_name, 1)
        lines.append(f"<@&{role_id}> ({role_name}): **{cd}h** CD, **{tickets}** tickets")
    return "\n".join(lines) if lines else "No roles configured."


async def run_setup_session(ctx_or_interaction, guild: discord.Guild, user: discord.Member, channel):
    if user.id in active_setup_sessions:
        msg = "You already have an active setup session. Type `done` to finish it or `cancel` to abort."
        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(msg, ephemeral=True)
        else:
            await channel.send(msg)
        return

    active_setup_sessions[user.id] = guild.id

    intro = (
        "**⚙️ GIF Bot Role Setup**\n\n"
        "Send one role per message in this format:\n"
        "> `@RoleName <cooldown_hours> <clash_tickets>`\n\n"
        "**Examples:**\n"
        "> `@Bum 18 4` — 18h cooldown, 4 clash tickets\n"
        "> `@Moderator 0 10` — no cooldown, 10 clash tickets\n\n"
        "**Notes:**\n"
        "- Cooldown `0` = no cooldown\n"
        "- Clash tickets determine win chance in a clash (higher = better odds)\n"
        "- Roles not listed here will use the server default cooldown\n"
        "- You have **2 minutes** per message before the session times out\n\n"
        f"**Current config:**\n{build_setup_summary(guild.id)}\n\n"
        "Type `done` when finished, or `cancel` to abort without saving."
    )

    if isinstance(ctx_or_interaction, discord.Interaction):
        await ctx_or_interaction.response.send_message(intro)
    else:
        await channel.send(intro)

    new_cooldowns = {}
    new_tickets = {}

    def check(m):
        return m.author.id == user.id and m.channel.id == channel.id

    while True:
        try:
            msg = await bot.wait_for("message", timeout=120.0, check=check)
        except asyncio.TimeoutError:
            active_setup_sessions.pop(user.id, None)
            await channel.send("⏱️ Setup timed out. No changes were saved.")
            return

        text = msg.content.strip().lower()

        if text == "cancel":
            active_setup_sessions.pop(user.id, None)
            await channel.send("❌ Setup cancelled. No changes were saved.")
            return

        if text == "done":
            if not new_cooldowns:
                active_setup_sessions.pop(user.id, None)
                await channel.send("❌ No roles were added. Setup cancelled.")
                return
            if guild.id not in server_settings:
                server_settings[guild.id] = {}
            server_settings[guild.id]["role_cooldowns"] = new_cooldowns
            server_settings[guild.id]["clash_tickets"] = new_tickets
            save_server_settings()
            active_setup_sessions.pop(user.id, None)
            summary_lines = []
            for role_name, data in new_cooldowns.items():
                role_id, cd = data
                tickets = new_tickets.get(role_name, 1)
                summary_lines.append(f"<@&{role_id}> ({role_name}): **{cd}h** CD, **{tickets}** tickets")
            await channel.send(
                f"✅ **Setup complete!** Saved {len(new_cooldowns)} role(s):\n" +
                "\n".join(summary_lines)
            )
            return

        if not msg.role_mentions:
            await channel.send(
                "⚠️ Couldn't find a role mention. Make sure to @mention the role.\n"
                "Format: `@Role <cooldown_hours> <clash_tickets>` — e.g. `@Bum 18 4`\n"
                "Type `cancel` to abort."
            )
            continue

        parts = msg.content.strip().split()
        numbers = [p for p in parts if re.match(r'^\d+(\.\d+)?$', p)]

        if len(numbers) < 2:
            await channel.send(
                "⚠️ Need both a cooldown and clash tickets value.\n"
                "Format: `@Role <cooldown_hours> <clash_tickets>` — e.g. `@Bum 18 4`"
            )
            continue

        try:
            cd_hours = float(numbers[0])
            tickets = int(float(numbers[1]))
        except ValueError:
            await channel.send("⚠️ Invalid numbers. Cooldown must be a number, tickets must be a whole number.")
            continue

        if cd_hours < 0:
            await channel.send("⚠️ Cooldown can't be negative.")
            continue
        if tickets < 0:
            await channel.send("⚠️ Clash tickets can't be negative.")
            continue

        role = msg.role_mentions[0]
        new_cooldowns[role.name] = [role.id, cd_hours]
        new_tickets[role.name] = tickets
        await channel.send(
            f"✅ Added **{role.name}**: **{cd_hours}h** cooldown, **{tickets}** clash tickets. "
            f"Send another role or type `done`."
        )


# =========================
# COOLDOWN STATUS
# =========================

def build_cooldown_status(member: discord.Member, guild_id: int) -> str:
    author_roles = [role.name for role in member.roles]
    role_cooldowns = get_role_cooldowns(guild_id)
    valid_roles = [r for r in author_roles if r in role_cooldowns]
    default_cd = get_default_cooldown(guild_id)

    if valid_roles:
        best_role = min(valid_roles, key=lambda r: role_cooldowns[r])
        base_cd = role_cooldowns[best_role]
        role_label = best_role
    else:
        base_cd = default_cd
        role_label = f"default ({default_cd}h)"

    vow = get_active_vow(author_roles)
    vow_str = format_vow_label(vow)
    now = datetime.utcnow()
    uid = member.id
    gid = guild_id

    if vow == "CONFLICT":
        return (
            f"{member.mention}, ⚠️ you have multiple Binding Vow roles — "
            "vows are being ignored until this is resolved."
        )

    if base_cd == 0:
        return f"{member.mention}, ({role_label}{vow_str}) you have no cooldown 😈"

    if vow == "Stack Vow":
        sv_cd = base_cd * STACK_VOW_MULTIPLIER

        def charge_status(action: str) -> str:
            available = stack_vow_available_charges(gid, uid, action, sv_cd, now)
            next_regen = stack_vow_next_regen(gid, uid, action, sv_cd, now)
            charge_pips = "🟢" * available + "🔴" * (STACK_VOW_MAX_CHARGES - available)
            if next_regen:
                return f"{charge_pips} (next regen in **{str(next_regen).split('.')[0]}**)"
            return charge_pips

        return (
            f"{member.mention}, ({role_label} [Stack Vow]) CD: {sv_cd:.4g}h per charge\n"
            f"☠️ Kill charges: {charge_status('kill')}\n"
            f"💚 Save charges: {charge_status('save')}"
        )

    if vow == "Miracle Vow":
        miracles = get_miracle_count(gid, uid)
        kill_cd = apply_vote_discount(base_cd * 2.5, uid)
        save_cd = apply_vote_discount(base_cd * 2.5, uid)
        last_kill = last_kill_used.get((gid, uid))
        last_save = last_save_used.get((gid, uid))

        def format_cd_miracle(hours: float, last: datetime | None) -> str:
            td = timedelta(hours=hours)
            if not last or now - last >= td:
                return "ready ✅"
            remaining = td - (now - last)
            return f"**{str(remaining).split('.')[0]}** remaining"

        return (
            f"{member.mention}, ({role_label} [Miracle Vow]) ✨ Miracles: {miracles}/{MIRACLE_MAX}\n"
            f"☠️ Kill CD: {format_cd_miracle(kill_cd, last_kill)}\n"
            f"💚 Save CD: {format_cd_miracle(save_cd, last_save)}"
        )

    if vow == "Random Vow":
        kill_cd_val = get_random_vow_cd(gid, uid, "kill")
        save_cd_val = get_random_vow_cd(gid, uid, "save")
        last_kill = last_kill_used.get((gid, uid))
        last_save = last_save_used.get((gid, uid))

        def format_random_cd(cd_val: float | None, last: datetime | None) -> str:
            if cd_val is None or not last:
                return "ready ✅"
            td = timedelta(hours=cd_val)
            if now - last >= td:
                return "ready ✅"
            remaining = td - (now - last)
            return f"**{str(remaining).split('.')[0]}** remaining (rolled {cd_val:.2f}h)"

        return (
            f"{member.mention}, ({role_label} [Random Vow])\n"
            f"☠️ Kill CD: {format_random_cd(kill_cd_val, last_kill)}\n"
            f"💚 Save CD: {format_random_cd(save_cd_val, last_save)}"
        )

    if vow == "Bitchout Vow":
        return f"{member.mention}, you're a bitch but a guh free bitch atleast"

    if vow == "Ragebait Vow":
        save_cd = apply_vote_discount(base_cd, uid)
        last_save = last_save_used.get((gid, uid))

        def format_cd_simple(hours: float, last: datetime | None) -> str:
            if not last or now - last >= timedelta(hours=hours):
                return "ready ✅"
            remaining = timedelta(hours=hours) - (now - last)
            return f"**{str(remaining).split('.')[0]}** remaining"

        ragebait_remaining = get_ragebait_remaining(gid, uid, now)
        ragebait_status = "ready ✅" if ragebait_remaining.total_seconds() == 0 else f"**{str(ragebait_remaining).split('.')[0]}** remaining"
        return (
            f"{member.mention}, ({role_label} [Ragebait Vow])\n"
            f"😡 Ragebait CD (1h): {ragebait_status}\n"
            f"💚 Save CD ({base_cd}h): {format_cd_simple(save_cd, last_save)}"
        )

    kill_cd = apply_vote_discount(apply_vow(base_cd, "kill", vow), uid)
    save_cd = apply_vote_discount(apply_vow(base_cd, "save", vow), uid)
    last_kill = last_kill_used.get((gid, uid))
    last_save = last_save_used.get((gid, uid))
    voted = has_active_vote(uid)
    vote_label = " 📥 25% off" if voted else ""

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
        return f"{member.mention}, ({role_label}{vow_str}{vote_label}) cooldown: {format_cd(kill_cd, last_kill)}"
    return (
        f"{member.mention}, ({role_label}{vow_str}{vote_label})\n"
        f"☠️ Kill CD: {format_cd(kill_cd, last_kill)}\n"
        f"💚 Save CD: {format_cd(save_cd, last_save)}"
    )


def build_help_embed(guild_id: int) -> discord.Embed:
    default_cd = get_default_cooldown(guild_id)
    default_role_id = get_default_role(guild_id)
    embed = discord.Embed(title="Bot Help", color=discord.Color.blurple())
    embed.add_field(
        name="How it works",
        value=(
            "Reply to someone's message with a **kill GIF** to time them out (90s).\n"
            "Reply to a timed-out user's message with a **save GIF** to free them early.\n"
            "If anyone replies to the kill GIF chain with another kill GIF within 5 seconds, a **Clash** happens — "
            "up to 10 fighters can join! The winner is picked by ticket weight, everyone else gets timed out."
        ),
        inline=False
    )
    default_role_str = f"<@&{default_role_id}>" if default_role_id else "none set (everyone can use GIFs)"
    embed.add_field(
        name="Access & Cooldowns",
        value=(
            f"Default role to use GIFs: {default_role_str}\n"
            f"Default cooldown: **{default_cd}h**\n"
            "*Cooldowns are per-server. Role-specific cooldowns via `/setup` or `!setup`.*"
        ),
        inline=False
    )
    vow_lines = "\n".join(
        f"**{name}** — {data['description']}"
        for name, data in BINDING_VOWS.items()
    )
    embed.add_field(name="Binding Vows", value=vow_lines, inline=False)
    embed.add_field(
        name="📥 Vote for a Cooldown Discount",
        value=(
            "Vote for the bot to get **25% off your cooldowns** for 12 hours!\n"
            "[Click here to vote](https://discordbotlist.com/bots/funnything/upvote)"
        ),
        inline=False
    )
    embed.add_field(
        name="Commands",
        value=(
            "`/help` or `!help` — show this message\n"
            "`/vote` or `!vote` — get the vote link for a 25% cooldown discount\n"
            "`/cooldown [@user]` or `@bot` — check your (or someone else's) cooldown status\n"
            "`/setup` or `!setup` — configure role cooldowns and clash tickets *(mods only)*\n"
            "`/viewsetup` or `!viewsetup` — view current role config\n"
            "`/resetcooldown @user [kill|save|both]` — reset a user's cooldown *(mods only)*\n"
            "`/cooldowns [hours]` or `!cooldowns [hours]` — view or set the default cooldown *(mods only)*\n"
            "`/setdefaultrole [@role]` — set the role needed to use GIFs *(mods only)*\n"
            "`/cleardefaultrole` — remove the role requirement *(mods only)*"
        ),
        inline=False
    )
    return embed


# =========================
# STARTUP
# =========================

@bot.event
async def on_ready():
    global server_settings
    server_settings = load_server_settings()
    load_cooldowns()
    print(f"Logged in as {bot.user}")

    for guild in bot.guilds:
        bum_role = discord.utils.get(guild.roles, name="Bum")
        if bum_role:
            if guild.id not in server_settings:
                server_settings[guild.id] = {}
            if "default_role_id" not in server_settings[guild.id]:
                server_settings[guild.id]["default_role_id"] = bum_role.id
                print(f"[setup] Auto-set default role to Bum in {guild.name}")
    save_server_settings()

    bot.loop.create_task(periodic_save())
    await start_webhook_server()


async def periodic_save():
    await bot.wait_until_ready()
    while not bot.is_closed():
        save_cooldowns()
        await asyncio.sleep(60)


@bot.command(name="sync")
@commands.is_owner()
async def sync_commands(ctx):
    await ctx.send("Syncing slash commands globally...")
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Synced {len(synced)} slash command(s) globally.")
    except Exception as e:
        await ctx.send(f"❌ Sync failed: {e}")


# =========================
# PREFIX COMMANDS
# =========================

@bot.command(name="help")
async def prefix_help(ctx):
    await ctx.send(embed=build_help_embed(ctx.guild.id))


@bot.command(name="setup")
async def prefix_setup(ctx):
    if not ctx.author.guild_permissions.manage_roles and not ctx.author.guild_permissions.manage_guild:
        await ctx.send(f"{ctx.author.mention}, you need Manage Roles permission to run setup.")
        return
    await run_setup_session(ctx, ctx.guild, ctx.author, ctx.channel)


@bot.command(name="viewsetup")
async def prefix_viewsetup(ctx):
    summary = build_setup_summary(ctx.guild.id)
    default_cd = get_default_cooldown(ctx.guild.id)
    default_role_id = get_default_role(ctx.guild.id)
    default_role_str = f"<@&{default_role_id}>" if default_role_id else "none (everyone)"
    await ctx.send(
        f"**⚙️ Current Role Config for this server:**\n{summary}\n\n"
        f"**Default cooldown:** {default_cd}h\n"
        f"**Default role required:** {default_role_str}"
    )


@bot.command(name="resetcooldown")
async def prefix_resetcooldown(ctx, target: discord.Member = None, which: str = "both"):
    if not ctx.author.guild_permissions.manage_roles and not ctx.author.guild_permissions.manage_guild:
        await ctx.send(f"{ctx.author.mention}, you need the Manage Roles permission to do that.")
        return
    if not target:
        await ctx.send("Usage: `!resetcooldown @user [kill|save|both]`")
        return
    if which not in ("both", "kill", "save"):
        await ctx.send("Invalid option. Use `kill`, `save`, or `both`.")
        return
    gid = ctx.guild.id
    uid = target.id
    if which in ("both", "kill"):
        last_kill_used.pop((gid, uid), None)
        if (gid, uid) in random_vow_cds:
            random_vow_cds[(gid, uid)]["kill"] = None
        if (gid, uid) in stack_vow_charges:
            stack_vow_charges[(gid, uid)]["kill"] = []
    if which in ("both", "save"):
        last_save_used.pop((gid, uid), None)
        if (gid, uid) in random_vow_cds:
            random_vow_cds[(gid, uid)]["save"] = None
        if (gid, uid) in stack_vow_charges:
            stack_vow_charges[(gid, uid)]["save"] = []
    save_cooldowns()
    label = "kill and save cooldowns" if which == "both" else f"{which} cooldown"
    await ctx.send(f"✅ Reset {label} for {target.mention}.")


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
        await ctx.send("Invalid value. Must be a non-negative number.")
        return
    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["default_cooldown"] = new_cd
    save_server_settings()
    await ctx.send(f"✅ Default cooldown set to **{new_cd}h**")


@bot.command(name="setdefaultrole")
async def prefix_setdefaultrole(ctx, *, role_input: str = None):
    if not ctx.author.guild_permissions.manage_roles and not ctx.author.guild_permissions.manage_guild:
        await ctx.send(f"{ctx.author.mention}, you need the Manage Roles permission to do that.")
        return
    if not role_input:
        current_id = get_default_role(ctx.guild.id)
        role_str = ctx.guild.get_role(current_id).mention if current_id and ctx.guild.get_role(current_id) else "none (everyone)"
        await ctx.send(f"Current default GIF role: {role_str}\nUsage: `!setdefaultrole @Role` or `!setdefaultrole clear`")
        return
    if role_input.strip().lower() == "clear":
        if ctx.guild.id in server_settings:
            server_settings[ctx.guild.id].pop("default_role_id", None)
            save_server_settings()
        await ctx.send("✅ Default role requirement cleared.")
        return
    role = ctx.message.role_mentions[0] if ctx.message.role_mentions else discord.utils.find(lambda r: r.name.lower() == role_input.lower(), ctx.guild.roles)
    if not role:
        await ctx.send("Couldn't find that role.")
        return
    if ctx.guild.id not in server_settings:
        server_settings[ctx.guild.id] = {}
    server_settings[ctx.guild.id]["default_role_id"] = role.id
    save_server_settings()
    await ctx.send(f"✅ Default GIF role set to **{role.name}**.")


# =========================
# SLASH COMMANDS
# =========================

@bot.tree.command(name="help", description="Show how the bot works")
async def slash_help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=build_help_embed(interaction.guild_id))


@bot.tree.command(name="cooldown", description="Check your (or someone else's) cooldown status")
@app_commands.describe(target="The user to check (leave blank for yourself)")
async def slash_cooldown(interaction: discord.Interaction, target: discord.Member = None):
    member = target or interaction.user
    if not isinstance(member, discord.Member):
        member = interaction.guild.get_member(member.id)
    if not member:
        await interaction.response.send_message("Couldn't find that user in this server.", ephemeral=True)
        return
    msg = build_cooldown_status(member, interaction.guild_id)
    await interaction.response.send_message(msg)


@bot.tree.command(name="setup", description="Configure role cooldowns and clash tickets (mods only)")
async def slash_setup(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need Manage Roles permission to run setup.", ephemeral=True)
        return
    await run_setup_session(interaction, interaction.guild, interaction.user, interaction.channel)


@bot.tree.command(name="viewsetup", description="View the current role cooldown config for this server")
async def slash_viewsetup(interaction: discord.Interaction):
    summary = build_setup_summary(interaction.guild_id)
    default_cd = get_default_cooldown(interaction.guild_id)
    default_role_id = get_default_role(interaction.guild_id)
    default_role_str = f"<@&{default_role_id}>" if default_role_id else "none (everyone)"
    await interaction.response.send_message(
        f"**⚙️ Current Role Config for this server:**\n{summary}\n\n"
        f"**Default cooldown:** {default_cd}h\n"
        f"**Default role required:** {default_role_str}"
    )


@bot.tree.command(name="resetcooldown", description="Reset a user's cooldown (mods only)")
@app_commands.describe(target="The user to reset", which="Which cooldown to reset")
@app_commands.choices(which=[
    app_commands.Choice(name="both", value="both"),
    app_commands.Choice(name="kill", value="kill"),
    app_commands.Choice(name="save", value="save"),
])
async def slash_resetcooldown(interaction: discord.Interaction, target: discord.Member, which: str = "both"):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need the Manage Roles permission to do that.", ephemeral=True)
        return
    gid = interaction.guild_id
    uid = target.id
    if which in ("both", "kill"):
        last_kill_used.pop((gid, uid), None)
        if (gid, uid) in random_vow_cds:
            random_vow_cds[(gid, uid)]["kill"] = None
        if (gid, uid) in stack_vow_charges:
            stack_vow_charges[(gid, uid)]["kill"] = []
    if which in ("both", "save"):
        last_save_used.pop((gid, uid), None)
        if (gid, uid) in random_vow_cds:
            random_vow_cds[(gid, uid)]["save"] = None
        if (gid, uid) in stack_vow_charges:
            stack_vow_charges[(gid, uid)]["save"] = []
    save_cooldowns()
    label = "kill and save cooldowns" if which == "both" else f"{which} cooldown"
    await interaction.response.send_message(f"✅ Reset {label} for {target.mention}.")


@bot.tree.command(name="cooldowns", description="View or set the default cooldown (mods only)")
@app_commands.describe(hours="New default cooldown in hours. Leave blank to view.")
async def slash_cooldowns(interaction: discord.Interaction, hours: float = None):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need the Manage Roles permission.", ephemeral=True)
        return
    if hours is None:
        current = get_default_cooldown(interaction.guild_id)
        await interaction.response.send_message(f"Current default cooldown: **{current}h**", ephemeral=True)
        return
    if hours < 0:
        await interaction.response.send_message("Cooldown must be non-negative.", ephemeral=True)
        return
    if interaction.guild_id not in server_settings:
        server_settings[interaction.guild_id] = {}
    server_settings[interaction.guild_id]["default_cooldown"] = hours
    save_server_settings()
    await interaction.response.send_message(f"✅ Default cooldown set to **{hours}h**")


@bot.tree.command(name="setdefaultrole", description="Set the role required to use GIFs (mods only)")
@app_commands.describe(role="The role to require. Leave blank to view.")
async def slash_setdefaultrole(interaction: discord.Interaction, role: discord.Role = None):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need the Manage Roles permission.", ephemeral=True)
        return
    if role is None:
        current_id = get_default_role(interaction.guild_id)
        role_str = interaction.guild.get_role(current_id).mention if current_id and interaction.guild.get_role(current_id) else "none (everyone)"
        await interaction.response.send_message(f"Current default GIF role: {role_str}", ephemeral=True)
        return
    if interaction.guild_id not in server_settings:
        server_settings[interaction.guild_id] = {}
    server_settings[interaction.guild_id]["default_role_id"] = role.id
    save_server_settings()
    await interaction.response.send_message(f"✅ Default GIF role set to **{role.name}**.")


@bot.tree.command(name="cleardefaultrole", description="Remove the role requirement for using GIFs (mods only)")
async def slash_cleardefaultrole(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_roles and not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You need the Manage Roles permission.", ephemeral=True)
        return
    if interaction.guild_id in server_settings:
        server_settings[interaction.guild_id].pop("default_role_id", None)
        save_server_settings()
    await interaction.response.send_message("✅ Role requirement cleared.")


# =========================
# VOTE COMMANDS
# =========================

VOTE_EMBED_COLOR = discord.Color.gold()


def build_vote_embed(user_id: int) -> discord.Embed:
    embed = discord.Embed(
        title="📥 Vote for a Cooldown Discount!",
        description=(
            "Vote for the bot on Discord Bot List and get **25% off your cooldowns** for 12 hours!\n\n"
            "[🔗 Click here to vote](https://discordbotlist.com/bots/funnything/upvote)"
        ),
        color=VOTE_EMBED_COLOR,
        url="https://discordbotlist.com/bots/funnything/upvote"
    )
    if has_active_vote(user_id):
        expires = vote_expires_in(user_id)
        expires_str = str(expires).split('.')[0] if expires else "soon"
        embed.add_field(name="✅ Your vote is active!", value=f"25% off cooldowns. Expires in **{expires_str}**.", inline=False)
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
    save_cooldowns()
    print(f"[vote] Recorded vote for user {user_id}")
    try:
        user = await bot.fetch_user(user_id)
        if user:
            dm_embed = discord.Embed(
                title="📥 Thanks for voting!",
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
# CLASH RESOLUTION
# =========================

async def finalize_clash(clash_id: int):
    try:
        await asyncio.sleep(CLASH_WINDOW_SECONDS)

        clash_data = pending_clashes.pop(clash_id, None)
        if not clash_data:
            return

        clash_head_lookup.pop(clash_data.get("head_message_id"), None)

        participants = clash_data["participants"]
        channel = clash_data["channel"]
        guild_id = channel.guild.id
        attacker = participants[0]
        attacker_vow = clash_data["attacker_vow"]
        timeout_duration = clash_data["timeout_duration"]
        vow_str = clash_data["vow_str"]
        user_id = clash_data["user_id"]

        if len(participants) < 2:
            return

        if attacker_vow == "Miracle Vow":
            actual_duration = 30
        elif attacker_vow == "Random Vow":
            actual_duration = roll_random_vow_timeout()
            set_random_vow_cd(guild_id, user_id, "kill")
            save_cooldowns()
        else:
            actual_duration = timeout_duration

        # Hakari solo
        if attacker_vow == "Hakari Vow" and len(participants) == 2 and not clash_data.get("target_challenged"):
            original_target = participants[1]
            if random.random() < 0.36:
                if await try_timeout(original_target, discord.utils.utcnow() + timedelta(seconds=251), channel):
                    await channel.send(f"🎰 **JACKPOT!** {original_target.mention} muted 4m11s by {attacker.mention} [Hakari Vow] lmao")
            else:
                if await try_timeout(attacker, discord.utils.utcnow() + timedelta(seconds=90), channel):
                    await channel.send(f"💀 {attacker.mention} [Hakari Vow] lost the gamble — muted 90s lmaooo")
            return

        # No clash, just timeout
        if len(participants) == 2 and not clash_data.get("target_challenged"):
            original_target = participants[1]
            if await try_timeout(original_target, discord.utils.utcnow() + timedelta(seconds=actual_duration), channel):
                await channel.send(f"{original_target.mention} has been timed out for {actual_duration}s by {attacker.mention}{vow_str} lmao")
            return

        # 1v1 clash
        if len(participants) == 2:
            original_target = participants[1]
            attacker_roles = [r.name for r in attacker.roles]
            d_roles = [r.name for r in original_target.roles]
            d_vow = get_active_vow(d_roles)
            attacker_tickets = get_clash_tickets(attacker_roles, guild_id)
            defender_tickets = get_clash_tickets(d_roles, guild_id)

            all_roles_list = [attacker_roles, d_roles]
            await channel.send(pick_clash_gif(all_roles_list))
            if any_gmm(all_roles_list):
                await channel.send("can't clash with someone that strong buddy")
            await asyncio.sleep(3)

            last_kill_used[(guild_id, original_target.id)] = datetime.utcnow()
            save_cooldowns()

            attacker_wins = resolve_clash(attacker_tickets, defender_tickets)
            winner = attacker if attacker_wins else original_target
            loser = original_target if attacker_wins else attacker

            if not attacker_wins and d_vow == "Miracle Vow":
                actual_duration = 30
            elif not attacker_wins and d_vow == "Random Vow":
                actual_duration = roll_random_vow_timeout()
                set_random_vow_cd(guild_id, original_target.id, "kill")
                save_cooldowns()

            if attacker_wins and attacker_vow == "Hakari Vow":
                if random.random() < 0.50:
                    if await try_timeout(original_target, discord.utils.utcnow() + timedelta(seconds=251), channel):
                        await channel.send(f"🎰 **JACKPOT! (clash)** {original_target.mention} muted 4m11s by {attacker.mention} [Hakari Vow]")
                else:
                    if await try_timeout(attacker, discord.utils.utcnow() + timedelta(seconds=90), channel):
                        await channel.send(f"💀 {attacker.mention} [Hakari Vow] won but lost the gamble — muted 90s lmaooo")
            elif not attacker_wins and d_vow == "Hakari Vow":
                if random.random() < 0.50:
                    if await try_timeout(attacker, discord.utils.utcnow() + timedelta(seconds=251), channel):
                        await channel.send(f"🎰 **JACKPOT! (clash)** {attacker.mention} muted 4m11s by {original_target.mention} [Hakari Vow]")
                else:
                    if await try_timeout(original_target, discord.utils.utcnow() + timedelta(seconds=90), channel):
                        await channel.send(f"💀 {original_target.mention} [Hakari Vow] won but lost the gamble — muted 90s lmaooo")
            else:
                if await try_timeout(loser, discord.utils.utcnow() + timedelta(seconds=actual_duration), channel):
                    await channel.send(f"{winner.mention} WON\n{loser.mention} get timed out")
            return

        # Multi-way clash (3-10)
        all_roles_list = [[r.name for r in p.roles] for p in participants]
        await channel.send(pick_clash_gif(all_roles_list))
        await channel.send(f"⚔️ **{len(participants)}-WAY CLASH!**")
        if any_gmm(all_roles_list):
            await channel.send("can't clash with someone that strong buddy")
        await asyncio.sleep(3)

        now_snap = datetime.utcnow()
        for p in participants[1:]:
            last_kill_used[(guild_id, p.id)] = now_snap
        save_cooldowns()

        ticket_list = [(p, get_clash_tickets([r.name for r in p.roles], guild_id)) for p in participants]
        total_tickets = sum(t for _, t in ticket_list)
        roll = random.randint(1, total_tickets)
        cumulative = 0
        winner = None
        for member, tickets in ticket_list:
            cumulative += tickets
            if roll <= cumulative:
                winner = member
                break

        losers = [p for p in participants if p.id != winner.id]
        await channel.send(f"🏆 {winner.mention} WON the {len(participants)}-way clash!")
        for loser in losers:
            if await try_timeout(loser, discord.utils.utcnow() + timedelta(seconds=actual_duration), channel):
                await channel.send(f"{loser.mention} gets timed out!")

    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"[ERROR] finalize_clash {clash_id}: {e}\n{traceback.format_exc()}")


# =========================
# MESSAGE EVENT
# =========================

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_roles = [role.name for role in message.author.roles]
    gid = message.guild.id
    uid = message.author.id

    if bot.user in message.mentions:
        role_cooldowns = get_role_cooldowns(gid)
        valid_roles_for_mention = [r for r in author_roles if r in role_cooldowns]
        default_role_id_for_mention = get_default_role(gid)
        has_named_role_mention = bool(valid_roles_for_mention)
        has_required_role_mention = (
            default_role_id_for_mention is not None and
            any(r.id == default_role_id_for_mention for r in message.author.roles)
        )
        if default_role_id_for_mention is not None and not has_named_role_mention and not has_required_role_mention:
            required_role = message.guild.get_role(default_role_id_for_mention)
            role_name = required_role.name if required_role else "the required role"
            await message.channel.send(
                f"{message.author.mention}, you can only use GIFs if you have the **{role_name}** role. "
                f"Subscribe to the Patreon for early access: https://www.patreon.com/15981390/join"
            )
            return
        msg = build_cooldown_status(message.author, gid)
        await message.channel.send(msg)
        return

    if not message.reference:
        await bot.process_commands(message)
        return

    content = message.content
    is_kill_gif = any(gif in content for gif in TARGET_GIFS)
    is_save_gif = any(gif in content for gif in UNTIMEOUT_GIFS)

    # =========================
    # CLASH JOIN CHECK
    # =========================
    if is_kill_gif and message.reference.message_id in clash_head_lookup:
        clash_id = clash_head_lookup[message.reference.message_id]
        clash_data = pending_clashes.get(clash_id)
        if clash_data:
            participants = clash_data["participants"]
            if (
                len(participants) >= 2
                and uid == participants[1].id
                and not clash_data.get("target_challenged")
            ):
                clash_data["target_challenged"] = True
                clash_head_lookup.pop(clash_data["head_message_id"], None)
                clash_data["head_message_id"] = message.id
                clash_head_lookup[message.id] = clash_id
                if not clash_data["task"].done():
                    clash_data["task"].cancel()
                await message.channel.send(f"⚔️ {participants[1].mention} is fighting back! Reply to their GIF to join!")
                clash_data["task"] = asyncio.create_task(finalize_clash(clash_id))
            elif len(participants) < 10:
                already_in = uid in [p.id for p in participants]
                if not already_in:
                    new_member = message.guild.get_member(uid)
                    if new_member:
                        participants.append(new_member)
                        clash_head_lookup.pop(clash_data["head_message_id"], None)
                        clash_data["head_message_id"] = message.id
                        clash_head_lookup[message.id] = clash_id
                        if not clash_data["task"].done():
                            clash_data["task"].cancel()
                        await message.channel.send(
                            f"{new_member.mention} jumped into the clash! ⚔️ **{len(participants)} fighters** — reply to their GIF to also join!"
                        )
                        clash_data["task"] = asyncio.create_task(finalize_clash(clash_id))
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

    role_cooldowns = get_role_cooldowns(gid)
    valid_roles = [r for r in author_roles if r in role_cooldowns]
    default_cd = get_default_cooldown(gid)
    default_role_id = get_default_role(gid)

    has_named_role = bool(valid_roles)
    has_required_role = (
        default_role_id is not None and
        any(r.id == default_role_id for r in message.author.roles)
    )

    if default_role_id is not None and not has_named_role and not has_required_role:
        required_role = message.guild.get_role(default_role_id)
        role_name = required_role.name if required_role else "the required role"
        await message.channel.send(
            f"{message.author.mention}, you need the **{role_name}** role to use GIFs! "
            f"Subscribe to the Patreon for early access: https://www.patreon.com/15981390/join"
        )
        return

    if valid_roles:
        best_role = min(valid_roles, key=lambda r: role_cooldowns[r])
        base_cd = role_cooldowns[best_role]
        role_label = best_role
    else:
        base_cd = default_cd
        role_label = f"default ({default_cd}h)"

    vow = get_active_vow(author_roles)
    now = datetime.utcnow()
    action = "kill" if is_kill_gif else "save"

    if vow == "CONFLICT":
        await message.channel.send(
            f"{message.author.mention}, ⚠️ you have multiple Binding Vow roles — vows are being ignored."
        )
        vow = None

    # =========================
    # BITCHOUT VOW
    # =========================
    if is_kill_gif:
        defender_roles = [r.name for r in member_to_timeout.roles]
        defender_vow = get_active_vow(defender_roles)
        if defender_vow == "Bitchout Vow" and GMM_ROLE not in author_roles:
            await message.channel.send(f"{member_to_timeout.mention} has **Bitchout Vow** — they're immune to guhs!")
            return

    if vow == "Bitchout Vow":
        if action == "kill":
            await message.channel.send("you're a bitch but a guh free bitch atleast")
        else:
            await message.channel.send(f"{message.author.mention}, your **Bitchout Vow** forbids you from saving. 🪹")
        return

    # =========================
    # STACK VOW
    # =========================
    if vow == "Stack Vow":
        sv_cd = base_cd * STACK_VOW_MULTIPLIER
        available = stack_vow_available_charges(gid, uid, action, sv_cd, now)
        if available == 0:
            next_regen = stack_vow_next_regen(gid, uid, action, sv_cd, now)
            await message.channel.send(
                f"{message.author.mention}, [Stack Vow] no {action} charges left — next charge in **{str(next_regen).split('.')[0]}**"
            )
            return
        stack_vow_consume_charge(gid, uid, action, now)
        remaining_after = available - 1
        vow_str = f" [Stack Vow | {remaining_after}/{STACK_VOW_MAX_CHARGES} {action} charges left]"

    # =========================
    # RANDOM VOW
    # =========================
    elif vow == "Random Vow":
        rv_cd = get_random_vow_cd(gid, uid, action)
        last = last_kill_used.get((gid, uid)) if action == "kill" else last_save_used.get((gid, uid))
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
        miracle_cd = apply_vote_discount(base_cd * 2.5, uid)
        last = last_kill_used.get((gid, uid)) if action == "kill" else last_save_used.get((gid, uid))
        if last and now - last < timedelta(hours=miracle_cd):
            remaining = timedelta(hours=miracle_cd) - (now - last)
            await message.channel.send(
                f"{message.author.mention}, [Miracle Vow] cooldown remaining: **{str(remaining).split('.')[0]}**"
            )
            return
        vow_str = " [Miracle Vow]"

    # =========================
    # RAGEBAIT VOW
    # =========================
    elif vow == "Ragebait Vow":
        if action == "save":
            save_cd = apply_vote_discount(base_cd, uid)
            last = last_save_used.get((gid, uid))
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
        effective_cd = apply_vote_discount(apply_vow(base_cd, action, vow), uid)
        vow_str = format_vow_label(vow)
        vote_label = " 📥 25% off" if has_active_vote(uid) else ""

        if effective_cd == -1.0:
            await message.channel.send(f"{message.author.mention}, your {vow} forbids you from this action. 🪹")
            return

        last = last_kill_used.get((gid, uid)) if action == "kill" else last_save_used.get((gid, uid))

        if effective_cd > 0 and last:
            if now - last < timedelta(hours=effective_cd):
                remaining = timedelta(hours=effective_cd) - (now - last)

                if is_kill_gif:
                    target_roles = [r.name for r in member_to_timeout.roles]
                    target_vow = get_active_vow(target_roles)
                    if target_vow == "Miracle Vow":
                        if not can_gain_miracle_from_failed_timeout(gid, member_to_timeout.id):
                            await message.channel.send(
                                f"{message.author.mention}, ({role_label}{vow_str}) cooldown remaining: {str(remaining).split('.')[0]}"
                            )
                            return
                        new_count = add_miracle(gid, member_to_timeout.id)
                        record_miracle_gain_from_failed_timeout(gid, member_to_timeout.id)
                        save_cooldowns()
                        if new_count == -1:
                            await message.channel.send(
                                f"{message.author.mention}, ({role_label}{vow_str}) cooldown remaining: {str(remaining).split('.')[0]}\n"
                                f"{member_to_timeout.mention} is already at max miracles ({MIRACLE_MAX}/{MIRACLE_MAX})!"
                            )
                        else:
                            await message.channel.send(
                                f"{message.author.mention}, ({role_label}{vow_str}) cooldown remaining: {str(remaining).split('.')[0]}\n"
                                f"✨ {member_to_timeout.mention} got a miracle! They now have **{new_count}/{MIRACLE_MAX}** miracles."
                            )
                        return

                await message.channel.send(
                    f"{message.author.mention}, ({role_label}{vow_str}{vote_label}) cooldown remaining: {str(remaining).split('.')[0]}"
                )
                return

        if action == "kill":
            last_kill_used[(gid, uid)] = now
            save_cooldowns()

    # =========================
    # SAVE GIF
    # =========================
    if is_save_gif:
        if not member_to_timeout.timed_out_until:
            await message.channel.send("They're not even timed out bro 💀")
            if action == "save":
                if vow == "Stack Vow":
                    user_data = stack_vow_charges.get((gid, uid), {})
                    if user_data.get("save"):
                        user_data["save"].pop()
                elif vow != "Random Vow":
                    last_save_used.pop((gid, uid), None)
            return

        remaining = member_to_timeout.timed_out_until - discord.utils.utcnow()
        if remaining.total_seconds() <= 90:
            if await try_untimeout(member_to_timeout, message.channel):
                if vow == "Random Vow":
                    last_save_used[(gid, uid)] = now
                    set_random_vow_cd(gid, uid, "save")
                elif vow == "Miracle Vow":
                    last_save_used[(gid, uid)] = now
                elif vow == "Ragebait Vow":
                    last_save_used[(gid, uid)] = now
                elif vow != "Stack Vow":
                    last_save_used[(gid, uid)] = now
                save_cooldowns()
                await message.channel.send(
                    f"{member_to_timeout.mention} has been freed early by {message.author.mention}{vow_str}"
                )
                if vow == "Miracle Vow":
                    new_count = add_miracle(gid, uid)
                    save_cooldowns()
                    if new_count == -1:
                        await message.channel.send(f"{message.author.mention} is already at max miracles ({MIRACLE_MAX}/{MIRACLE_MAX})!")
                    else:
                        await message.channel.send(f"✨ {message.author.mention} got a miracle for saving! They now have **{new_count}/{MIRACLE_MAX}** miracles.")
                saved_roles = [r.name for r in member_to_timeout.roles]
                saved_vow = get_active_vow(saved_roles)
                if saved_vow == "Miracle Vow":
                    new_count = add_miracle(gid, member_to_timeout.id)
                    save_cooldowns()
                    if new_count == -1:
                        await message.channel.send(f"{member_to_timeout.mention} is already at max miracles ({MIRACLE_MAX}/{MIRACLE_MAX})!")
                    else:
                        await message.channel.send(f"✨ {member_to_timeout.mention} got a miracle from being saved! They now have **{new_count}/{MIRACLE_MAX}** miracles.")
        else:
            await message.channel.send(f"Too long left on timeout ({int(remaining.total_seconds())}s). Can't save them.")
        await bot.process_commands(message)
        return

    # =========================
    # KILL GIF
    # =========================
    if is_kill_gif:
        if vow == "Ragebait Vow":
            if is_ragebait_on_cd(gid, uid, now):
                remaining = get_ragebait_remaining(gid, uid, now)
                await message.channel.send(
                    f"{message.author.mention}, [Ragebait Vow] ability on cooldown: **{str(remaining).split('.')[0]}**"
                )
                return
            last_kill_used[(gid, member_to_timeout.id)] = now
            ragebait_last_used[(gid, uid)] = now
            save_cooldowns()
            await message.channel.send(
                f"{message.author.mention} [Ragebait Vow] raged at {member_to_timeout.mention}! Their kill guh is now on CD."
            )
            await bot.process_commands(message)
            return

        timeout_duration = 180 if vow == "Destruction Vow" else TIMEOUT_SECONDS

        if vow == "Random Vow":
            last_kill_used[(gid, uid)] = now
            save_cooldowns()
        elif vow == "Miracle Vow":
            last_kill_used[(gid, uid)] = now
            save_cooldowns()

        attacker = message.author
        original_target = member_to_timeout
        clash_id = message.id
        attacker_vow = vow

        # Miracle block check
        defender_roles_list = [r.name for r in original_target.roles]
        defender_vow_check = get_active_vow(defender_roles_list)
        if defender_vow_check == "Miracle Vow":
            miracles = get_miracle_count(gid, original_target.id)
            if miracles >= MIRACLE_BLOCK_COST:
                consume_miracles(gid, original_target.id, MIRACLE_BLOCK_COST)
                save_cooldowns()
                await message.channel.send(
                    f"{MIRACLE_BLOCK_GIF}\n"
                    f"✨ {original_target.mention}'s miracle blocked the guh! {MIRACLE_BLOCK_COST} miracles consumed. "
                    f"They now have **{get_miracle_count(gid, original_target.id)}/{MIRACLE_MAX}** miracles."
                )
                if vow == "Random Vow":
                    last_kill_used.pop((gid, uid), None)
                elif vow == "Stack Vow":
                    user_data = stack_vow_charges.get((gid, uid), {})
                    if user_data.get("kill"):
                        user_data["kill"].pop()
                elif vow != "Miracle Vow":
                    last_kill_used.pop((gid, uid), None)
                save_cooldowns()
                await bot.process_commands(message)
                return

        clash_entry = {
            "participants": [attacker, original_target],
            "head_message_id": message.id,
            "channel": message.channel,
            "timeout_duration": timeout_duration,
            "attacker_vow": attacker_vow,
            "vow_str": vow_str,
            "user_id": uid,
            "task": None,
        }
        pending_clashes[clash_id] = clash_entry
        clash_head_lookup[message.id] = clash_id
        clash_entry["task"] = asyncio.create_task(finalize_clash(clash_id))

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
