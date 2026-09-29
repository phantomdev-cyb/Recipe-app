# Recipe Box (Backend)

A recipe search and favourites API. It pulls recipes from [TheMealDB](https://www.themealdb.com/api.php), lets you save favourites, and supports adding your own custom recipes.

Built with FastAPI and SQLite as part of my journey into full-stack development.

## Tech Stack

- **FastAPI**: web framework
- **SQLAlchemy**: ORM
- **SQLite**: database
- **Pydantic**: request/response validation
- **httpx**: async calls to TheMealDB

## Features

- Search recipes by name (data comes from TheMealDB)
- Save recipes to a favourites list (duplicates are blocked)
- Add custom recipes of your own
- View and delete favourites

## API Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | `/recipes/get_recipes?search_item=` | Search TheMealDB and return cleaned-up recipe data |
| POST | `/post_recipes` | Save a TheMealDB recipe to favourites (skips duplicates) |
| POST | `/custom_recipes` | Save a user-authored recipe |
| GET | `/favourites` | List all saved recipes |
| DELETE | `/favourites/{id}` | Remove a favourite (404 if it doesn't exist) |

## Project Structure

```
backend/
└── app/
    ├── main.py          # app entry point, router setup, table creation
    ├── database.py      # engine, session, get_db() dependency
    ├── model.py         # SQLAlchemy Favourite table
    ├── schema.py        # Pydantic schemas (Recipe, SavedRecipe)
    └── route/
        └── favourite.py # all endpoints
```

## Running Locally

```bash
# clone the repo
git clone <your-repo-url>
cd <repo-folder>

# set up a virtual environment
cd backend
python -m venv venv
source venv/bin/activate

# install dependencies
pip install fastapi uvicorn sqlalchemy httpx

# start the server (run from inside backend/)
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the interactive API docs.

## Design Notes

- Recipes from TheMealDB and custom recipes live in one table. A `meal_id` of `null` marks a custom recipe.
- TheMealDB returns ingredients as 20 separate fields, so the API loops through them and combines them into one clean list.

## Roadmap

- [ ] Rewrite the backend in Go (`net/http` + GORM): in progress
- [ ] Build the React + TypeScript frontend (starting after the Go rewrite is done)
- [ ] Add CORS middleware for frontend integration

## Author

**White**, cybersecurity student at OAU
