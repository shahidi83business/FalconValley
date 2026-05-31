from app.schemas.challenge_schema import Question

class QuestionValidator:
    def validate(self, data: dict) -> Question:
        return Question.model_validate(data)
