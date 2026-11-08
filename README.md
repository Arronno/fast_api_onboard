# FastAPI Onboarding · Fast Zone

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![FastAPI Users](https://img.shields.io/badge/FastAPI_Users-009688?style=flat-square&logo=fastapi&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-4051B5?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![ImageKit](https://img.shields.io/badge/ImageKit-1D4ED8?style=flat-square&logo=imagekit&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=uv&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64?style=flat-square&logo=ruff&logoColor=261230)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

A small media-sharing app built to explore FastAPI: create an account, sign in, and upload images or videos to ImageKit through a Streamlit interface.

## Features

- **User accounts** — registration, JWT sign-in, and authenticated user profiles with FastAPI Users. Access tokens last one hour.
- **Media uploads** — share images and videos with optional captions. ImageKit stores the files; SQLite stores users and post metadata.
- **Shared feed** — browse all posts, newest first, with author emails, dates, image caption overlays, and video playback.
- **Post ownership** — users can delete their own posts from the feed.
- **Account APIs** — profile updates, password reset, and email verification routes are available through the backend.

## Run locally

Requires **Python 3.14+**, **uv**, and an **ImageKit account**.

1. Install dependencies from the project root:

   ```bash
   uv sync --locked
   ```

2. Make these secrets available as environment variables:

   | Secret | Value |
   | --- | --- |
   | `JWT_SECRET` | Your manually configured JWT signing secret |
   | `IMAGEKIT_PRIVATE_KEY` | Your ImageKit private API key |

   Secrets are stored outside the code and exposed to the running app as environment variables. The API reads them with `os.getenv()` at startup.

3. Start the API:

   ```bash
   uv run python main.py
   ```

4. In a second terminal, start the UI:

   ```bash
   uv run streamlit run frontend.py
   ```

Open **[Fast Zone](http://localhost:8501)** to sign up and upload media. Interactive API documentation is available at **[localhost:8000/docs](http://localhost:8000/docs)**.

Run both commands from the project root. The API reads its secrets directly from the environment. SQLite tables are created in `test.db` on API startup, and the UI connects to `http://localhost:8000`.

## API at a glance

| Method | Route | Purpose |
| --- | --- | --- |
| `POST` | `/auth/register` | Create an account |
| `POST` | `/auth/jwt/login` | Sign in with form fields `username` (email) and `password` |
| `GET`, `PATCH` | `/auth/me` | Read or update the signed-in user's profile |
| `POST` | `/upload` | Upload multipart `file` and optional `caption` |
| `GET` | `/feed` | Retrieve the shared feed |
| `DELETE` | `/posts/{post_id}` | Delete a post owned by the signed-in user |

Profile, upload, feed, and deletion requests require an `Authorization: Bearer <token>` header. See the [API docs](http://localhost:8000/docs) for the complete account, password reset, and verification APIs.

## Project layout

```text
main.py          # Uvicorn entry point with auto-reload
frontend.py      # Streamlit login, feed, and upload screens
app/
  app.py         # FastAPI routes and application startup
  users.py       # User management and JWT authentication
  database.py    # SQLAlchemy models and async SQLite sessions
  images.py      # ImageKit client
  schemas.py     # Request and response schemas
```

## Development notes

- The UI accepts PNG, JPG, JPEG, MP4, AVI, MOV, MKV, and WebM files.
- Deleting a post removes its database record; the file remains in ImageKit.
- Password reset and verification tokens are printed to the server console; email delivery is not configured.
- Check lint and formatting with `uv run ruff check .` and `uv run ruff format --check .`.

## License

[MIT](LICENSE)
