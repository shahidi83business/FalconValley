# callback_manager.py

import logging
from dataclasses import dataclass
from typing import Callable, Awaitable, Dict, Optional, List, Any

from app.data.models import UserProfile, Scenario
from app.game.engine import GameEngine


@dataclass
class CallbackContext:
    callback: dict
    user_id: int
    user_name: str
    data: str
    action: str
    args: List[str]


CallbackHandler = Callable[[CallbackContext], Awaitable[None]]


class CallbackRouter:
    def __init__(self, bot):
        self.bot = bot
        self.handlers: Dict[str, CallbackHandler] = {}

    def register(self, action: str, handler: CallbackHandler):
        self.handlers[action] = handler

    def parse(self, callback: dict) -> Optional[CallbackContext]:
        data = callback.get("data", "")
        user = callback.get("from", {})

        user_id = user.get("id")
        user_name = user.get("first_name", "User")

        if not data or user_id is None:
            return None

        if ":" in data:
            parts = data.split(":")
            action = parts[0]
            args = parts[1:]

        elif "_" in data:
            prefix, value = data.split("_", 1)
            action = prefix
            args = [value]

        else:
            action = data
            args = []

        return CallbackContext(
            callback=callback,
            user_id=user_id,
            user_name=user_name,
            data=data,
            action=action,
            args=args,
        )

    async def dispatch(self, callback: dict):
        ctx = self.parse(callback)

        if not ctx:
            return

        handler = self.handlers.get(ctx.action)

        if not handler:
            await self.bot.send_message(ctx.user_id, "این دکمه شناخته نشد.")
            return

        try:
            await handler(ctx)

        except Exception as e:
            logging.exception("callback handler error: %s", e)
            await self.bot.send_message(
                ctx.user_id,
                "خطایی در پردازش دکمه رخ داد. لطفاً دوباره تلاش کن."
            )


