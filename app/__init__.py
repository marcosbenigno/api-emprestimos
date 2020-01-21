from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app.emprestimos.routes import mod
from app.login.routes import mod as login

app.register_blueprint(mod)
app.register_blueprint(login)