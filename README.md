
# Aze's Blog

A multi-user blog built with Flask, SQLAlchemy, and PostgreSQL. Visitors can read posts and comment, registered users can submit posts for review, and the admin approves or rejects them.

## Homepage
<img align="center" width="80%" alt="Blog Home Page" src="https://github.com/user-attachments/assets/35773b22-3ab7-4f49-9c16-722b3cba4ebe" />

## Features

- Register, log in, and log out, with hashed passwords
- Admin can create, edit, and delete posts
- Users can submit posts for review (a request queue with a notification bell for the admin)
- Users can track the status of their requests, including a rejection reason
- Comments with avatars (Gravatar, or a custom image set on the profile page)
- Profile page to change display name and picture
- Pagination on the home page
- Rich text editing with CKEditor, sanitized with `nh3` before saving
- Contact form that sends an email to the site owner

## Screenshots

<p align="center">
   <img width="32%" alt="Blog Post" src="https://github.com/user-attachments/assets/a7802008-e337-433c-85bb-6efd0fd7f63f" />
   <img width="32%" alt="Blog User Requests" src="https://github.com/user-attachments/assets/4b8965f6-6134-4d16-873a-2dfdb3adfd71" />
   <img width="32%" alt="Blog Profile" src="https://github.com/user-attachments/assets/e99f5bc4-7c0d-4223-b544-cebfb96eecd1" />
   <img width="32%" alt="Blog Post History" src="https://github.com/user-attachments/assets/6f2ae60d-84cc-4da3-847a-50ccb44a22ce" />
   <img width="32%" alt="Blog Add Post" src="https://github.com/user-attachments/assets/0f971465-eeaf-4ad6-b193-8942034a7c7e" />
</p>

## Tech stack

- **Backend:** Python, Flask, Flask-WTF, Flask-CKEditor
- **Database:** PostgreSQL (hosted on Neon), accessed through SQLAlchemy 2.0
- **Frontend:** Jinja templates, Bootstrap 4 (Clean Blog theme)
- **Server:** gunicorn

## Project structure

```
main.py            # creates the app and registers blueprints
components/        # config, database, models, forms, auth helpers, utilities
routes/            # blueprints: posts, auth, pages, requests
templates/         # Jinja templates
static/            # CSS, JS, vendor libraries, optimized images
```

## Run it locally

1. Clone the repo and create a virtual environment:

   ```
   git clone <your-repo-url>
   cd <your-repo-folder>
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file (see below).

3. Create the tables:

   ```
   python -c "from components.db import init_db; init_db()"
   ```

4. Start the app:

   ```
   python main.py
   ```

   Then open http://127.0.0.1:5000.

## Environment variables

Create a `.env` file in the project root. Never commit it.

```
SECRET_KEY=a-long-random-string
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
ADMIN_EMAIL=you@example.com

# Only needed for the contact page
SENDER_EMAIL=your-gmail@gmail.com
SENDER_EMAIL_PW=your-gmail-app-password
RECEIVER_EMAIL=where-messages-go@example.com
```

Generate a secret key with:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

The account that registers with `ADMIN_EMAIL` becomes the admin.

## Deployment

The app runs with gunicorn:

```
gunicorn main:app
```

Set the same environment variables on your host (for example Render), and point `DATABASE_URL` at your hosted Postgres database. Do not set `FLASK_DEBUG` in production.

## Adding your own screenshots

Take screenshots of each page and save them in `docs/screenshots/` with the filenames used above (`home.png`, `post.png`, `profile.png`, `my-requests.png`, `requests.png`, `review.png`). Keep them under about 500 KB each, since GitHub shows them on the README page.

## Credits

Based on the Clean Blog theme by Start Bootstrap, built as part of a Python web development course and extended with PostgreSQL, SQLAlchemy, blueprints, and a post review system.
