## db_helper.py

This file is responsible for connecting the project to the database.

In simple terms, whenever the program needs to store or retrieve information such as users, games, markets, trades, or questions, it first connects to the database through this file.

---

**Main responsibility of this file**

This file performs three main tasks:

---

**1. Establishing a connection to MongoDB**

* When the program starts, it tries to connect to the database.
* If the connection is successful, the program can read and store data.

---

**2. Preparing data models**

* It registers all project models (such as users, markets, trades, etc.) with the database so they can interact with it.

---

**3. Closing the connection**

* When the program ends, it properly closes the database connection to free system resources.

---

## models.py

This file is one of the most important files in the project because it defines the structure of all project data.

If we think of the project as an online game, this file defines what types of data exist, what properties each one has, and how they are stored in the database.

---

**Main responsibility of this file**

This file is essentially the database schema of the project.

It defines:

* What information a user has
* What properties a user profile includes
* How markets are defined
* What structure questions have
* How games are stored
* How player decisions are recorded
* What information trades contain
* How the in-game economy state is maintained
