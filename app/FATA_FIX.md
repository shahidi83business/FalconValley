FalconValley Refactor Task (DO NOT CHANGE PROJECT LOGIC)
You are a senior Python software engineer.
Your task is NOT to redesign the project.
Your ONLY goal is to make the current repository executable with Docker and Linux server while preserving all existing functionality.
Rules
DO NOT rewrite business logic.
DO NOT redesign architecture.
DO NOT change game logic.
DO NOT rename public classes.
DO NOT modify Telegram workflow.
DO NOT remove any feature.
Preserve every behavior.
Only fix structural problems preventing execution.
Current project structure
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
The project currently fails because imports are broken.
Example:
from db_helper import connect_to_database
while the real file is
app/data/db_helper.py
Many imports have the same issue.
Your tasks
1.
Inspect EVERY python file.
Fix every broken import.
Use package imports.
Example:
from data.db_helper import connect_to_database
or
from app.data.db_helper import connect_to_database
Choose ONE convention and use it consistently across the whole repository.
2.
Create missing
__init__.py
inside every package that needs it.
Example
app/
app/ai/
app/bot/
app/data/
app/game/
app/services/
app/utils/
3.
Make run.py the official entry point.
It should only execute the existing async main()
Example
import asyncio
from app.main import main

if __name__ == "__main__":
    asyncio.run(main())
Adapt imports if needed.
4.
Update Dockerfile if necessary.
The final image must execute
python run.py
without import errors.
5.
Create docker-compose.yml
Include
bot service
mongodb service
MongoDB should persist data using volumes.
Use environment variables.
6.
Do NOT hardcode secrets.
Read everything from
.env
If variables are missing,
create
.env.example
7.
After fixing imports,
run static verification mentally.
Ensure there are NO import cycles.
8.
Return ONLY:
List of modified files
Exact diff for every modified file
Newly created files
Dockerfile
docker-compose.yml
Any new init.py
Do NOT summarize.
Do NOT explain.
Produce complete file contents.
The output should be directly applicable to the repository.
