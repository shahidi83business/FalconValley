import random
from typing import List, Optional
from app.schemas.challenge_schema import Question

class QuestionSelector:
    def select(
        self,
        questions: List[Question],
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        limit: int = 5
    ) -> List[Question]:
        filtered = [q for q in questions if q.active]

        if topic:
            filtered = [q for q in filtered if q.topic == topic]

        if difficulty:
            filtered = [q for q in filtered if q.difficulty == difficulty]

        random.shuffle(filtered)
        return filtered[:limit]
