import json

# Load your current JSON file
with open("messages.json", "r", encoding="utf-8") as f:
    old_data = json.load(f)  # assuming your file is proper JSON

# Create GPT-style conversation
conversation = []
for item in old_data:
    conversation.append({
        "role": "user",
        "content": item["question"]
    })
    conversation.append({
        "role": "assistant",
        "content": item["answer"]
    })

# Save to a new JSON file
with open("gpt_conversation.json", "w", encoding="utf-8") as f:
    json.dump(conversation, f, ensure_ascii=False, indent=2)

print("Conversion done! Saved as gpt_conversation.json")
