from dataclasses import dataclass, field
from typing import List
from app.schemas.challenge_schema import Question
from app.services.judge_service import JudgeService, JudgeResult

@dataclass
class SessionAnswer:
    question_id: str
    user_answer: str
    correct: bool
    earned_xp: int

@dataclass
class ChallengeSession:
    questions: List[Question]
    current_index: int = 0
    total_xp: int = 0
    answers: List[SessionAnswer] = field(default_factory=list)

    def current_question(self):
        if self.current_index >= len(self.questions):
            return None
        return self.questions[self.current_index]

class ChallengeSessionService:
    def __init__(self):
        self.judge = JudgeService()

    def submit_answer(self, session: ChallengeSession, user_answer: str) -> JudgeResult:
        question = session.current_question()
        result = self.judge.judge(question, user_answer)

        session.answers.append(SessionAnswer(
            question_id=question.id,
            user_answer=user_answer,
            correct=result.correct,
            earned_xp=result.earned_xp
        ))

        session.total_xp += result.earned_xp
        session.current_index += 1
        return result
