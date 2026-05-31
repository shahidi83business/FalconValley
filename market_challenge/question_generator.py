from typing import Dict, Any

class QuestionGenerator:
    def generate_prompt(self, topic: str, difficulty: str, qtype: str) -> str:
        return f"""
Generate one investment education question in JSON format.
Topic: {topic}
Difficulty: {difficulty}
Type: {qtype}

Rules:
- Return valid JSON only
- Include id, type, topic, difficulty, question, xp, explanation
- If type is mcq or scenario, include 4 choices and correct_choice_key
- If type is numeric, include correct_number and tolerance
- The question must be unambiguous
- The explanation must be short and educational
"""

    def parse_generated_question(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return raw_data
