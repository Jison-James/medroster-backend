# MedRoster Backend

MedRoster is a hospital roster management system. This repository contains the **Django REST API backend**.

## Tech Stack

- **Python 3.12+**
- **Django 6.0** — web framework
- **Django REST Framework** — API toolkit
- **PostgreSQL** — database
- **dj-rest-auth + SimpleJWT** — JWT authentication
- **django-allauth** — social & email authentication
- **django-cors-headers** — CORS support
- **Gunicorn** — production WSGI server
- **WhiteNoise** — static file serving

## Core Modules

| Module | Description |
|---|---|
| `users/` | User model, profiles, serializers |
| `roster/` | Roster, shifts, leave, conflicts, notifications |
| `roster/services/scheduler/` | Scheduling engine (constraint, fairness, rotation, scoring, assignment) |
| `roster/services/conflict_engine/` | Conflict detection & suggestion engine |

## Prerequisites

- Python ≥ 3.12
- PostgreSQL ≥ 14
- pip

## Installation

```bash
git clone https://github.com/Jison-James/medroster-backend.git
cd medroster-backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Environment Variables

Copy the example and configure:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | insecure dev key |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins | `http://localhost:5173` |
| `DATABASE_URL` | PostgreSQL connection string | local PostgreSQL |

## Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

To load demo data:

```bash
python manage.py populate_demo_data
```

## Local Development

```bash
python manage.py runserver
```

The API runs at **http://localhost:8000/api/**.

Make sure the [medroster-frontend](https://github.com/Jison-James/medroster-frontend) has `VITE_API_BASE_URL` pointing to this server.

## API Endpoints

| Prefix | Description |
|---|---|
| `/api/auth/` | Login, logout, password change (dj-rest-auth) |
| `/api/auth/registration/` | User registration |
| `/api/users/profiles/` | User profiles CRUD |
| `/api/roster/rosters/` | Roster CRUD |
| `/api/roster/shifts/` | Shift entries |
| `/api/roster/leaves/` | Leave requests |
| `/api/roster/conflicts/` | Conflict detection |
| `/api/roster/notifications/` | Notifications |
| `/api/roster/settings/` | Roster rules |
| `/api/roster/shift-templates/` | Shift templates |

## Render Deployment

1. Create a new **Web Service** on [Render](https://render.com).
2. Connect the `medroster-backend` GitHub repository.
3. Set the following:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn medRoster.wsgi:application --bind 0.0.0.0:$PORT`
4. Add a **PostgreSQL** database on Render and link it.
5. Add environment variables:
   - `SECRET_KEY` = a strong random string
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `medroster-backend.onrender.com`
   - `CORS_ALLOWED_ORIGINS` = `https://medroster-frontend.onrender.com`
   - `DATABASE_URL` = (auto-populated by Render when you link the PostgreSQL addon)
6. Deploy.

## Project Structure

```
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── medRoster/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/              # User model & auth
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── roster/             # Core roster module
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── permissions.py
    └── services/
        ├── scheduler/         # Auto-scheduling engine
        │   ├── scheduler.py
        │   ├── constraint_engine.py
        │   ├── fairness_engine.py
        │   ├── rotation_engine.py
        │   ├── scoring_engine.py
        │   └── assignment_engine.py
        └── conflict_engine/   # Conflict detection
            ├── engine.py
            ├── suggestion_engine.py
            └── *_validator.py
```

## License

Private — IntPurple
