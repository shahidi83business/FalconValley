#main.py
import asyncio
import os
import logging
from dotenv import load_dotenv

# Helpers & Models
from db_helper import connect_to_database
from telegramapi import TelegramBotAPI
from models import UserProfile,Scenario, Decision
from marketfactory import MarketFactory
from manager import game_manager  # مدیریت مرکزی بازی‌ها
from engine import GameEngine      # موتور محاسبات نتایج
from ui import UI                  # کلاس رابط کاربری که ساختیم
from questionfactory import QuestionFactory
from judge_service import JudgeService
from deal_service import DealService
from callback_manager import CallbackManager

load_dotenv()
bot = TelegramBotAPI(os.getenv("BASE_URL") + os.getenv("BOT_TOKEN"))
market_factory = MarketFactory()

question_factory = QuestionFactory()
judge = JudgeService()

user_context = {} 
waiting_queue = {} 

active_quiz_users = set()  # کاربرهایی که باید هر دقیقه سوال بگیرن

# وضعیت سوال جاری هر کاربر (pending)
quiz_state = {
    # user_id: {"pending_scenario_id": "...", "mode": "solo"|"pvp", "game_id": "..."}
}

callback_manager = None


def clear_user_quiz_pending(user_id):
    """
    وقتی کاربر وارد بازی می‌شود، سؤال solo باز او را پاک می‌کنیم
    تا بعداً به سؤال قدیمی جواب ندهد.
    """
    st = quiz_state.setdefault(
        user_id,
        {
            "pending_scenario_id": None,
            "mode": "solo",
            "market_id": "global"
        }
    )
    st["pending_scenario_id"] = None

# -------------------------
# Core Game Logic
# -------------------------

async def handle_strategy_logic(game, user_id, strategy):
    """مدیریت انتخاب استراتژی و هدایت به فاز بعدی"""

    if user_id in game.strategy:
        await bot.send_message(user_id, "قبلاً استراتژی‌ات را انتخاب کردی.")
        return

    game.strategy[user_id] = strategy

    await bot.send_message(
        user_id,
        f"✅ Strategy {strategy.upper()} locked. منتظر انتخاب حریف..."
    )

    if len(game.strategy) < 2:
        return

    s1, s2 = list(game.strategy.values())

    if s1 == "negotiation" and s2 == "negotiation":
        await game.start_negotiation()

        for p in game.players:
            await bot.send_message(
                p["id"],
                "🤝 هر دو مذاکره را انتخاب کردید. ۲ دقیقه فرصت چت دارید!",
                reply_markup=None
            )

        asyncio.create_task(negotiation_timeout(game))

    elif s1 == "war" and s2 == "war":
        await game.start_chicken()

        for p in game.players:
            await bot.send_message(
                p["id"],
                "⚠️ هر دو جنگ را انتخاب کردید! وارد Chicken Game شدید.",
                reply_markup=UI.get_chicken_buttons()
            )

    else:
        results = GameEngine.calculate_war_advantage_results(game)
        await finalize_game(game, results)

async def negotiation_timeout(game):
    """تایمر پایان مذاکره"""
    await asyncio.sleep(120)
    print(game.state)
    if game.game_id in game_manager.games and game.state == "waiting_negotiation":
        await game.start_decision()
        for p in game.players:
            await bot.send_message(p["id"], "⌛ Time's up! Make your final decision:", 
                                 reply_markup=UI.get_negotiation_buttons())

async def finalize_game(game, results):
    text = GameEngine.generate_result_text(game, results)

    for p in game.players:
        user_id = p["id"]

        await bot.send_message(user_id, text)

        st = quiz_state.setdefault(
            user_id,
            {
                "pending_scenario_id": None,
                "mode": "solo",
                "market_id": game.market_id
            }
        )

        st["mode"] = "solo"
        st["pending_scenario_id"] = None
        st["market_id"] = game.market_id

    await game_manager.end_game(game.game_id)

async def send_quiz_question(user_id, market_id="global", topic="general", difficulty="easy"):
    """
    ارسال یک سؤال solo به کاربر.
    اگر کاربر داخل بازی باشد یا سؤال pending داشته باشد، سؤال جدید نمی‌فرستد.
    """

    # اگر داخل بازی دو نفره است، سؤال solo نفرست
    if game_manager.get_game(user_id):
        return

    st = quiz_state.setdefault(
        user_id,
        {
            "pending_scenario_id": None,
            "mode": "solo",
            "market_id": market_id
        }
    )

    # اگر هنوز به سؤال قبلی جواب نداده، سؤال جدید نفرست
    if st.get("pending_scenario_id"):
        return

    st["market_id"] = market_id
    st["mode"] = "solo"

    q = await question_factory.generate_question(
        market_id=market_id,
        topic=topic,
        difficulty=difficulty,
        xp=10,
    )

    scenario = await Scenario.find_one(Scenario.scenario_key == q.id)

    if not scenario:
        await bot.send_message(user_id, "متأسفانه نتونستم سؤال بسازم. دوباره تلاش کن.")
        return

    quiz_state[user_id] = {
        "pending_scenario_id": str(scenario.id),
        "mode": "solo",
        "market_id": market_id
    }

    await bot.send_message(
        user_id,
        f"🧠 سؤال جدید:\n\n{scenario.text}",
        reply_markup=UI.get_question_buttons(
            str(scenario.id),
            scenario.options,
            prefix="quiz"
        )
    )

