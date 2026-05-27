# engine.py

class GameEngine:
    @staticmethod
    def calculate_game_results(game_data, market_payoff):
        """محاسبه نتایج مذاکره (Prisoner's Dilemma)"""
        p1_id, p2_id = [p["id"] for p in game_data["players"]]
        c1, c2 = game_data["choices"][p1_id], game_data["choices"][p2_id]
        
        pay = market_payoff
        # منطق ماتریس بازار
        if c1 == "cooperate" and c2 == "cooperate":
            return {p1_id: pay["coop"], p2_id: pay["coop"]}
        elif c1 == "cooperate" and c2 == "defect":
            return {p1_id: 0, p2_id: pay["betray"]}
        elif c1 == "defect" and c2 == "cooperate":
            return {p1_id: pay["betray"], p2_id: 0}
        else:
            return {p1_id: pay["both"], p2_id: pay["both"]}

    @staticmethod
    def calculate_chicken_results(game_data):
        """محاسبه نتایج جنگ (Chicken Game)"""
        p1_id, p2_id = [p["id"] for p in game_data["players"]]
        c1, c2 = game_data["war_choices"][p1_id], game_data["war_choices"][p2_id]

        # ماتریس پایه Chicken
        matrix = {
            ("yield", "yield"): (0, 0),
            ("yield", "straight"): (-1, 2),
            ("straight", "yield"): (2, -1),
            ("straight", "straight"): (-5, -5)
        }
        r1, r2 = matrix.get((c1, c2), (0, 0))

        # اعمال جریمه‌های فشار جنگ (War Pressure)
        r1 += game_data["war_penalty"].get(p1_id, 0)
        r2 += game_data["war_penalty"].get(p2_id, 0)

        return {p1_id: r1, p2_id: r2}

    @staticmethod
    def calculate_war_advantage_results(game_data):
        """محاسبه نتایج وقتی یکی جنگ و دیگری مذاکره را انتخاب کرده است"""
        p1_id, p2_id = [p["id"] for p in game_data["players"]]
        s1, s2 = game_data["strategy"][p1_id], game_data["strategy"][p2_id]

        if s1 == "war" and s2 == "negotiation":
            return {p1_id: 3, p2_id: -2}
        elif s1 == "negotiation" and s2 == "war":
            return {p1_id: -2, p2_id: 3}
        return {p1_id: 0, p2_id: 0}

    @staticmethod
    def generate_result_text(game_data, scores, mode="NORMAL"):
        """تولید متن خروجی واحد برای هر سه حالت"""
        p1, p2 = game_data["players"]
        
        if mode == "CHICKEN":
            c1, c2 = game_data["war_choices"][p1["id"]], game_data["war_choices"][p2["id"]]
            mode_label = "CHICKEN (War)"
        elif mode == "ADVANTAGE":
            c1, c2 = game_data["strategy"][p1["id"]], game_data["strategy"][p2["id"]]
            mode_label = "WAR (Advantage)"
        else:
            c1, c2 = game_data["choices"][p1["id"]], game_data["choices"][p2["id"]]
            mode_label = "Standard Negotiation"

        return (
            f"📌 Market: {game_data['market'].upper()}\n"
            f"🕹 Mode: {mode_label}\n\n"
            f"👤 {p1['name']}: {c1}\n"
            f"👤 {p2['name']}: {c2}\n\n"
            f"📊 Final Scores:\n"
            f"├ {p1['name']}: {scores[p1['id']]}\n"
            f"└ {p2['name']}: {scores[p2['id']]}"
        )
