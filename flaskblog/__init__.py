from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '06034d4e636230b64a9ce204b492d68d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from flaskblog.blogs.routes import blogs
from flaskblog.comments.routes import comments
from flaskblog.reactions.routes import reactions

app.register_blueprint(blogs)
app.register_blueprint(comments)
app.register_blueprint(reactions)