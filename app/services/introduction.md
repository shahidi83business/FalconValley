## judge_service.py

This file (JudgeService) is much simpler than the others and has a clear role.

---

**Simple mental model**

This class acts like a judge in the game:

It checks whether the player selected the correct answer and then awards XP accordingly.

---

## questionfactor.py

This file (questionfactory.py) is a system for generating and managing educational / game-economy questions.

It works with both the database and AI to generate questions.

---

In simple terms:

This is where quiz questions are created, stored, and generated for players.

---

## session_service.py

This file (session_service.py) is very simple and has a single clear responsibility.

---

**Simple mental model**

This function does only one thing:

It creates a “session” for starting a game round and stores it in the database.

---

## state_service.py

This file (StateService) is one of the most important parts of the entire system because it is where the actual game results are applied to the data.

---

**Simple mental model**

This class acts like an effect-applier system:

* It does not generate scores ❌
* It does not make decisions ❌
* It only applies the results to the game world ✅
