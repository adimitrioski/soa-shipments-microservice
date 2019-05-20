import os
import connexion
import pybreaker
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from pathlib import Path  # python3 only

# Read from .env file in the same folder
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

postgres_user = os.getenv("POSTGRES_USER")
postgres_db = os.getenv("POSTGRES_DB")
postgres_hostname = os.getenv("POSTGRES_HOSTNAME")
postgres_password = os.getenv("POSTGRES_PASSWORD")

# Build the PostgreSQL URL for SqlAlchemy
postgres_url = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@postgres:5432/{postgres_db}"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = postgres_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Configure PyBreaker (Circut Breaker)
db_breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=20)

from models import *
