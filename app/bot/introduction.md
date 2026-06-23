**callback_manager**

**Main responsibility of this file**

This file can be considered the control center of the user’s interaction with the bot.

Every time the user presses a button:

* It detects which button the user clicked.
* It checks whether that action is allowed in the current state.
* If it is allowed, it executes the related section.
* Finally, it sends the result back to the user.

---

**Important parts it manages**

This file controls almost all major events in the game:

---

**Deal management (Deal)**

* Accepting or rejecting a deal
* Checking whether the deal can be executed
* Showing the result of the deal

---

**Quiz management**

* Receiving the player’s answer
* Checking whether the answer is correct or incorrect
* Adding XP (experience points)
* Sending the explanation of the answer

---

**Matchmaking management**

* Placing the player in a waiting queue
* Finding an opponent
* Creating a new game when two players are ready

---

**Strategy selection**

* Checking whether it is currently the time to choose a strategy
* Recording the player’s choice

---

**Final game decision**

* Recording both players’ choices
* When both have made their selection, calculating the game result

---

**War mode (Chicken Game)**

* Recording each player’s war decision
* After both players choose, calculating the result

---

## telegrampi.py

In simple terms, this file allows the program to communicate with Telegram servers without other parts of the project being involved in the communication details.

---

**Main responsibility of this file**

This file performs three main tasks:

---

**1. Connecting to Telegram**

* At the start of the program, it establishes a session with Telegram servers.

---

**2. Receiving messages and events**

* It continuously checks Telegram for new events:
  “Has a new message or button click arrived for the bot?”
* If something exists, it returns it to the program.

---

**3. Sending messages**

* Whenever another part of the program wants to send a message to a user, it uses this file.
* It sends the message to Telegram and, if needed, also includes the related keyboard buttons.

---

## ui.py

**Main responsibility of this file**

This file only builds the appearance of buttons and does not execute any game logic.

For example, it defines:

* Which buttons should be displayed
* What the text on each button is
* What identifier is sent to the program when a button is clicked

This file itself does not decide what happens after a click; that is handled by `callback_manager.py`.
