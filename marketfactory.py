# marketfactory.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import uuid

from raghelper import DocChunk
from openai import AsyncOpenAI


@dataclass
class MarketBlueprint:
    id: str
    display_name: str
    required_xp: int
    base_market: str
    payoff: dict
    allowed_modes: list
    rag_docs: List[str]


class MarketFactory:

    def __init__(self):
        self.client = AsyncOpenAI()
        self._markets: Dict[str, MarketBlueprint] = {}

        # base markets (fixed)
        self._register(MarketBlueprint(
            id="energy",
            display_name="⚡ Energy Market",
            required_xp=0,
            base_market="energy",
            payoff={"coop": 4, "betray": 6, "both": -1},
            allowed_modes=["prisoner", "chicken", "war"],
            rag_docs=[
                "Energy market is a classical Prisoner’s Dilemma…",
            ],
        ))

        self._register(MarketBlueprint(
            id="tech",
            display_name="💻 Tech Market",
            required_xp=0,
            base_market="tech",
            payoff={"coop": 3, "betray": 5, "both": 1},
            allowed_modes=["prisoner", "chicken"],
            rag_docs=[
                "Tech market models competitive innovation dilemma…",
            ],
        ))

    # ------------------------------------------------------
    def _register(self, m: MarketBlueprint):
        self._markets[m.id] = m

    def get(self, market_id: str) -> MarketBlueprint:
        return self._markets[market_id]

    def all_markets(self):
        return list(self._markets.values())

    # ======================================================
    # 🎯 Generate new market dynamically using AI
    # ======================================================
    async def generate_market(
        self,
        *,
        base_market: str,
        xp_required: int,
        player_profile_summary: str,
    ) -> MarketBlueprint:

        prompt = f"""
You are a game economy designer AI.

Create a NEW advanced market based on:
- base market: {base_market}
- xp unlock requirement: {xp_required}
- player profile tendencies: {player_profile_summary}

Provide:
1) short market name
2) display title (emoji + name)
3) payoff matrix (coop, betray, both)
4) allowed modes (subset of ["prisoner","chicken","war"])
5) 3 RAG documents describing rules, scenario, and strategy
"""

        resp = await self.client.chat.completions.create(
            model="gpt-4.1",
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}],
        )

        data = resp.choices[0].message.content.strip()

        # AI returns a structured block → parse (simple & robust)
        # to avoid writing a strict parser, we use a simple approach:
        lines = data.split("\n")
        name = lines[0].replace("1)", "").strip()
        title = lines[1].replace("2)", "").strip()

        payoff = eval(lines[2].split(":", 1)[1].strip())          # dict
        modes = eval(lines[3].split(":", 1)[1].strip())           # list
        rag = [l.strip() for l in lines[4:] if l.strip()]         # docs

        market_id = name.lower().replace(" ", "_") + "_" + uuid.uuid4().hex[:5]

        m = MarketBlueprint(
            id=market_id,
            display_name=title,
            required_xp=xp_required,
            base_market=base_market,
            payoff=payoff,
            allowed_modes=modes,
            rag_docs=rag
        )

        self._register(m)
        return m

    # ======================================================
    # 🎯 convert market docs → RAG chunks
    # ======================================================
    def docs_for_rag(self, market_id: str) -> List[DocChunk]:
        m = self.get(market_id)
        return [
            DocChunk(
                id=f"{market_id}_doc{i}",
                text=doc,
                meta={"market": market_id},
            )
            for i, doc in enumerate(m.rag_docs)
        ]
