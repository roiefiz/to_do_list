import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Integer, Column
from flask import Flask, render_template, url_for, redirect, request, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_login import login_manager, logout_user, login_user, current_user, UserMixin, LoginManager



app = Flask(__name__)
app.config["SECRET_KEY"] = 'roiefiz'
Bootstrap(app)

# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TaskTable(db.Model):
    id = Column(Integer, primary_key=True)
    task = Column(db.String(250), nullable=False)


class CreateTaskForm(FlaskForm):
    mission = StringField(label="To do:", validators=[DataRequired()])
    submit = SubmitField(label="Add task")


@app.route("/", methods=["GET", "POST"])
def home():
    form = CreateTaskForm()
    if form.validate_on_submit():
        new_task = TaskTable(
            task=form.mission.data
        )
        with app.app_context():
            db.session.add(new_task)
            db.session.commit()
    with app.app_context():
        all_tasks = db.session.query(TaskTable).all()
    return render_template('index.html', tasks=all_tasks, form=form)


@app.route("/delete", methods=["POST"])
def delete():
    delete_post_id = request.form["form_id"]
    with app.app_context():
        task = db.session.query(TaskTable).filter_by(id=delete_post_id).first()
        print(task)
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("home"))


# Testing starts here: playing with frontend, backend, Sqlite, django, jinja, forms, and more!


if __name__ == "__main__":
    app.run(debug=True)
