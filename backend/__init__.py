from flask import Flask

# for using form
from backend.config import Config

# for database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# for login
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login
login = LoginManager(app)
login.login_view = 'login'

from backend import routes, models