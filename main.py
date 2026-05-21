#main.py
import requests
import time
import random
import threading
from db_helper import connect_to_database
from telegramapi import TelegramBotAPI
from models import User,UserProfile
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")+BOT_TOKEN

# -------------------------
# Telegram Helper
# -------------------------

from telegramapi import TelegramBotAPI

bot = TelegramBotAPI(BASE_URL)


# -------------------------
# Game Storage
# -------------------------

waiting_markets = {
    "energy": None,
    "tech": None,
    "agro": None
}

games = {}
player_game = {}
profile_edit_state = {}

WAR_PRESSURE_INTERVAL = 3
WAR_PRESSURE_DAMAGE = 1

war_pressure_tasks = {}


async def war_pressure(game_id):

    while True:

        await asyncio.sleep(WAR_PRESSURE_INTERVAL)

        if game_id not in games:
            return

        game = games[game_id]

        if game["state"] != "war_decision":
            return

        for p in game["players"]:
            uid = p["id"]

            if uid not in game["war_choices"]:
                game["war_penalty"][uid] -= WAR_PRESSURE_DAMAGE

                await bot.send_message(
                    uid,
                    f"⏳ Pressure! -{WAR_PRESSURE_DAMAGE} score"
                )

async def start_chicken(game_id):
    game = games[game_id]
    game["state"] = "war_decision"
    game["chat_enabled"] = False

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🕊 Yield", "callback_data": "war_yield"},
                {"text": "🚗 Straight", "callback_data": "war_straight"},
            ]
        ]
    }

    for p in game["players"]:
        await bot.send_message(p["id"], "War mode: choose your move:", keyboard)
    war_pressure_tasks[game_id] = asyncio.create_task(war_pressure(game_id))



async def resolve_war_advantage(game_id):
    game = games[game_id]
    p1, p2 = game["players"]
    s1 = game["strategy"].get(p1["id"])
    s2 = game["strategy"].get(p2["id"])

    # امتیازدهی ساده برای حالت «یکی جنگ یکی مذاکره»
    if s1 == "war" and s2 == "negotiation":
        r1, r2 = 3, -2
    elif s1 == "negotiation" and s2 == "war":
        r1, r2 = -2, 3
    else:
        r1, r2 = 0, 0  # نباید رخ دهد

    result = f"""
Market: {game['market'].upper()}
Mode: WAR (Advantage)

{p1['name']}: {s1}
{p2['name']}: {s2}

Scores:
{p1['name']}: {r1}
{p2['name']}: {r2}
"""
    for p in game["players"]:
        await bot.send_message(p["id"], result)

    del player_game[p1["id"]]
    del player_game[p2["id"]]
    del games[game_id]


async def resolve_chicken(game_id):
    game = games[game_id]
    p1, p2 = game["players"]
    c1 = game["war_choices"][p1["id"]]   # "yield" | "straight"
    c2 = game["war_choices"][p2["id"]]

    # ماتریس متعادل پیشنهادی
    if c1 == "yield" and c2 == "yield":
        r1, r2 = 0, 0
    elif c1 == "yield" and c2 == "straight":
        r1, r2 = -1, 2
    elif c1 == "straight" and c2 == "yield":
        r1, r2 = 2, -1
    else:
        r1, r2 = -5, -5

    result = f"""
Market: {game['market'].upper()}
Mode: CHICKEN (War)

{p1['name']}: {c1}
{p2['name']}: {c2}

Scores:
{p1['name']}: {r1}
{p2['name']}: {r2}
"""
    r1 += game["war_penalty"][p1["id"]]
    r2 += game["war_penalty"][p2["id"]]

    for p in game["players"]:
        await bot.send_message(p["id"], result)

    del player_game[p1["id"]]
    del player_game[p2["id"]]
    del games[game_id]

async def create_game(p1, p2, market):

    game_id = random.randint(1000, 9999)

    games[game_id] = {
        "players": [p1, p2],
        "choices": {},
        "state": "waiting_scenario",
        "chat_enabled": False,
        "market": market,
        "strategy": {},          # user_id -> "negotiation" | "war"
        "mode": None,            # "prisoner" | "chicken" | "war_advantage"
        "war_choices": {},        # user_id -> "yield" | "straight"
        "war_penalty": {p1["id"]: 0, p2["id"]: 0}
    }

    player_game[p1["id"]] = game_id
    player_game[p2["id"]] = game_id

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🤝 Negotiation", "callback_data": "strategy_negotiation"},
                {"text": "⚔️ War", "callback_data": "strategy_war"},
            ]
        ]
    }

    await bot.send_message(p1["id"], f"Matched in {market.upper()} market!\nChoose your approach:", keyboard)
    await bot.send_message(p2["id"], f"Matched in {market.upper()} market!\nChoose your approach:", keyboard)


