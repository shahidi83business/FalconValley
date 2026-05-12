import os
import random
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class SimpleScenarioEngine:

    OPPONENT_PROFILES = [
        {"strategy": "cooperative", "trust": 0.7},
        {"strategy": "neutral", "trust": 0.5},
        {"strategy": "aggressive", "trust": 0.3},
    ]

    @staticmethod
    def request_ai_scenario(prompt, player_state):

        system_prompt = """
You generate short game scenarios for an economic strategy game.

Return ONLY valid JSON in this format:
{
 "title": "short title",
 "description": "2-3 sentence scenario description",
 "difficulty": "easy | medium | hard"
}
"""

        user_prompt = f"""
Base idea: {prompt}

Player state:
wealth: {player_state["wealth"]}
trust: {player_state["trust"]}
reputation: {player_state["reputation"]}
risk_level: {player_state["risk_level"]}

Create a scenario appropriate for this player.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.8,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}
        )

        scenario = response.choices[0].message.content
        import json
        return json.loads(scenario)

    @staticmethod
    def generate_opponents(count=2):

        opponents = []

        for i in range(count):
            profile = random.choice(SimpleScenarioEngine.OPPONENT_PROFILES)

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

        scenario = SimpleScenarioEngine.request_ai_scenario(prompt, player_state)

        opponents = SimpleScenarioEngine.generate_opponents(2)

        return {
            "scenario": scenario,
            "opponents": opponents,
            "decision_time_limit": 30,
            "player": player_state
        }
