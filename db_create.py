from project import db, app
from project.models import Task, User
from datetime import date


# create the database and the db table
with app.app_context():
    db.create_all()

    db.session.commit()