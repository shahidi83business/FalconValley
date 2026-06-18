import random


class DealEngine:

    @staticmethod
    def resolve(deal):

        capital = deal.required_capital
        reward = deal.expected_return
        risk = deal.risk_level

        roll = random.random()

        if roll < risk:

            return {
                "status": "failed",
                "capital_change": -capital,
                "trust_change": -5,
                "message": "The deal collapsed. Counterparty risk materialized."
            }

        profit = reward - capital

        return {
            "status": "completed",
            "capital_change": profit,
            "trust_change": 3,
            "message": "The deal succeeded."
        }
