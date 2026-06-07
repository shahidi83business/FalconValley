from dataclasses import dataclass
from models import Scenario


@dataclass
class JudgeResult:
    is_correct: bool
    earned_xp: int
    explanation: str | None


class JudgeService:
    def judge(self, scenario: Scenario, selected_option: int) -> JudgeResult:
        is_correct = scenario.correct_option == selected_option
        return JudgeResult(
            is_correct=is_correct,
            earned_xp=scenario.xp if is_correct else 0,
            explanation=scenario.explanation,
        )
