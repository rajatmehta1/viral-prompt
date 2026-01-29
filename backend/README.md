# ViralPrompt Backend

A FastAPI-powered backend for the ViralPrompt platform - a Pinterest-style gallery for viral content and AI prompts.

## Features

- 🚀 **FastAPI** - High-performance async Python web framework
- 🗃️ **SQLAlchemy** - Async ORM with PostgreSQL support
- 🔐 **JWT Authentication** - Secure user authentication
- 📝 **Jinja2 Templates** - Server-side rendered HTML templates
- 📊 **Swagger UI** - Auto-generated API documentation at `/docs`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API routes
│   └── utils/               # Utility functions
├── templates/               # Jinja2 templates
├── static/                  # Static assets (CSS, JS)
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 13+ (or use SQLite for development)
- pip or poetry

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The application will be available at http://localhost:8000

## API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `POST /api/auth/logout` - Logout user

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/{username}` - Get user by username

### Prompts
- `GET /api/prompts` - List prompts with filters
- `POST /api/prompts` - Create a new prompt
- `GET /api/prompts/{id}` - Get prompt by ID
- `PUT /api/prompts/{id}` - Update prompt
- `DELETE /api/prompts/{id}` - Delete prompt
- `POST /api/prompts/{id}/like` - Like a prompt
- `DELETE /api/prompts/{id}/like` - Unlike a prompt

### Content
- `GET /api/content` - List content with filters
- `GET /api/content/trending` - Get trending content
- `POST /api/content` - Create new content
- `GET /api/content/{id}` - Get content by ID
- `PUT /api/content/{id}` - Update content
- `DELETE /api/content/{id}` - Delete content
- `POST /api/content/{id}/like` - Like content
- `POST /api/content/{id}/view` - Record view

### Collections
- `GET /api/collections` - List public collections
- `GET /api/collections/me` - Get current user's collections
- `POST /api/collections` - Create a collection
- `GET /api/collections/{id}` - Get collection by ID
- `PUT /api/collections/{id}` - Update collection
- `DELETE /api/collections/{id}` - Delete collection
- `POST /api/collections/{id}/items` - Add item to collection
- `DELETE /api/collections/{id}/items/{item_id}` - Remove item from collection

## Pages

All HTML templates are rendered via the pages router:
- `/` - Home page
- `/explore` - Explore categories
- `/trending` - Trending content
- `/prompt-library` - Prompt library
- `/dashboard` - User dashboard
- `/profile` - User profile
- `/settings` - User settings
- `/collections` - Collections
- `/signin` - Sign in page
- `/analytics` - Analytics dashboard
- `/ai-books` - AI Books generator
- `/ai-music` - AI Music generator
- `/ai-video-generator` - AI Video generator
- `/caption-generator` - Caption generator
- `/script-writer` - Script writer
- `/reel-creator` - Reel creator

## Database

The application uses PostgreSQL. Create the database and run the schema:

```sql
CREATE DATABASE viralprompt;
```

Then apply the schema from `../db/schema.sql`.

## Development

### Running in development mode
```bash
uvicorn app.main:app --reload --port 8000
```

### Running with Docker
```bash
docker build -t viralprompt-backend .
docker run -p 8000:8000 viralprompt-backend
```

## License

MIT License
