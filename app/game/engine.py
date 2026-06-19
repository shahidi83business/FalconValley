class GameEngine:
    # ============================================================
    # Legacy score-only methods
    # These are kept for backward compatibility.
    # ============================================================

    @staticmethod
    def calculate_game_results(game, market_payoff):
        """محاسبه نتایج مذاکره قدیمی - فقط score"""
        outcome = GameEngine.calculate_negotiation_outcome(game, market_payoff)
        return outcome["scores"]

    @staticmethod
    def calculate_chicken_results(game):
        """محاسبه نتایج جنگ قدیمی - فقط score"""
        outcome = GameEngine.calculate_chicken_outcome(game)
        return outcome["scores"]

    @staticmethod
    def calculate_war_advantage_results(game):
        """محاسبه نتایج وقتی یکی جنگ و دیگری مذاکره را انتخاب کرده است - فقط score"""
        outcome = GameEngine.calculate_war_advantage_outcome(game)
        return outcome["scores"]

    # ============================================================
    # New outcome-based methods
    # ============================================================

    @staticmethod
    def empty_effects(game):
        effects = {p["id"]: {} for p in game.players}
        effects["economy"] = {}
        return effects

    @staticmethod
    def add_effect(target, field_name, delta):
        target[field_name] = target.get(field_name, 0) + delta

    @staticmethod
    def get_market_modifier(game, key, default=1):
        """
        Optional helper.
        If later you store market modifiers in session.game_data,
        this method can read them safely.
        """
        game_data = getattr(game.session, "game_data", None) or {}
        market_modifiers = game_data.get("market_modifiers", {})
        return market_modifiers.get(key, default)

    @staticmethod
    def calculate_negotiation_outcome(game, market_payoff=None):
        """
        محاسبه خروجی مذاکره به شکل outcome کامل.

        choices expected:
        - cooperate
        - defect

        output:
        {
            "mode": "NEGOTIATION",
            "scores": {...},
            "effects": {
                user_id: {...},
                "economy": {...}
            },
            "result_text": "...",
            "summary": "..."
        }
        """

        if market_payoff is None:
            market_payoff = {
                "coop": 2,
                "betray": 3,
                "both": -1,
            }

        p1, p2 = game.players
        p1_id = p1["id"]
        p2_id = p2["id"]

        c1 = game.choices.get(p1_id)
        c2 = game.choices.get(p2_id)

        scores = {
            p1_id: 0,
            p2_id: 0,
        }

        effects = GameEngine.empty_effects(game)

        if c1 == "cooperate" and c2 == "cooperate":
            scores[p1_id] = market_payoff["coop"]
            scores[p2_id] = market_payoff["coop"]

            # فردی
            GameEngine.add_effect(effects[p1_id], "public_standing", 2)
            GameEngine.add_effect(effects[p2_id], "public_standing", 2)
            GameEngine.add_effect(effects[p1_id], "peer_standing", 2)
            GameEngine.add_effect(effects[p2_id], "peer_standing", 2)
            GameEngine.add_effect(effects[p1_id], "cooperation_bias", 0.02)
            GameEngine.add_effect(effects[p2_id], "cooperation_bias", 0.02)

            # سیستمی
            GameEngine.add_effect(effects["economy"], "trust", 5)
            GameEngine.add_effect(effects["economy"], "resilience", 2)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", -2)
            GameEngine.add_effect(effects["economy"], "volatility", -1)

            summary = "Both players cooperated. Trust and systemic resilience improved."

        elif c1 == "cooperate" and c2 == "defect":
            scores[p1_id] = 0
            scores[p2_id] = market_payoff["betray"]

            # p1 قربانی همکاری
            GameEngine.add_effect(effects[p1_id], "public_standing", 1)
            GameEngine.add_effect(effects[p1_id], "peer_standing", 1)
            GameEngine.add_effect(effects[p1_id], "risk_appetite", -0.01)

            # p2 سود کوتاه‌مدت با هزینه اجتماعی
            GameEngine.add_effect(effects[p2_id], "public_standing", -4)
            GameEngine.add_effect(effects[p2_id], "peer_standing", -5)
            GameEngine.add_effect(effects[p2_id], "leverage", 2)
            GameEngine.add_effect(effects[p2_id], "cooperation_bias", -0.03)

            # اقتصاد آسیب می‌بیند
            GameEngine.add_effect(effects["economy"], "trust", -6)
            GameEngine.add_effect(effects["economy"], "resilience", -2)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", 4)
            GameEngine.add_effect(effects["economy"], "volatility", 2)

            summary = f"{p2['name']} exploited {p1['name']}'s cooperation. Short-term gain, long-term distrust."

        elif c1 == "defect" and c2 == "cooperate":
            scores[p1_id] = market_payoff["betray"]
            scores[p2_id] = 0

            # p1 سود کوتاه‌مدت با هزینه اجتماعی
            GameEngine.add_effect(effects[p1_id], "public_standing", -4)
            GameEngine.add_effect(effects[p1_id], "peer_standing", -5)
            GameEngine.add_effect(effects[p1_id], "leverage", 2)
            GameEngine.add_effect(effects[p1_id], "cooperation_bias", -0.03)

            # p2 قربانی همکاری
            GameEngine.add_effect(effects[p2_id], "public_standing", 1)
            GameEngine.add_effect(effects[p2_id], "peer_standing", 1)
            GameEngine.add_effect(effects[p2_id], "risk_appetite", -0.01)

            # اقتصاد آسیب می‌بیند
            GameEngine.add_effect(effects["economy"], "trust", -6)
            GameEngine.add_effect(effects["economy"], "resilience", -2)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", 4)
            GameEngine.add_effect(effects["economy"], "volatility", 2)

            summary = f"{p1['name']} exploited {p2['name']}'s cooperation. Short-term gain, long-term distrust."

        elif c1 == "defect" and c2 == "defect":
            scores[p1_id] = market_payoff["both"]
            scores[p2_id] = market_payoff["both"]

            # هر دو بدنام‌تر می‌شوند
            GameEngine.add_effect(effects[p1_id], "public_standing", -5)
            GameEngine.add_effect(effects[p2_id], "public_standing", -5)
            GameEngine.add_effect(effects[p1_id], "peer_standing", -4)
            GameEngine.add_effect(effects[p2_id], "peer_standing", -4)
            GameEngine.add_effect(effects[p1_id], "cooperation_bias", -0.04)
            GameEngine.add_effect(effects[p2_id], "cooperation_bias", -0.04)
            GameEngine.add_effect(effects[p1_id], "risk_appetite", 0.02)
            GameEngine.add_effect(effects[p2_id], "risk_appetite", 0.02)

            # آسیب سیستمی جدی‌تر
            GameEngine.add_effect(effects["economy"], "trust", -10)
            GameEngine.add_effect(effects["economy"], "resilience", -5)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", 8)
            GameEngine.add_effect(effects["economy"], "volatility", 5)

            summary = "Both players defected. Everyone lost trust, and systemic pressure increased."

        else:
            summary = "Negotiation ended with invalid or missing choices."

        outcome = {
            "mode": "NEGOTIATION",
            "scores": scores,
            "effects": effects,
            "summary": summary,
        }

        outcome["result_text"] = GameEngine.generate_rich_result_text(
            game=game,
            outcome=outcome,
            mode="NEGOTIATION",
        )

        return outcome

    @staticmethod
    def calculate_chicken_outcome(game):
        """
        محاسبه خروجی بازی Chicken / War.

        war_choices expected:
        - yield
        - straight
        """

        p1, p2 = game.players
        p1_id = p1["id"]
        p2_id = p2["id"]

        c1 = game.war_choices.get(p1_id)
        c2 = game.war_choices.get(p2_id)

        effects = GameEngine.empty_effects(game)

        matrix = {
            ("yield", "yield"): (0, 0),
            ("yield", "straight"): (-1, 2),
            ("straight", "yield"): (2, -1),
            ("straight", "straight"): (-5, -5),
        }

        r1, r2 = matrix.get((c1, c2), (0, 0))

        # توجه:
        # در کد قدیمی تو penalty اضافه می‌شد.
        # اگر penalty عدد منفی است، اضافه کردن درست است.
        # اگر penalty عدد مثبت به معنی جریمه است، باید کم شود.
        r1 += game.war_penalty.get(p1_id, 0)
        r2 += game.war_penalty.get(p2_id, 0)

        scores = {
            p1_id: r1,
            p2_id: r2,
        }

        if c1 == "yield" and c2 == "yield":
            GameEngine.add_effect(effects[p1_id], "public_standing", 1)
            GameEngine.add_effect(effects[p2_id], "public_standing", 1)
            GameEngine.add_effect(effects[p1_id], "peer_standing", 1)
            GameEngine.add_effect(effects[p2_id], "peer_standing", 1)

            GameEngine.add_effect(effects["economy"], "trust", 2)
            GameEngine.add_effect(effects["economy"], "volatility", -2)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", -1)

            summary = "Both players backed down. The system stabilized slightly."

        elif c1 == "yield" and c2 == "straight":
            GameEngine.add_effect(effects[p2_id], "leverage", 3)
            GameEngine.add_effect(effects[p2_id], "public_standing", -2)
            GameEngine.add_effect(effects[p2_id], "risk_appetite", 0.02)

            GameEngine.add_effect(effects[p1_id], "peer_standing", -1)
            GameEngine.add_effect(effects[p1_id], "risk_appetite", -0.01)

            GameEngine.add_effect(effects["economy"], "regulatory_heat", 3)
            GameEngine.add_effect(effects["economy"], "volatility", 3)
            GameEngine.add_effect(effects["economy"], "trust", -1)

            summary = f"{p2['name']} escalated while {p1['name']} yielded."

        elif c1 == "straight" and c2 == "yield":
            GameEngine.add_effect(effects[p1_id], "leverage", 3)
            GameEngine.add_effect(effects[p1_id], "public_standing", -2)
            GameEngine.add_effect(effects[p1_id], "risk_appetite", 0.02)

            GameEngine.add_effect(effects[p2_id], "peer_standing", -1)
            GameEngine.add_effect(effects[p2_id], "risk_appetite", -0.01)

            GameEngine.add_effect(effects["economy"], "regulatory_heat", 3)
            GameEngine.add_effect(effects["economy"], "volatility", 3)
            GameEngine.add_effect(effects["economy"], "trust", -1)

            summary = f"{p1['name']} escalated while {p2['name']} yielded."

        elif c1 == "straight" and c2 == "straight":
            GameEngine.add_effect(effects[p1_id], "public_standing", -6)
            GameEngine.add_effect(effects[p2_id], "public_standing", -6)
            GameEngine.add_effect(effects[p1_id], "peer_standing", -4)
            GameEngine.add_effect(effects[p2_id], "peer_standing", -4)
            GameEngine.add_effect(effects[p1_id], "risk_appetite", 0.03)
            GameEngine.add_effect(effects[p2_id], "risk_appetite", 0.03)

            GameEngine.add_effect(effects["economy"], "trust", -5)
            GameEngine.add_effect(effects["economy"], "resilience", -6)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", 7)
            GameEngine.add_effect(effects["economy"], "volatility", 8)

            summary = "Both players escalated. The conflict damaged the system."

        else:
            summary = "Chicken game ended with invalid or missing choices."

        outcome = {
            "mode": "CHICKEN",
            "scores": scores,
            "effects": effects,
            "summary": summary,
        }

        outcome["result_text"] = GameEngine.generate_rich_result_text(
            game=game,
            outcome=outcome,
            mode="CHICKEN",
        )

        return outcome

    @staticmethod
    def calculate_war_advantage_outcome(game):
        """
        محاسبه وقتی یکی strategy=war و دیگری strategy=negotiation انتخاب کرده.
        """

        p1, p2 = game.players
        p1_id = p1["id"]
        p2_id = p2["id"]

        s1 = game.strategy.get(p1_id)
        s2 = game.strategy.get(p2_id)

        scores = {
            p1_id: 0,
            p2_id: 0,
        }

        effects = GameEngine.empty_effects(game)

        if s1 == "war" and s2 == "negotiation":
            scores[p1_id] = 3
            scores[p2_id] = -2

            GameEngine.add_effect(effects[p1_id], "leverage", 3)
            GameEngine.add_effect(effects[p1_id], "public_standing", -3)
            GameEngine.add_effect(effects[p1_id], "risk_appetite", 0.02)

            GameEngine.add_effect(effects[p2_id], "peer_standing", -1)
            GameEngine.add_effect(effects[p2_id], "risk_appetite", -0.01)

            GameEngine.add_effect(effects["economy"], "trust", -3)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", 5)
            GameEngine.add_effect(effects["economy"], "volatility", 4)

            summary = f"{p1['name']} chose war while {p2['name']} chose negotiation."

        elif s1 == "negotiation" and s2 == "war":
            scores[p1_id] = -2
            scores[p2_id] = 3

            GameEngine.add_effect(effects[p2_id], "leverage", 3)
            GameEngine.add_effect(effects[p2_id], "public_standing", -3)
            GameEngine.add_effect(effects[p2_id], "risk_appetite", 0.02)

            GameEngine.add_effect(effects[p1_id], "peer_standing", -1)
            GameEngine.add_effect(effects[p1_id], "risk_appetite", -0.01)

            GameEngine.add_effect(effects["economy"], "trust", -3)
            GameEngine.add_effect(effects["economy"], "regulatory_heat", 5)
            GameEngine.add_effect(effects["economy"], "volatility", 4)

            summary = f"{p2['name']} chose war while {p1['name']} chose negotiation."

        elif s1 == "war" and s2 == "war":
            # این حالت معمولاً باید برود به Chicken،
            # اما برای safety outcome خنثی/هشدار می‌دهیم.
            summary = "Both players chose war. This should normally trigger Chicken mode."

        elif s1 == "negotiation" and s2 == "negotiation":
            # این حالت معمولاً باید برود به Negotiation.
            summary = "Both players chose negotiation. This should normally trigger Negotiation mode."

        else:
            summary = "Strategy outcome ended with invalid or missing strategies."

        outcome = {
            "mode": "ADVANTAGE",
            "scores": scores,
            "effects": effects,
            "summary": summary,
        }

        outcome["result_text"] = GameEngine.generate_rich_result_text(
            game=game,
            outcome=outcome,
            mode="ADVANTAGE",
        )

        return outcome

    # ============================================================
    # Text generation
    # ============================================================

    @staticmethod
    def generate_result_text(game, scores, mode="NORMAL"):
        """متد قدیمی تولید متن خروجی برای سازگاری قبلی"""
        p1, p2 = game.players

        if mode == "CHICKEN":
            c1 = game.war_choices.get(p1["id"], "-")
            c2 = game.war_choices.get(p2["id"], "-")
            mode_label = "CHICKEN (War)"
        elif mode == "ADVANTAGE":
            c1 = game.strategy.get(p1["id"], "-")
            c2 = game.strategy.get(p2["id"], "-")
            mode_label = "WAR (Advantage)"
        else:
            c1 = game.choices.get(p1["id"], "-")
            c2 = game.choices.get(p2["id"], "-")
            mode_label = "Standard Negotiation"

        return (
            f"📌 Market: {str(game.market_id).upper()}\n"
            f"🕹 Mode: {mode_label}\n\n"
            f"👤 {p1['name']}: {c1}\n"
            f"👤 {p2['name']}: {c2}\n\n"
            f"📊 Final Scores:\n"
            f"├ {p1['name']}: {scores.get(p1['id'], 0)}\n"
            f"└ {p2['name']}: {scores.get(p2['id'], 0)}"
        )

    @staticmethod
    def generate_rich_result_text(game, outcome, mode="NEGOTIATION"):
        """
        متن جدید که علاوه بر score، اثرات فردی و سیستمی را هم نشان می‌دهد.
        """

        p1, p2 = game.players
        scores = outcome.get("scores", {})
        effects = outcome.get("effects", {})
        economy_effects = effects.get("economy", {})

        if mode == "CHICKEN":
            c1 = game.war_choices.get(p1["id"], "-")
            c2 = game.war_choices.get(p2["id"], "-")
            mode_label = "CHICKEN (War)"
        elif mode == "ADVANTAGE":
            c1 = game.strategy.get(p1["id"], "-")
            c2 = game.strategy.get(p2["id"], "-")
            mode_label = "WAR (Advantage)"
        else:
            c1 = game.choices.get(p1["id"], "-")
            c2 = game.choices.get(p2["id"], "-")
            mode_label = "Standard Negotiation"

        p1_effects = effects.get(p1["id"], {})
        p2_effects = effects.get(p2["id"], {})

        return (
            f"📌 Market: {str(game.market_id).upper()}\n"
            f"🕹 Mode: {mode_label}\n\n"
            f"👤 {p1['name']}: {c1}\n"
            f"👤 {p2['name']}: {c2}\n\n"
            f"📊 Final Scores:\n"
            f"├ {p1['name']}: {scores.get(p1['id'], 0)}\n"
            f"└ {p2['name']}: {scores.get(p2['id'], 0)}\n\n"
            f"🧍 Player Effects:\n"
            f"├ {p1['name']}: {GameEngine.format_effects(p1_effects)}\n"
            f"└ {p2['name']}: {GameEngine.format_effects(p2_effects)}\n\n"
            f"🌐 System Effects:\n"
            f"└ {GameEngine.format_effects(economy_effects)}\n\n"
            f"📝 Summary:\n"
            f"{outcome.get('summary', '-')}"
        )

    @staticmethod
    def format_effects(effects):
        if not effects:
            return "No change"

        parts = []

        labels = {
            "public_standing": "Public Standing",
            "investor_standing": "Investor Standing",
            "institution_standing": "Institution Standing",
            "peer_standing": "Peer Standing",
            "leverage": "Leverage",
            "risk_appetite": "Risk Appetite",
            "cooperation_bias": "Cooperation Bias",
            "clarity": "Clarity",

            "trust": "Trust",
            "resource_health": "Resource Health",
            "market_heat": "Market Heat",
            "regulatory_heat": "Regulatory Heat",
            "resilience": "Resilience",
            "volatility": "Volatility",
        }

        for key, value in effects.items():
            label = labels.get(key, key)

            if value > 0:
                parts.append(f"{label} +{value}")
            else:
                parts.append(f"{label} {value}")

        return ", ".join(parts)
