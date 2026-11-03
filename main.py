from flask import Flask
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
#own modules
from components.config import SECRET_KEY
from components.auth import inject_state
from components.db import close_db
from routes.pages_bp import pages
from routes.posts_bp import posts
from routes.auth_bp import auth
from routes.requests_bp import requests_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
CKEditor(app)
Bootstrap(app)

app.teardown_appcontext(close_db)
app.context_processor(inject_state)

for bp in (pages,posts,auth,requests_bp):
    app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
