import json
from pathlib import Path
from typing import List
from app.schemas.challenge_schema import Question

class QuestionStore:
    def __init__(self, file_path: str = "app/data/generated_questions.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def load_all(self) -> List[Question]:
        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        return [Question.model_validate(item) for item in data]

    def save_all(self, questions: List[Question]):
        data = [q.model_dump() for q in questions]
        self.file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def append(self, question: Question):
        questions = self.load_all()
        questions.append(question)
        self.save_all(questions)
