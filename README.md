## Video Overview
https://www.loom.com/share/54451e024b3343b996ea60cd192f59c7

## How to run locally

### Set up local variables

Copy .env.example to .env.local and set values where needed

### Install dependencies and launch app
```
# Run setup.sh from root
chmod +x setup.sh && ./setup.sh
```
See webapp running at http://localhost:3000

## How to run database migrations
1. Makes changes to sqlalchemy models in backend/models/um_database.py
2. Run `alembic revision --autogenerate -m "description of changes"`
3. Run `alembic upgrade head`

## Additional work I wish I could do
- Make frontend more modular (creating components for rendering case report page)
- Persist cases in database using postgres (and add a migration script with alembic)
- Add validators to pydantic models (e.g. cpt codes 5 char alphanumeric, etc.)
- Additional logging

## Stretch goals
- History of uploaded files
- Navigation through case reports with up to date statuses
- Worklists for cases
