# Flask ORM Repo (Flask-SQLAlchemy + Flask Test Client)

This repo teaches Flask ORM using Flask-SQLAlchemy and reuses database concepts from the previous lesson:
tables, constraints, relationships, joins, and transactions.

## Structure
- `data/` — generated SQLite DB files (ignored by git)
- `src/flask_orm/` — Flask app factory + models + routes
- `src/demo/` — demo script
- `src/exercises/` — in-class exercises (TODOs)
- `src/homework/` — homework (TODOs)
- `tests/` — pytest tests including Flask test client route tests
- `.github/` — GitHub Classroom autograding using `education/autograding@v1`

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
# .venv\Scripts\activate  # windows
pip install -r requirements.txt
```

## Run server (dev)
```bash
python -m src.flask_orm.run
```

## Run tests
```bash
pytest -q
```