# -------------------------
# Scenario Phase
# -------------------------
async def negotiation_timer(game_id):
    await asyncio.sleep(120)
    if game_id in games:
        await start_decision(game_id)


async def start_negotiation(game_id):

    game = games[game_id]
    game["state"] = "negotiation"
    game["chat_enabled"] = True

    scenario_text = """
You and your partner were arrested.

You can talk for 2 minutes.
Convince each other before deciding.
"""

    for p in game["players"]:
      await bot.send_message(p["id"], scenario_text)

    # timer 2 دقیقه
    asyncio.create_task(negotiation_timer(game_id))



async def start_decision(game_id):

    if game_id not in games:
        return

    game = games[game_id]
    game["state"] = "decision"
    game["chat_enabled"] = False

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Cooperate", "callback_data": "cooperate"},
                {"text": "defect", "callback_data": "defect"}
            ]
        ]
    }

    for p in game["players"]:
      await bot.send_message(p["id"], "Time's up. Make your decision:", keyboard)


# -------------------------
# Resolve
# -------------------------

async def resolve_game(game_id):

    game = games[game_id]
    market = game["market"]

    p1, p2 = game["players"]
    c1 = game["choices"][p1["id"]]
    c2 = game["choices"][p2["id"]]

    # -------- MARKET PAYOFFS --------

    if market == "energy":
        coop, betray, both = 4, 6, -1

    elif market == "tech":
        coop, betray, both = 3, 5, 1

    elif market == "agro":
        coop, betray, both = 2, 3, 1

    # -------- PAYOFF LOGIC --------

    if c1 == "cooperate" and c2 == "cooperate":
        r1, r2 = coop, coop
    elif c1 == "cooperate" and c2 == "defect":
        r1, r2 = 0, betray
    elif c1 == "defect" and c2 == "cooperate":
        r1, r2 = betray, 0
    else:
        r1, r2 = both, both

    result = f"""
Market: {market.upper()}

Results

{p1['name']}: {c1}
{p2['name']}: {c2}

Scores:
{p1['name']}: {r1}
{p2['name']}: {r2}
"""

    for p in game["players"]:
        await bot.send_message(p["id"], result)

    del player_game[p1["id"]]
    del player_game[p2["id"]]
    del games[game_id]


# -------------------------
# Command Handling
# -------------------------

async def handle_play(user):

    if user["id"] in player_game:
        await bot.send_message(user["id"], "Already in game.")
        return

    keyboard = {
        "inline_keyboard": [
            [{"text": "⚡ Energy Market", "callback_data": "market_energy"}],
            [{"text": "💻 Tech Market", "callback_data": "market_tech"}],
            [{"text": "🌾 Agro Market", "callback_data": "market_agro"}]
        ]
    }

    await bot.send_message(user["id"], "Choose a market:", keyboard)


async def handle_text_message(msg):

    user_id = msg["from"]["id"]
    user_name = msg["from"]["first_name"]
    text = msg.get("text", "")

    # --- profile edit mode ---
    if user_id in profile_edit_state:
        field = profile_edit_state[user_id]
        user = await get_or_create_user(user_id, user_name)

        if field == "edit_first_name":
            user.first_name = text
        elif field == "edit_last_name":
            user.last_name = text
        elif field == "edit_bio":
            user.bio = text

        await user.save()
        del profile_edit_state[user_id]

        await bot.send_message(user_id, "Profile updated successfully.")
        await handle_profile(user_id)
        return

    # --- game chat mode ---
    if user_id not in player_game:
        return

    game_id = player_game[user_id]
    game = games[game_id]

    if game["chat_enabled"]:
        for p in game["players"]:
            if p["id"] != user_id:
                await bot.send_message(p["id"], f"{user_name}: {text}")

async def start_profile_edit(user_id, field):
    profile_edit_state[user_id] = field

    prompts = {
        "edit_first_name": "Send your new first name:",
        "edit_last_name": "Send your new last name:",
        "edit_bio": "Send your new bio:"
    }

    await bot.send_message(user_id, prompts[field])

