import pandas as pd

def run_quiz_pandas(questions):
    """
    questions: لیستی از دیکشنری‌ها با ساختار زیر:
    {
        "id": "Q1",
        "question": "متن سوال...",
        "options": ["...", "...", "..."]
    }

    خروجی: DataFrame شامل:
    - question_id
    - selected_option
    """

    answers = []

    print("\n=== شروع کوییز ===\n")

    for q in questions:
        print(f"ID: {q['id']}")
        print(q["question"])

        for idx, opt in enumerate(q["options"], start=1):
            print(f"{idx}) {opt}")

        choice = input("انتخاب شما: ")
        answers.append(choice)
        print()

    # ساخت ماتریس تصمیم
    df = pd.DataFrame({
        "question_id": [q["id"] for q in questions],
        "selected_option": answers
    })

    return df


# نمونه استفاده
if __name__ == "__main__":
    questions = [
        {
            "id": "Q1",
            "question": "اگر تورم بالا برود بانک مرکزی چه می‌کند؟",
            "options": ["کاهش نرخ بهره", "افزایش نرخ بهره", "چاپ پول"]
        },
        {
            "id": "Q2",
            "question": "اگر بیکاری زیاد شود دولت چه می‌کند؟",
            "options": ["کاهش هزینه", "سیاست انبساطی", "افزایش مالیات"]
        }
    ]

    result = run_quiz_pandas(questions)
    print("\nDecision Matrix:")
    print(result)
