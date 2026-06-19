#questionfactory.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
import uuid
import json
import re
import os

from openai import AsyncOpenAI
from dotenv import load_dotenv

from models import Scenario

load_dotenv()


@dataclass
class QuestionBlueprint:
    id: str
    text: str
    options: List[str]
    correct_option: int

    topic: Optional[str] = None
    difficulty: str = "easy"
    xp: int = 10
    explanation: Optional[str] = None

    market_tags: List[str] = None
    active: bool = True
    source: str = "generated"


class QuestionFactory:
    def __init__(self):
        self.client = AsyncOpenAI(base_url=os.environ.get("OPENAI_BASE_URL"),api_key=os.environ.get("OPENAI_API_KEY"))
        self._questions: Dict[str, QuestionBlueprint] = {}

    def _register(self, q: QuestionBlueprint):
        self._questions[q.id] = q

    def get(self, question_id: str) -> QuestionBlueprint:
        return self._questions[question_id]

    def all_questions(self) -> List[QuestionBlueprint]:
        return list(self._questions.values())

    async def load_from_db(self):
        all_scenarios = await Scenario.find_all().to_list()

        for s in all_scenarios:
            bp = QuestionBlueprint(
                id=s.scenario_key,
                text=s.text,
                options=s.options,
                correct_option=s.correct_option if s.correct_option is not None else 0,
                topic=getattr(s, "topic", None),
                difficulty=getattr(s, "difficulty", "easy"),
                xp=getattr(s, "xp", 10),
                explanation=getattr(s, "explanation", None),
                market_tags=getattr(s, "market_tags", []),
                active=getattr(s, "active", True),
                source=getattr(s, "source", "generated"),
            )
            self._questions[bp.id] = bp

    async def register_new_question(self, blueprint: QuestionBlueprint):
        db_scenario = await Scenario.find_one(Scenario.scenario_key == blueprint.id)

        if db_scenario:
            db_scenario.text = blueprint.text
            db_scenario.options = blueprint.options
            db_scenario.correct_option = blueprint.correct_option
            db_scenario.topic = blueprint.topic
            db_scenario.difficulty = blueprint.difficulty
            db_scenario.xp = blueprint.xp
            db_scenario.explanation = blueprint.explanation
            db_scenario.market_tags = blueprint.market_tags or []
            db_scenario.active = blueprint.active
            db_scenario.source = blueprint.source
            await db_scenario.save()
        else:
            db_scenario = Scenario(
                scenario_key=blueprint.id,
                text=blueprint.text,
                options=blueprint.options,
                correct_option=blueprint.correct_option,
                topic=blueprint.topic,
                difficulty=blueprint.difficulty,
                xp=blueprint.xp,
                explanation=blueprint.explanation,
                market_tags=blueprint.market_tags or [],
                active=blueprint.active,
                source=blueprint.source,
            )
            await db_scenario.insert()

        self._register(blueprint)

    async def generate_question(
        self,
        *,
        market_id: str,
        topic: str,
        difficulty: str = "easy",
        xp: int = 10,
        case_text: Optional[str] = None,
        player_profile_summary: Optional[str] = None,
    ) -> QuestionBlueprint:
        prompt = f"""
You are an educational finance game question designer.

Generate exactly ONE multiple-choice question.
Return ONLY valid JSON. No markdown. No extra text.

Constraints:
- language: Persian
- market_id: "{market_id}"
- topic: "{topic}"
- difficulty: "{difficulty}"
- xp: {xp}
- exactly 4 options
- exactly 1 correct answer
- correct_option must be a zero-based integer index (0..3)
- explanation must be short, clear, and educational
- question must be relevant to the market/topic
- avoid ambiguity
- avoid trick wording
- all options should be plausible

Optional case/context:
{case_text or "No extra case provided."}

Optional player profile:
{player_profile_summary or "No profile provided."}

Return JSON with exactly:
{{
  "text": "string",
  "options": ["opt1", "opt2", "opt3", "opt4"],
  "correct_option": 0,
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "xp": {xp},
  "explanation": "string",
  "market_tags": ["{market_id}"],
  "active": true,
  "source": "generated"
}}
"""

        resp = await self.client.chat.completions.create(
            model="gpt-4.1",
            temperature=0.4,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = resp.choices[0].message.content.strip()

        json_text = raw
        m = re.search(r"\{.*\}", raw, flags=re.S)
        if m:
            json_text = m.group(0)

        data = json.loads(json_text)

        text = data["text"].strip()
        options = data["options"]
        correct_option = int(data["correct_option"])
        explanation = data.get("explanation")
        market_tags = data.get("market_tags", [market_id])

        if len(options) != 4:
            raise ValueError("Generated question must have exactly 4 options")

        if correct_option < 0 or correct_option >= len(options):
            raise ValueError("correct_option out of range")

        question_id = f"{market_id}_{topic}_{uuid.uuid4().hex[:8]}"

        bp = QuestionBlueprint(
            id=question_id,
            text=text,
            options=options,
            correct_option=correct_option,
            topic=data.get("topic", topic),
            difficulty=data.get("difficulty", difficulty),
            xp=int(data.get("xp", xp)),
            explanation=explanation,
            market_tags=market_tags,
            active=bool(data.get("active", True)),
            source=data.get("source", "generated"),
        )

        await self.register_new_question(bp)
        return bp

    async def generate_batch(
        self,
        *,
        market_id: str,
        topic: str,
        difficulty: str = "easy",
        xp: int = 10,
        count: int = 5,
        case_text: Optional[str] = None,
    ) -> List[QuestionBlueprint]:
        items = []
        for _ in range(count):
            q = await self.generate_question(
                market_id=market_id,
                topic=topic,
                difficulty=difficulty,
                xp=xp,
                case_text=case_text,
            )
            items.append(q)
        return items
