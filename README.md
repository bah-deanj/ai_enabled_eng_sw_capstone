# Capstone (AI Enabled SW Engineering) - Recipe Generator
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

## Running Application ( Dockerfile - TBD - Don't think this works)
docker-compose up --build

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
| Run Command  | Can run through FastAPI Endpoint (Labelled RAG) |

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
| adr_database_choice_recipies.md | Database choice architectural decision record |
| prd_recipies.md               | Product requirements document for RecipeShare |
| user_stories_recipies.json    | User stories for RecipeShare                 |
| design_review.md              | Design review notes                          |
| recipes.db                    | SQLite database for recipes (used by app, located in artifacts/) |
| schema.sql                    | SQL schema for recipes.db                    |
| seed_data.sql                 | Seed data for recipes.db                     |
| schema_old.sql                | (Legacy) SQL schema for onboarding.db        |

Additional artifacts, documentation, and code (e.g., validation models, tests, screenshots, and Jupyter notebooks) are present in subfolders of `./artifacts/`.


