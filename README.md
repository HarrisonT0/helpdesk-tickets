# Helpdesk Manager
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)
![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)
![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)

Web-app for handling IT helpdesk tickets and users.

## Run
The app was initialised using `uv`. If you have `uv`, you can clone the repo and run
```
uv venv .venv
source .venv/bin/activate
uv pip install # Install dependencies for app to run
uv pip install -G dev # Install dev dependencies for development
```

**Standard Python tooling is also supported**, and you can setup and install dependencies with Python+Pip using:
```
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Once the app is running, you can log into any of the default user accounts created in the database seed script (such as *admin@company.com*), using the default password: *Password123!*. You can see the seed script for more details at `helpdesk_management/utils/seed_database.py`

## Development
Commits follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) spec.  
`ruff` is used for linting and formatting.  
`pytest` is used for (unit) testing critical functionality via endpoints - use `pytest tests/` to run the unit tests.