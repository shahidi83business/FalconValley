class SimpleScenarioEngineMock:
    OPPONENT_PROFILES = [
        {"strategy": "cooperative", "trust": 0.7},
        {"strategy": "neutral", "trust": 0.5},
        {"strategy": "aggressive", "trust": 0.3},
    ]

    @staticmethod
    def generate_opponents(count=2):
        opponents = []
        for i in range(count):
            profile = random.choice(SimpleScenarioEngineMock.OPPONENT_PROFILES)
            opponents.append({
                "id": f"op_{random.randint(1000,9999)}",
                "name": f"Faction {i+1}",
                "strategy": profile["strategy"],
                "wealth": random.randint(200, 1500),
                "trust": round(profile["trust"] + random.uniform(-0.1, 0.1), 2)
            })
        return opponents

    @staticmethod
    def generate_round(prompt, player_state):
        scenario = {
            "title": "Sample Scenario Title",
            "description": "This is a sample scenario description.",
            "difficulty": "medium"
        }
        opponents = SimpleScenarioEngineMock.generate_opponents(2)

        return {
            "scenario": scenario,
            "opponents": opponents,
            "decision_time_limit": 30,
            "player": player_state
        }