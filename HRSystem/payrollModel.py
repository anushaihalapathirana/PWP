import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///payroll.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    employee_id =  db.Column(db.Integer, nullable=False)


# how to run the database

# python3
# from models import db
# db.create_all()
# from payrollModel import Payroll
# from datetime import datetime
# payroll = Payroll(date=datetime(2018, 11, 21, 11, 20, 30), amount = 12563, employee_id = 1)
# db.session.add(payroll)
# db.session.commit()


 