class CallbackManager:
    def __init__(
        self,
        *,
        bot,
        ui,
        judge,
        deal_service,
        market_factory,
        game_manager,
        quiz_state: dict,
        waiting_queue: dict,
        clear_user_quiz_pending: Callable[[int], None],
        handle_strategy_logic: Callable[[Any, int, str], Awaitable[None]],
        finalize_game: Callable[[Any, dict], Awaitable[None]],
    ):
        self.bot = bot
        self.UI = ui
        self.judge = judge
        self.DealService = deal_service
        self.market_factory = market_factory
        self.game_manager = game_manager

        self.quiz_state = quiz_state
        self.waiting_queue = waiting_queue

        self.clear_user_quiz_pending = clear_user_quiz_pending
        self.handle_strategy_logic = handle_strategy_logic
        self.finalize_game = finalize_game

        self.router = CallbackRouter(bot)
        self._register_handlers()

    def _register_handlers(self):
        self.router.register("deal_reject", self.handle_deal_reject)
        self.router.register("deal_accept", self.handle_deal_accept)

        self.router.register("quiz_ans", self.handle_quiz_answer)

        self.router.register("market", self.handle_market)
        self.router.register("strategy", self.handle_strategy)
        self.router.register("choice", self.handle_choice)
        self.router.register("war", self.handle_war)

    async def dispatch(self, callback: dict):
        await self.router.dispatch(callback)

    # -------------------------
    # Helpers
    # -------------------------

    async def require_active_game(self, user_id: int):
        game = self.game_manager.get_game(user_id)

        if not game:
            await self.bot.send_message(user_id, "بازی فعالی نداری.")
            return None

        return game

    def ensure_quiz_state(self, user_id: int, market_id: str = "global"):
        return self.quiz_state.setdefault(
            user_id,
            {
                "pending_scenario_id": None,
                "mode": "solo",
                "market_id": market_id,
            }
        )

    # -------------------------
    # Deal Callbacks
    # -------------------------

    async def handle_deal_reject(self, ctx: CallbackContext):
        if not ctx.args:
            await self.bot.send_message(ctx.user_id, "شناسه Deal نامعتبر است.")
            return

        deal_id = ctx.args[0]

        result = await self.DealService.reject_deal(
            deal_id=deal_id,
            user_id=ctx.user_id,
        )

        if not result["ok"]:
            await self.bot.send_message(
                ctx.user_id,
                f"❌ Deal رد نشد.\nReason: {result.get('reason')}"
            )
            return

        await self.bot.send_message(ctx.user_id, "❌ Deal rejected.")

    async def handle_deal_accept(self, ctx: CallbackContext):
        if not ctx.args:
            await self.bot.send_message(ctx.user_id, "شناسه Deal نامعتبر است.")
            return

        deal_id = ctx.args[0]

        result = await self.DealService.accept_and_resolve_deal(
            deal_id=deal_id,
            user_id=ctx.user_id,
        )

        if not result["ok"]:
            reason = result.get("reason")

            if reason == "insufficient_balance":
                await self.bot.send_message(
                    ctx.user_id,
                    f"❌ موجودی کافی نیست.\n\n"
                    f"Required: {result['required']}\n"
                    f"Balance: {result['balance']}"
                )
                return

            if reason == "trust_requirement_not_met":
                await self.bot.send_message(
                    ctx.user_id,
                    f"❌ سطح اعتماد کافی نیست.\n\n"
                    f"Required Trust: {result['required_trust']}\n"
                    f"Your Trust: {result['current_trust']}"
                )
                return

            await self.bot.send_message(
                ctx.user_id,
                f"❌ Deal قابل انجام نیست.\nReason: {reason}"
            )
            return

        outcome = result["outcome"]
        deal = result["deal"]

        await self.bot.send_message(
            ctx.user_id,
            f"📄 نتیجه Deal\n\n"
            f"Status: {deal.status}\n"
            f"Success: {outcome['success']}\n"
            f"Balance Effect: {outcome['profile_effects'].get('balance', 0)}\n\n"
            f"{outcome['message']}"
        )

    # -------------------------
    # Quiz Callback
    # -------------------------

    async def handle_quiz_answer(self, ctx: CallbackContext):
        if len(ctx.args) < 2:
            await self.bot.send_message(ctx.user_id, "پاسخ سؤال نامعتبر است.")
            return

        scenario_id = ctx.args[0]

        try:
            selected = int(ctx.args[1])
        except ValueError:
            await self.bot.send_message(ctx.user_id, "گزینه انتخاب‌شده نامعتبر است.")
            return

        st = self.quiz_state.get(ctx.user_id, {})

        if st.get("pending_scenario_id") != scenario_id:
            await self.bot.send_message(
                ctx.user_id,
                "این سؤال منقضی شده یا سؤال جدیدتری داری."
            )
            return

        scenario = await Scenario.get(scenario_id)

        if not scenario:
            await self.bot.send_message(ctx.user_id, "سؤال پیدا نشد.")

            st = self.ensure_quiz_state(ctx.user_id)
            st["pending_scenario_id"] = None

            return

        result = self.judge.judge(scenario, selected)

        profile = await UserProfile.find_one(UserProfile.telegram_id == ctx.user_id)

        if profile and result.earned_xp:
            profile.score += result.earned_xp
            await profile.save()

        st = self.ensure_quiz_state(ctx.user_id)
        st["pending_scenario_id"] = None

        msg = "✅ درست!" if result.is_correct else "❌ غلط!"
        exp = f"\n\nتوضیح: {result.explanation}" if result.explanation else ""

        await self.bot.send_message(
            ctx.user_id,
            f"{msg} (+{result.earned_xp} XP){exp}"
        )

    # -------------------------
    # Market Callback
    # -------------------------

    async def handle_market(self, ctx: CallbackContext):
        if not ctx.args:
            await self.bot.send_message(ctx.user_id, "Market نامعتبر است.")
            return

        m_id = ctx.args[0]

        st = self.ensure_quiz_state(ctx.user_id, market_id=m_id)
        st["market_id"] = m_id

        if self.waiting_queue.get(m_id) is None:
            self.waiting_queue[m_id] = {
                "id": ctx.user_id,
                "name": ctx.user_name,
            }

            await self.bot.send_message(
                ctx.user_id,
                f"🔍 Searching for opponent in {m_id}..."
            )
            return

        opponent = self.waiting_queue.pop(m_id)

        if opponent["id"] == ctx.user_id:
            self.waiting_queue[m_id] = opponent
            await self.bot.send_message(ctx.user_id, "هنوز منتظر حریف هستی...")
            return

        game = await self.game_manager.create_game(
            opponent,
            {
                "id": ctx.user_id,
                "name": ctx.user_name,
            },
            m_id
        )

        self.clear_user_quiz_pending(opponent["id"])
        self.clear_user_quiz_pending(ctx.user_id)

        self.quiz_state[opponent["id"]]["mode"] = "in_game"
        self.quiz_state[ctx.user_id]["mode"] = "in_game"

        for p in game.players:
            await self.bot.send_message(
                p["id"],
                "🎮 Match Found!\n\nاستراتژی اولیه‌ات را انتخاب کن:",
                reply_markup=self.UI.get_strategy_buttons()
            )

    # -------------------------
    # Strategy Callback
    # -------------------------

    async def handle_strategy(self, ctx: CallbackContext):
        game = await self.require_active_game(ctx.user_id)

        if not game:
            return

        if game.state != "waiting_strategy":
            await self.bot.send_message(ctx.user_id, "الان زمان انتخاب استراتژی نیست.")
            return

        if not ctx.args:
            await self.bot.send_message(ctx.user_id, "استراتژی نامعتبر است.")
            return

        strategy = ctx.args[0]

        allowed = {"negotiation", "war"}

        if strategy not in allowed:
            await self.bot.send_message(ctx.user_id, "استراتژی انتخاب‌شده معتبر نیست.")
            return

        await self.handle_strategy_logic(game, ctx.user_id, strategy)

    # -------------------------
    # Final Choice Callback
    # -------------------------

    async def handle_choice(self, ctx: CallbackContext):
        game = await self.require_active_game(ctx.user_id)

        if not game:
            return

        if game.state != "decision":
            await self.bot.send_message(ctx.user_id, "الان زمان تصمیم نهایی نیست.")
            return

        if not ctx.args:
            await self.bot.send_message(ctx.user_id, "تصمیم نامعتبر است.")
            return

        if ctx.user_id in game.choices:
            await self.bot.send_message(ctx.user_id, "قبلاً انتخابت را ثبت کردی.")
            return

        choice = ctx.args[0]
        game.choices[ctx.user_id] = choice

        await self.bot.send_message(
            ctx.user_id,
            "✅ انتخاب نهایی ثبت شد. منتظر حریف..."
        )

        if len(game.choices) == 2:
            market = self.market_factory.get(game.market_id)

            if not market:
                for p in game.players:
                    await self.bot.send_message(
                        p["id"],
                        "Market این بازی پیدا نشد. بازی قابل محاسبه نیست."
                    )
                return

            payoffs = market.payoff
            results = GameEngine.calculate_game_results(game, payoffs)

            await self.finalize_game(game, results)

    # -------------------------
    # Chicken Game Callback
    # -------------------------

    async def handle_war(self, ctx: CallbackContext):
        game = await self.require_active_game(ctx.user_id)

        if not game:
            return

        if game.state != "war_decision":
            await self.bot.send_message(ctx.user_id, "الان زمان تصمیم جنگی نیست.")
            return

        if not ctx.args:
            await self.bot.send_message(ctx.user_id, "انتخاب جنگی نامعتبر است.")
            return

        if ctx.user_id in game.war_choices:
            await self.bot.send_message(ctx.user_id, "قبلاً انتخابت را ثبت کردی.")
            return

        war_choice = ctx.args[0]
        game.war_choices[ctx.user_id] = war_choice

        await self.bot.send_message(
            ctx.user_id,
            "✅ انتخاب جنگی ثبت شد. منتظر حریف..."
        )

        if len(game.war_choices) == 2:
            results = GameEngine.calculate_chicken_results(game)
            await self.finalize_game(game, results)
