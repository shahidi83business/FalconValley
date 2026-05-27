import asyncio
import os
import logging
from dotenv import load_dotenv

# Helpers & Models
from db_helper import connect_to_database
from telegramapi import TelegramBotAPI
from models import UserProfile
from marketfactory import MarketFactory
from manager import game_manager  # مدیریت مرکزی بازی‌ها
from engine import GameEngine      # موتور محاسبات نتایج
from ui import UI                  # کلاس رابط کاربری که ساختیم

load_dotenv()
bot = TelegramBotAPI(os.getenv("BASE_URL") + os.getenv("BOT_TOKEN"))
market_factory = MarketFactory()

# استیت‌های موقت برای خارج از بازی (مثل ساخت مارکت یا ویرایش پروفایل)
user_context = {} 
waiting_queue = {} # market_id -> user_data

# -------------------------
# Core Game Logic
# -------------------------

async def handle_strategy_logic(game, user_id, strategy):
    """مدیریت انتخاب استراتژی و هدایت به فاز بعدی"""
    game.strategy[user_id] = strategy
    await bot.send_message(user_id, f"✅ Strategy {strategy.upper()} locked.")

    if len(game.strategy) == 2:
        s1, s2 = list(game.strategy.values())
        
        if s1 == "negotiation" and s2 == "negotiation":
            await game.start_negotiation()
            for p in game.players:
                await bot.send_message(p["id"], "🤝 Both chose Negotiation. 2 minutes to chat!", 
                                     reply_markup=None)
            asyncio.create_task(negotiation_timeout(game))
            
        elif s1 == "war" and s2 == "war":
            await game.start_chicken()
            for p in game.players:
                await bot.send_message(p["id"], "⚠️ WAR! Entering Chicken Game phase...", 
                                     reply_markup=UI.get_chicken_buttons())
        else:
            # حالت Advantage (یکی جنگ، یکی مذاکره)
            results = GameEngine.calculate_war_advantage(game)
            await finalize_game(game, results)

async def negotiation_timeout(game):
    """تایمر پایان مذاکره"""
    await asyncio.sleep(120)
    if game.game_id in game_manager.games and game.state == "negotiation":
        await game.start_decision()
        for p in game.players:
            await bot.send_message(p["id"], "⌛ Time's up! Make your final decision:", 
                                 reply_markup=UI.get_negotiation_buttons())

async def finalize_game(game, results):
    """نمایش نتایج و بستن بازی در منیجر"""
    text = GameEngine.generate_result_text(game, results)
    for p in game.players:
        await bot.send_message(p["id"], text)
    await game_manager.end_game(game.game_id)

# -------------------------
# Event Handlers
# -------------------------

async def handle_callback(callback):
    user_id = callback["from"]["id"]
    data = callback["data"]
    user_name = callback["from"]["first_name"]

    # ۱. مدیریت Matchmaking
    if data.startswith("market_"):
        m_id = data.replace("market_", "")
        if waiting_queue.get(m_id) is None:
            waiting_queue[m_id] = {"id": user_id, "name": user_name}
            await bot.send_message(user_id, f"🔍 Searching for opponent in {m_id}...")
        else:
            opponent = waiting_queue.pop(m_id)
            game = await game_manager.create_game(opponent, {"id": user_id, "name": user_name}, m_id)
            for p in game.players:
                await bot.send_message(p["id"], "🎮 Match Found!", reply_markup=UI.get_strategy_buttons())
        return

    # ۲. پیدا کردن بازی کاربر
    game = game_manager.get_game(user_id)
    if not game: return

    # ۳. هندلینگ دکمه‌های بازی بر اساس وضعیت FSM
    if data.startswith("strat_") and game.state == "waiting_strategy":
        await handle_strategy_logic(game, user_id, data.replace("strat_", ""))

    elif data.startswith("choice_") and game.state == "decision":
        game.choices[user_id] = data.replace("choice_", "")
        if len(game.choices) == 2:
            payoffs = market_factory.get(game.market_id).payoff
            results = GameEngine.calculate_standard_results(game, payoffs)
            await finalize_game(game, results)

    elif data.startswith("war_") and game.state == "war_decision":
        game.war_choices[user_id] = data.replace("war_", "")
        if len(game.war_choices) == 2:
            results = GameEngine.calculate_chicken_results(game)
            await finalize_game(game, results)

async def handle_text(msg):
    user_id = msg["from"]["id"]
    text = msg.get("text", "")

    # اگر در حال چت در فاز مذاکره است
    game = game_manager.get_game(user_id)
    if game and game.state == "negotiation":
        opponent_id = [p["id"] for p in game.players if p["id"] != user_id][0]
        await bot.send_message(opponent_id, f"💬 {msg['from']['first_name']}: {text}")
        return

    # دستورات پایه
    if text == "/play":
        profile = await UserProfile.find_one(UserProfile.telegram_id == user_id)
        # فرض بر این است که متد زیر در UI مارکت‌ها را می‌سازد
        await bot.send_message(user_id, "Select Market:", reply_markup=UI.get_market_selection([], ["energy", "tech", "agro"]))
    elif text == "/profile":
        # نمایش پروفایل با دکمه‌های UI
        await bot.send_message(user_id, "Your Profile:", reply_markup=UI.get_profile_menu())

# -------------------------
# Main Entry
# -------------------------

async def main():
    await connect_to_database()
    await market_factory.load_from_db()
    print("🤖 Bot is running...")
    
    offset = None
    while True:
        updates = await bot.get_updates(offset)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1
            if "message" in update:
                await handle_text(update["message"])
            elif "callback_query" in update:
                await handle_callback(update["callback_query"])
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())