async def handle_callback(callback):
    user_id = callback["from"]["id"]
    data = callback["data"]
    user_name = callback["from"]["first_name"]

    if data.startswith("deal_reject:"):
        deal_id = data.replace("deal_reject:", "")

        result = await DealService.reject_deal(
            deal_id=deal_id,
            user_id=user_id,
        )

        if not result["ok"]:
            await bot.send_message(
                user_id,
                f"❌ Deal رد نشد.\nReason: {result.get('reason')}"
            )
            return

        await bot.send_message(user_id, "❌ Deal rejected.")
        return

    if data.startswith("deal_accept:"):
        deal_id = data.replace("deal_accept:", "")

        result = await DealService.accept_and_resolve_deal(
            deal_id=deal_id,
            user_id=user_id,
        )

        if not result["ok"]:
            reason = result.get("reason")

            if reason == "insufficient_balance":
                await bot.send_message(
                    user_id,
                    f"❌ موجودی کافی نیست.\n\n"
                    f"Required: {result['required']}\n"
                    f"Balance: {result['balance']}"
                )
                return

            if reason == "trust_requirement_not_met":
                await bot.send_message(
                    user_id,
                    f"❌ سطح اعتماد کافی نیست.\n\n"
                    f"Required Trust: {result['required_trust']}\n"
                    f"Your Trust: {result['current_trust']}"
                )
                return

            await bot.send_message(
                user_id,
                f"❌ Deal قابل انجام نیست.\nReason: {reason}"
            )
            return

        outcome = result["outcome"]
        deal = result["deal"]

        await bot.send_message(
            user_id,
            f"📄 نتیجه Deal\n\n"
            f"Status: {deal.status}\n"
            f"Success: {outcome['success']}\n"
            f"Balance Effect: {outcome['profile_effects'].get('balance', 0)}\n\n"
            f"{outcome['message']}"
        )
        return

    if data.startswith("quiz_ans:"):
        _, rest = data.split("quiz_ans:", 1)
        scenario_id, opt_str = rest.split(":")
        selected = int(opt_str)

        st = quiz_state.get(user_id, {})

        if st.get("pending_scenario_id") != scenario_id:
            await bot.send_message(user_id, "این سؤال منقضی شده یا سؤال جدیدتری داری.")
            return

        scenario = await Scenario.get(scenario_id)

        if not scenario:
            await bot.send_message(user_id, "سؤال پیدا نشد.")
            quiz_state[user_id]["pending_scenario_id"] = None
            return

        result = judge.judge(scenario, selected)

        # ثبت Decision اگر مدلش را کامل داری
        # await Decision(...).insert()

        profile = await UserProfile.find_one(UserProfile.telegram_id == user_id)

        if profile and result.earned_xp:
            profile.score += result.earned_xp
            await profile.save()

        quiz_state[user_id]["pending_scenario_id"] = None

        msg = "✅ درست!" if result.is_correct else "❌ غلط!"
        exp = f"\n\nتوضیح: {result.explanation}" if result.explanation else ""

        await bot.send_message(
            user_id,
            f"{msg} (+{result.earned_xp} XP){exp}"
        )
        return

    # -------------------------
    # 2. انتخاب Market و Matchmaking
    # -------------------------
    if data.startswith("market_"):
        m_id = data.replace("market_", "")

        # market آخر کاربر را ذخیره کن تا سؤال‌های solo بعدی مرتبط‌تر باشند
        st = quiz_state.setdefault(
            user_id,
            {
                "pending_scenario_id": None,
                "mode": "solo",
                "market_id": m_id
            }
        )
        st["market_id"] = m_id

        # اگر کسی منتظر این market نیست
        if waiting_queue.get(m_id) is None:
            waiting_queue[m_id] = {
                "id": user_id,
                "name": user_name
            }

            await bot.send_message(
                user_id,
                f"🔍 Searching for opponent in {m_id}..."
            )
            return

        # اگر یک نفر منتظر است، match بساز
        opponent = waiting_queue.pop(m_id)

        # اگر کاربر با خودش match نشود
        if opponent["id"] == user_id:
            waiting_queue[m_id] = opponent
            await bot.send_message(user_id, "هنوز منتظر حریف هستی...")
            return

        game = await game_manager.create_game(
            opponent,
            {
                "id": user_id,
                "name": user_name
            },
            m_id
        )

        # سؤال‌های solo باز را پاک کن
        clear_user_quiz_pending(opponent["id"])
        clear_user_quiz_pending(user_id)

        # mode را برای خوانایی عوض کن، هرچند get_game خودش کافی است
        quiz_state[opponent["id"]]["mode"] = "in_game"
        quiz_state[user_id]["mode"] = "in_game"

        for p in game.players:
            await bot.send_message(
                p["id"],
                "🎮 Match Found!\n\nاستراتژی اولیه‌ات را انتخاب کن:",
                reply_markup=UI.get_strategy_buttons()
            )

        return

    # -------------------------
    # 3. پیدا کردن بازی کاربر
    # -------------------------
    game = game_manager.get_game(user_id)

    if not game:
        await bot.send_message(user_id, "بازی فعالی نداری.")
        return

    print(game.state)

    # -------------------------
    # 4. انتخاب Strategy اولیه
    # -------------------------
    if data.startswith("strategy_") and game.state == "waiting_strategy":
        strategy = data.replace("strategy_", "")
        await handle_strategy_logic(game, user_id, strategy)
        return

    # -------------------------
    # 5. تصمیم نهایی بعد از مذاکره
    # -------------------------
    if data.startswith("choice_") and game.state == "decision":
        if user_id in game.choices:
            await bot.send_message(user_id, "قبلاً انتخابت را ثبت کردی.")
            return

        game.choices[user_id] = data.replace("choice_", "")

        await bot.send_message(user_id, "✅ انتخاب نهایی ثبت شد. منتظر حریف...")

        if len(game.choices) == 2:
            payoffs = market_factory.get(game.market_id).payoff
            results = GameEngine.calculate_game_results(game, payoffs)
            await finalize_game(game, results)

        return

    # -------------------------
    # 6. انتخاب در Chicken Game
    # -------------------------
    if data.startswith("war_") and game.state == "war_decision":
        if user_id in game.war_choices:
            await bot.send_message(user_id, "قبلاً انتخابت را ثبت کردی.")
            return

        game.war_choices[user_id] = data.replace("war_", "")

        await bot.send_message(user_id, "✅ انتخاب جنگی ثبت شد. منتظر حریف...")

        if len(game.war_choices) == 2:
            results = GameEngine.calculate_chicken_results(game)
            await finalize_game(game, results)

        return

    await bot.send_message(user_id, "این دکمه الان معتبر نیست.")

