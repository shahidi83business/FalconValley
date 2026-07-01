#main.py
import asyncio
import os
import logging
from dotenv import load_dotenv

# Helpers & Models
from app.data.db_helper import connect_to_database
from app.bot.telegramapi import TelegramBotAPI
from app.data.models import UserProfile, Scenario, Decision
from app.game.marketfactory import MarketFactory
from app.game.manager import game_manager  # مدیریت مرکزی بازی‌ها
from app.game.engine import GameEngine      # موتور محاسبات نتایج
from app.bot.ui import UI                  # کلاس رابط کاربری که ساختیم
from app.services.questionfactory import QuestionFactory
from app.services.judge_service import JudgeService
from app.game.deal_service import DealService
from app.bot.callback_manager import CallbackManager

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
    if callback_manager is None:
        logging.error("callback_manager is not initialized")
        return

    await callback_manager.dispatch(callback)

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
    global callback_manager

    await connect_to_database()
    await market_factory.load_from_db()

    deal_service = DealService()

    callback_manager = CallbackManager(
        bot=bot,
        ui=UI,
        judge=judge,
        deal_service=deal_service,
        market_factory=market_factory,
        game_manager=game_manager,
        quiz_state=quiz_state,
        waiting_queue=waiting_queue,
        clear_user_quiz_pending=clear_user_quiz_pending,
        handle_strategy_logic=_handle_strategy_logic,
        finalize_game=finalize_game,
    )

    await bot.start()  # ✅ اضافه شود: قبل از اولین get_updates
    asyncio.create_task(quiz_scheduler_loop())  # ✅
    print("🤖 Bot is running...")

    offset = 0

    while True:
        updates = await bot.get_updates(offset=offset, timeout=30)

        results = updates.get("result", [])

        if results:
            for update in results:
                offset = update["update_id"] + 1

                if "message" in update:
                    await handle_text(update["message"])

                elif "callback_query" in update:
                    await handle_callback(update["callback_query"])

        await asyncio.sleep(0.2)


async def _handle_strategy_logic(game, user_id, strategy):
    """Placeholder for strategy logic — wires into game FSM."""
    game.strategy[user_id] = strategy

    if len(game.strategy) == 2:
        p1_id = game.players[0]["id"]
        p2_id = game.players[1]["id"]
        s1 = game.strategy.get(p1_id)
        s2 = game.strategy.get(p2_id)

        if s1 == "negotiation" and s2 == "negotiation":
            await game.start_negotiation()
            for p in game.players:
                await bot.send_message(
                    p["id"],
                    "🤝 Both chose negotiation. Chat freely, then decide:",
                    reply_markup=UI.get_negotiation_buttons()
                )
            asyncio.create_task(negotiation_timeout(game))

        elif s1 == "war" and s2 == "war":
            await game.start_chicken()
            for p in game.players:
                await bot.send_message(
                    p["id"],
                    "⚔️ Both chose war! Chicken game begins:",
                    reply_markup=UI.get_chicken_buttons()
                )

        else:
            results = GameEngine.calculate_war_advantage_results(game)
            await finalize_game(game, results)


if __name__ == "__main__":
    asyncio.run(main())
