# ui.py

class UI:
    @staticmethod
    def get_main_menu():
        return {
            "inline_keyboard": [
                [{"text": "🎮 Play Now", "callback_data": "menu_play"}],
                [{"text": "👤 My Profile", "callback_data": "menu_profile"}],
            ]
        }

    @staticmethod
    def get_market_selection(unlocked_markets=None, include_generate=False, market_unlocks=None):
        """
        ساخت منوی انتخاب مارکت

        unlocked_markets: لیست market id های بازشده کاربر
        include_generate: آیا دکمه ساخت مارکت AI نمایش داده شود؟
        market_unlocks: دیکشنری MARKET_UNLOCKS برای گرفتن title
        """
        unlocked_markets = unlocked_markets or []
        market_unlocks = market_unlocks or {}

        buttons = [
            [{"text": "⚡ Energy Market", "callback_data": "market_energy"}],
            [{"text": "💻 Tech Market", "callback_data": "market_tech"}],
            [{"text": "🌾 Agro Market", "callback_data": "market_agro"}],
        ]

        for market_id in unlocked_markets:
            title = market_unlocks.get(market_id, {}).get("title", market_id)
            buttons.append([
                {"text": title, "callback_data": f"market_{market_id}"}
            ])

        if include_generate:
            buttons.append([
                {"text": "🧠 Generate New Market (AI)", "callback_data": "market_gen_start"}
            ])

        return {"inline_keyboard": buttons}

    @staticmethod
    def get_market_generation_base_menu():
        return {
            "inline_keyboard": [
                [{"text": "⚡ Based on Energy", "callback_data": "market_gen_base_energy"}],
                [{"text": "💻 Based on Tech", "callback_data": "market_gen_base_tech"}],
                [{"text": "🌾 Based on Agro", "callback_data": "market_gen_base_agro"}],
            ]
        }

    @staticmethod
    def get_strategy_buttons():
        return {
            "inline_keyboard": [
                [
                    {"text": "🤝 Negotiation", "callback_data": "strategy_negotiation"},
                    {"text": "⚔️ War", "callback_data": "strategy_war"},
                ]
            ]
        }

    @staticmethod
    def get_negotiation_buttons():
        return {
            "inline_keyboard": [
                [
                    {"text": "🤝 Cooperate", "callback_data": "choice_cooperate"},
                    {"text": "😈 Defect", "callback_data": "choice_defect"},
                ]
            ]
        }

    @staticmethod
    def get_chicken_buttons():
        return {
            "inline_keyboard": [
                [
                    {"text": "🕊 Yield", "callback_data": "war_yield"},
                    {"text": "🚗 Straight", "callback_data": "war_straight"},
                ]
            ]
        }

    @staticmethod
    def get_profile_menu():
        return {
            "inline_keyboard": [
                [
                    {"text": "📝 Edit First Name", "callback_data": "edit_first_name"},
                    {"text": "📝 Edit Last Name", "callback_data": "edit_last_name"},
                ],
                [
                    {"text": "✍️ Edit Bio", "callback_data": "edit_bio"},
                ]
            ]
        }

    @staticmethod
    def get_question_buttons(scenario_id: str, options: list[str], prefix: str = "quiz"):
        keyboard = []
        for i, opt in enumerate(options):
            keyboard.append([{
                "text": opt,
                "callback_data": f"{prefix}_ans:{scenario_id}:{i}"
            }])
        return {"inline_keyboard": keyboard}