async def handle_text(msg):
    user_id = msg["from"]["id"]
    text = msg.get("text", "")

    # اگر در فاز مذاکره است، پیام را برای حریف بفرست
    game = game_manager.get_game(user_id)

    if game and game.state == "waiting_negotiation":
        opponent_id = [p["id"] for p in game.players if p["id"] != user_id][0]

        await bot.send_message(
            opponent_id,
            f"💬 {msg['from']['first_name']}: {text}"
        )
        return

    if text == "/start":
        await bot.send_message(
            user_id,
            "سلام! برای شروع /play را بزن."
        )
        return

    if text == "/play":
        profile = await UserProfile.find_one(UserProfile.telegram_id == user_id)

        # اگر پروفایل نداری، بسته به مدل خودت اینجا بساز
        # if not profile:
        #     profile = UserProfile(telegram_id=user_id, score=0)
        #     await profile.insert()

        active_quiz_users.add(user_id)

        quiz_state.setdefault(
            user_id,
            {
                "pending_scenario_id": None,
                "mode": "solo",
                "market_id": "global"
            }
        )

        await bot.send_message(
            user_id,
            "Select Market:",
            keyboard=UI.get_market_selection(
                unlocked_markets=[],
                include_generate=False,
                market_unlocks={}
            )
        )
        return

    if text == "/profile":
        await bot.send_message(
            user_id,
            "Your Profile:",
            reply_markup=UI.get_profile_menu()
        )
        return

    await bot.send_message(user_id, "دستور نامعتبر است. از /play استفاده کن.")

async def quiz_scheduler_loop():
    while True:
        try:
            for user_id in list(active_quiz_users):

                # اگر کاربر داخل game است، سوال solo نفرست
                game = game_manager.get_game(user_id)
                if game:
                    continue

                st = quiz_state.get(user_id, {})

                # اگر هنوز سؤال pending دارد، سؤال جدید نفرست
                if st.get("pending_scenario_id"):
                    continue

                market_id = st.get("market_id", "global")
                topic = "general"
                difficulty = "easy"

                await send_quiz_question(
                    user_id=user_id,
                    market_id=market_id,
                    topic=topic,
                    difficulty=difficulty
                )

        except Exception as e:
            logging.exception("quiz scheduler error: %s", e)

        await asyncio.sleep(1)


# -------------------------
# Main Entry
# -------------------------

async def main():
    await connect_to_database()
    await market_factory.load_from_db()

    await bot.start()  # ✅ اضافه شود: قبل از اولین get_updates
    asyncio.create_task(quiz_scheduler_loop())  # ✅
    print("🤖 Bot is running...")

    offset = None
    try:
        while True:
            updates = await bot.get_updates(offset)
            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                if "message" in update:
                    await handle_text(update["message"])
                elif "callback_query" in update:
                    await handle_callback(update["callback_query"])
            await asyncio.sleep(0.5)
    finally:
        # ✅ برای خروج تمیز (Ctrl+C یا خطا)
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
