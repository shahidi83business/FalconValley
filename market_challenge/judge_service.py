from dataclasses import dataclass
from app.schemas.challenge_schema import Question

@dataclass
class JudgeResult:
    correct: bool
    earned_xp: int
    explanation: str

class JudgeService:
    def judge(self, question: Question, user_answer):
        if question.type in ["mcq", "scenario"]:
            correct = str(user_answer).strip().upper() == question.correct_choice_key.upper()
            return JudgeResult(
                correct=correct,
                earned_xp=question.xp if correct else 0,
                explanation=question.explanation
            )

        if question.type == "numeric":
            try:
                value = float(user_answer)
                correct = abs(value - question.correct_number) <= (question.tolerance or 0.01)
            except:
                correct = False

            return JudgeResult(
                correct=correct,
                earned_xp=question.xp if correct else 0,
                explanation=question.explanation
            )

        return JudgeResult(False, 0, "Unsupported question type")
