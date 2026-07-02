class MarketFactoryMock:
    def __init__(self):
        self._markets = {
            "energy": {
                "id": "energy",
                "display_name": "⚡ Energy Market",
                "required_xp": 0,
                "entry_fee": 0,
                "base_market": "energy",
                "payoff": {"coop": 4, "betray": 6, "both": -1},
                "allowed_modes": ["prisoner", "chicken", "war"],
                "rag_docs": ["Energy market is a classical Prisoner's Dilemma..."],
            },
            "tech": {
                "id": "tech",
                "display_name": "💻 Tech Market",
                "required_xp": 0,
                "entry_fee": 0,
                "base_market": "tech",
                "payoff": {"coop": 3, "betray": 5, "both": 1},
                "allowed_modes": ["prisoner", "chicken"],
                "rag_docs": ["Tech market models competitive innovation dilemma..."],
            }
        }

    def get(self, market_id):
        return self._markets.get(market_id)

    def all_markets(self):
        return list(self._markets.values())

    def register_new_market(self, blueprint):
        self._markets[blueprint["id"]] = blueprint
