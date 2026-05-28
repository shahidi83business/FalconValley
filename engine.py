# engine.py

class GameEngine:
    @staticmethod
    def calculate_game_results(game, market_payoff):
        """محاسبه نتایج مذاکره (Prisoner's Dilemma)"""
        p1_id, p2_id = [p["id"] for p in game.players]
        c1 = game.choices[p1_id]
        c2 = game.choices[p2_id]

        pay = market_payoff

        if c1 == "cooperate" and c2 == "cooperate":
            return {p1_id: pay["coop"], p2_id: pay["coop"]}
        elif c1 == "cooperate" and c2 == "defect":
            return {p1_id: 0, p2_id: pay["betray"]}
        elif c1 == "defect" and c2 == "cooperate":
            return {p1_id: pay["betray"], p2_id: 0}
        else:
            return {p1_id: pay["both"], p2_id: pay["both"]}

    @staticmethod
    def calculate_chicken_results(game):
        """محاسبه نتایج جنگ (Chicken Game)"""
        p1_id, p2_id = [p["id"] for p in game.players]
        c1 = game.war_choices[p1_id]
        c2 = game.war_choices[p2_id]

        matrix = {
            ("yield", "yield"): (0, 0),
            ("yield", "straight"): (-1, 2),
            ("straight", "yield"): (2, -1),
            ("straight", "straight"): (-5, -5),
        }
        r1, r2 = matrix.get((c1, c2), (0, 0))

        r1 += game.war_penalty.get(p1_id, 0)
        r2 += game.war_penalty.get(p2_id, 0)

        return {p1_id: r1, p2_id: r2}

    @staticmethod
    def calculate_war_advantage_results(game):
        """محاسبه نتایج وقتی یکی جنگ و دیگری مذاکره را انتخاب کرده است"""
        p1_id, p2_id = [p["id"] for p in game.players]
        s1 = game.strategy[p1_id]
        s2 = game.strategy[p2_id]

        if s1 == "war" and s2 == "negotiation":
            return {p1_id: 3, p2_id: -2}
        elif s1 == "negotiation" and s2 == "war":
            return {p1_id: -2, p2_id: 3}
        return {p1_id: 0, p2_id: 0}

    @staticmethod
    def generate_result_text(game, scores, mode="NORMAL"):
        """تولید متن خروجی برای حالت‌های مختلف بازی"""
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
