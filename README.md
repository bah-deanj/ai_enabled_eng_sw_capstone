# Capstone (AI Enabled SW Engineering)
## Setup
### Clone the Repository
1. Create a new window in VSCode
1. Clone the Repository to an empty folder
1. Open the repository in VSCode

### Set Up Keys (.env)
1. Set up ```.env``` file in the base directory
1. An ```.env-example``` file is provided as an example

### Set Up Virtual Environment (.venv)
1. Open Command Prompt Terminal
    * In VSCode this is Terminal > New Terminal
1. Run: ```python -m venv .venv```
1. To start, run:  ```.venv\scripts\Activate```
1. After starting, run ```pip install -r requirements.txt```

### Initialize Database (recipes.db)
sqlite3 ./artifacts/recipes.db ".read artifacts/schema.sql"                             
sqlite3 ./artifacts/recipes.db ".read artifacts/seed_data.sql"

## Running Application ( Dockerfile - TBD)
TBD

## Component Structure and Descriptions
### Frontend Details

| Frontend Info   |  |
|------------|---------------------|
| Environment | React      |
| Location  | ```./app/``` folder & index.html |
| Run Command | ```npx serve``` |
| Visible at | http://127.0.0.1:3000/ |

| File Descriptions |   |
|------------|---------------------|
| index.html | Main html file      |
| login.jsx  | Main frontend file  |

### Backend Details
| Backend Info   |  |
|---------------|---------------------|
| Environment   | Python (venv)       |
| Location      | `./app/` folder     |
| Run Command   | ```uvicorn app.main:app --reload ```  |
| Visible at    | http://127.0.0.1:8000/docs |

| File Descriptions   |   |
|---------------------|---------------------|
| main.py             | Main backend entry point |

### Agent Details
| Agent Info   |  |
|--------------|-----------------------------|
| Environment  | Python (venv)               |
| Location     | `./app/agent/` folder       |
| Run Command  | `python app\agent\rag_agent.py` |

| File Descriptions   |   |
|---------------------|-----------------------------|
| rag_agent.py        | Generic Agent Class          |
| knowledge_base.py   | Structure for loading knowledge |
| utils.py            | Provided by instructor       |
### Artifacts
| Artifacts Info   |   |
|---------------------|-----------------------------|
| Location     | `./artifacts/` folder       |

| File Descriptions   |   |
|---------------------|-----------------------------|
| adr_001_database_choice.md | Database choice architectural decision record |
| day1_prd.md               | Product requirements document for Day 1        |
| day1_user_stories.json    | User stories for Day 1                         |
| design_review.md          | Design review notes                            |
| onboarding.db             | SQLite onboarding database                     |
| schema.sql                | SQL schema for onboarding.db                   |
| seed_data.sql             | Seed data for onboarding.db                    |


