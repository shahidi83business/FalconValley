# marketfactory.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List
import uuid, json, re

from raghelper import DocChunk
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from models import Market  # <-- مهم: ایمپورت مدل دیتابیس
load_dotenv()


@dataclass
class MarketBlueprint:
    id: str
    display_name: str
    required_xp: int
    entry_fee: int
    base_market: str
    payoff: dict
    allowed_modes: list
    rag_docs: List[str]


class MarketFactory:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self._markets: Dict[str, MarketBlueprint] = {}

        # base markets (fixed)
        self._register(MarketBlueprint(
            id="energy",
            display_name="⚡ Energy Market",
            required_xp=0,
            entry_fee=0,
            base_market="energy",
            payoff={"coop": 4, "betray": 6, "both": -1},
            allowed_modes=["prisoner", "chicken", "war"],
            rag_docs=["Energy market is a classical Prisoner’s Dilemma…"],
        ))

        self._register(MarketBlueprint(
            id="tech",
            display_name="💻 Tech Market",
            required_xp=0,
            entry_fee=0,
            base_market="tech",
            payoff={"coop": 3, "betray": 5, "both": 1},
            allowed_modes=["prisoner", "chicken"],
            rag_docs=["Tech market models competitive innovation dilemma…"],
        ))

    def _register(self, m: MarketBlueprint):
        self._markets[m.id] = m

    def get(self, market_id: str) -> MarketBlueprint:
        return self._markets[market_id]

    def all_markets(self) -> List[MarketBlueprint]:
        return list(self._markets.values())

    async def load_from_db(self):
        all_markets = await Market.find_all().to_list()
        for m in all_markets:
            bp = MarketBlueprint(
                id=m.market_id,
                display_name=m.display_name,
                required_xp=m.required_xp,
                entry_fee=getattr(m, "entry_fee", 0),
                base_market=m.base_market,
                payoff=m.payoff,
                allowed_modes=m.allowed_modes,
                rag_docs=m.rag_docs,
            )
            self._markets[bp.id] = bp

    async def register_new_market(self, blueprint: MarketBlueprint):
        # upsert برای اینکه اگر market_id تکراری شد، آپدیت کند
        db_market = Market(
            market_id=blueprint.id,
            display_name=blueprint.display_name,
            required_xp=blueprint.required_xp,
            entry_fee=blueprint.entry_fee,
            base_market=blueprint.base_market,
            payoff=blueprint.payoff,
            allowed_modes=blueprint.allowed_modes,
            rag_docs=blueprint.rag_docs,
        )
        await db_market.save()
        self._register(blueprint)

    # -------------------------------
    # Generate new market using AI
    # -------------------------------
    async def generate_market(
        self,
        *,
        base_market: str,
        xp_required: int,
        player_profile_summary: str,
    ) -> MarketBlueprint:

        prompt = f"""
You are a game economy designer AI.

Generate ONE advanced market. Return ONLY valid JSON (no markdown).

Constraints:
- base_market: "{base_market}"
- required_xp: {xp_required}
- allowed_modes subset of ["prisoner","chicken","war"]
- payoff must be JSON object with keys: "coop","betray","both" (ints)
- entry_fee must scale with required_xp (higher xp -> higher entry_fee)
- display_name must include an emoji and a short catchy name
- rag_docs must be an array of exactly 3 short strings

Player tendencies:
{player_profile_summary}

Return JSON with exactly:
{{
  "short_name": "string (no emoji)",
  "display_name": "string (with emoji)",
  "entry_fee": 123,
  "payoff": {{"coop": 0, "betray": 0, "both": 0}},
  "allowed_modes": ["prisoner"],
  "rag_docs": ["...", "...", "..."]
}}
"""

        resp = await self.client.chat.completions.create(
            model="gpt-4.1",
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = resp.choices[0].message.content.strip()

        # اگر احیاناً AI چیزی قبل/بعد JSON گذاشت، JSON را جدا کن
        json_text = raw
        m = re.search(r"\{.*\}", raw, flags=re.S)
        if m:
            json_text = m.group(0)

        data = json.loads(json_text)

        short_name = data["short_name"].strip()
        title = data["display_name"].strip()
        entry_fee = int(data["entry_fee"])
        payoff = data["payoff"]
        modes = data["allowed_modes"]
        rag = data["rag_docs"]

        market_id = (
            short_name.lower().replace(" ", "_")
            + "_"
            + uuid.uuid4().hex[:5]
        )

        bp = MarketBlueprint(
            id=market_id,
            display_name=title,
            required_xp=xp_required,
            entry_fee=entry_fee,
            base_market=base_market,
            payoff=payoff,
            allowed_modes=modes,
            rag_docs=rag,
        )

        await self.register_new_market(bp)
        return bp

    def docs_for_rag(self, market_id: str) -> List[DocChunk]:
        m = self.get(market_id)
        return [
            DocChunk(id=f"{market_id}_doc{i}", text=doc, meta={"market": market_id})
            for i, doc in enumerate(m.rag_docs)
        ]
