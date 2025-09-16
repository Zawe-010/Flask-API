# extensions.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Replace with your actual DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_api_user:Zawadi06zara@172.17.0.1:5432/flask_api'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Zawadi%402006#@localhost:5432/flask_api'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myduka_user:Zawadi06zara@172.17.0.1/:5432/myduka_api'

# basedir = os.path.abspath(os.path.dirname(__file__))
# print("basedir ------", basedir)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'flask_api.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/flask_api.db'
# Disables events / tracks objects changes

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"]= "JBL@123"
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up the database connection
# CREATE USER myduka_user WITH PASSWORD ''Zawadi06zara';
# GRANT CONNECT ON DATABASE myduka_api TO myduka_user;

# CREATE USER flask_api_user WITH PASSWORD 'Zawadi06zara';
# GRANT ALL PRIVILEGES ON DATABASE flask_api TO flask_api_user;