async def get_or_create_user(user_id, default_first_name=None):

    user = await UserProfile.find_one(UserProfile.telegram_id == user_id)

    if not user:
        user = UserProfile(
            telegram_id=user_id,
            first_name=default_first_name or "",
            last_name="",
            bio="",
            wins=0,
            games=0,
            loses=0,
            score=0
        )

        await user.insert()

    return user


async def handle_callback(callback):
    user_id = callback["from"]["id"]
    data = callback["data"]

    # --- Market Selection ---
    if data.startswith("market_"):
        market = data.split("_")[1]
        if waiting_markets[market] is None:
            waiting_markets[market] = callback["from"]
            await bot.send_message(user_id, f"Waiting for opponent in {market} market...")
        else:
            opponent = waiting_markets[market]
            waiting_markets[market] = None

            p1 = {"id": opponent["id"], "name": opponent["first_name"]}
            p2 = {"id": callback["from"]["id"], "name": callback["from"]["first_name"]}

            await create_game(p1, p2, market)
        return

    # --- Profile edit allowed even outside game ---
    if data in ["edit_first_name", "edit_last_name", "edit_bio"] and user_id not in player_game:
        await start_profile_edit(user_id, data)
        return

    # از اینجا به بعد باید داخل بازی باشد
    if user_id not in player_game:
        return

    game_id = player_game[user_id]
    game = games[game_id]

    # --- Strategy selection (NEW) ---
    if data.startswith("strategy_") and game["state"] == "waiting_scenario":
        strategy = data.split("_", 1)[1]  # "negotiation" | "war"
        game["strategy"][user_id] = strategy
        await bot.send_message(user_id, f"You chose: {strategy}")

        if len(game["strategy"]) == 2:
            s_values = set(game["strategy"].values())
            if s_values == {"negotiation"}:
                game["mode"] = "prisoner"
                await start_negotiation(game_id)
            elif s_values == {"war"}:
                game["mode"] = "chicken"
                await start_chicken(game_id)
            else:
                game["mode"] = "war_advantage"
                await resolve_war_advantage(game_id)
        return

    # --- Prisoner decision ---
    if data in ["cooperate", "defect"] and game["state"] == "decision":
        game["choices"][user_id] = data
        await bot.send_message(user_id, f"You chose: {data}")
        if len(game["choices"]) == 2:
            await resolve_game(game_id)
        return

    # --- Chicken decision ---
    if data in ["war_yield", "war_straight"] and game["state"] == "war_decision":
        move = "yield" if data == "war_yield" else "straight"
        game["war_choices"][user_id] = move
        await bot.send_message(user_id, f"You chose: {move}")
        if len(game["war_choices"]) == 2:
            task = war_pressure_tasks.get(game_id)
            if task:
                task.cancel()
            await resolve_chicken(game_id)
        return

    # --- Profile edit inside game too ---
    if data in ["edit_first_name", "edit_last_name", "edit_bio"]:
        await start_profile_edit(user_id, data)
        return


async def handle_profile(user_id):
    user = await get_or_create_user(user_id)

    text = f"""Your profile:

First name: {user.first_name}
Last name: {user.last_name}
Bio: {user.bio}

Wins: {user.wins}
Games: {user.games}
Losses: {user.loses}
Score: {user.score}
"""

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Edit First Name", "callback_data": "edit_first_name"},
                {"text": "Edit Last Name", "callback_data": "edit_last_name"}
            ],
            [
                {"text": "Edit Bio", "callback_data": "edit_bio"}
            ]
        ]
    }

    await bot.send_message(user_id, text, keyboard)

# -------------------------
# Polling Loop
# -------------------------

async def polling():

    offset = None

    while True:

        updates = await bot.get_updates(offset)

        for update in updates["result"]:

            offset = update["update_id"] + 1

            if "message" in update:

                msg = update["message"]
                text = msg.get("text", "")

                user = {
                    "id": msg["from"]["id"],
                    "name": msg["from"]["first_name"]
                }

                if text == "/start":
                    await bot.send_message(user["id"], "Use /play to start.")

                elif text == "/play":
                    await handle_play(user)

                elif text == "/profile":
                    await handle_profile(user["id"])

                else:
                    await handle_text_message(msg)

            elif "callback_query" in update:
                await handle_callback(update["callback_query"])

        await asyncio.sleep(1)


async def main():

    global session
    await connect_to_database()
    await bot.start() 

    print("Bot started")

    await polling()


if __name__ == "__main__":
    asyncio.run(main())

