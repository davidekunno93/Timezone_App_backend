from flask import Flask
from config import Config
from flask_cors import CORS
from .models import db
from flask_migrate import Migrate

# instanciating app in Flask class
app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

# this line of code - directs the flask app to routes for web routes
from . import routes
from . import models

db.init_app(app)
migrate = Migrate(app, db)

# new directory for api routes
from .api.routes import api
app.register_blueprint(api)

# new directory for organization
from .auth.routes import auth
app.register_blueprint(auth)