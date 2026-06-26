# FalconValley Refactor Task (DO NOT CHANGE PROJECT LOGIC)

You are a senior Python software engineer.

Your task is NOT to redesign the project.
Your ONLY goal is to make the current repository executable with Docker and Linux server while preserving all existing functionality.

## ⚠️ Rules

DO NOT rewrite business logic.  
DO NOT redesign architecture.  
DO NOT change game logic.  
DO NOT rename public classes.  
DO NOT modify Telegram workflow.  
DO NOT remove any feature.  
Preserve every behavior.

Only fix structural problems preventing execution.

## 📁 Current Project Structure

app/
    ai/
    bot/
    data/
    game/
    services/
    utils/

    main.py
    main-old.py
    wsgi.py

run.py
requirements.txt
Dockerfile

## ❗ Current Issue

The project currently fails due to broken imports.

Example:
from db_helper import connect_to_database

while the real file is:
app/data/db_helper.py

Many imports across the project have the same issue.

## 🎯 Your Tasks

1. Fix ALL imports  
- Inspect EVERY Python file  
- Fix all broken imports  
- Use package imports only  
- Choose ONE consistent convention and apply it everywhere  

Example:
from app.data.db_helper import connect_to_database  
or  
from data.db_helper import connect_to_database  

(Choose one style and use it consistently across the project)

2. Add missing __init__.py  
Ensure every required package contains __init__.py:

app/
app/ai/
app/bot/
app/data/
app/game/
app/services/
app/utils/

3. Fix entry point (run.py)  
run.py must be the official entry point and only execute async main():

import asyncio
from app.main import main

if __name__ == "__main__":
    asyncio.run(main())

Adjust imports if needed.

4. Dockerfile  
Update if necessary so the container runs:

python run.py

without import errors.

5. docker-compose.yml  
Create docker-compose.yml including:
- bot service
- mongodb service

MongoDB must:
- persist data using volumes
- use environment variables

6. Environment variables  
DO NOT hardcode secrets.  
Read everything from .env  

Create .env.example if missing variables exist.

7. Static verification  
After fixing imports:
- Ensure NO import cycles exist
- Ensure project runs on Linux/Docker

## 📦 Final Output Requirements

Return ONLY:
- List of modified files
- Exact diff for every modified file
- Newly created files
- Final Dockerfile
- Final docker-compose.yml
- Any new __init__.py files

## ❌ Output Restrictions

DO NOT summarize  
DO NOT explain  
DO NOT add commentary  
DO NOT omit diffs  

## ✅ Goal

The final output must be directly applicable to the repository and fully executable in Docker without import errors.
