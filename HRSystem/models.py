import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from enum import Enum

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hrcore.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)




@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class TitleEnum(Enum):
    MR = 'Mr'
    MISS = 'Miss'
    MRS = 'Mrs'
    DR = 'Dr'

class MarritialEnum(Enum):
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    SINGLE = 'Single'
    WIDOWED = 'Widowed'
    UNAVAILABLE = 'Unavailable'

class LeaveTypeEnum(Enum):
    MEDICAL = 'Medical'
    CASUAL = 'Casual'
    PATERNITY = 'Paternity'
    MATERNITY = 'Maternity'
    SABBATICAL = 'Sabbatical'
    UNPAID = 'Unpaid'

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    middle_name = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(32), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    active_emp = db.Column(db.Boolean, default = True, nullable=False)
    suffix_title = db.Column(db.Enum(TitleEnum), nullable=False)
    marritial_status = db.Column(db.Enum(MarritialEnum), nullable=False)
    mobile_no = db.Column(db.String(256), nullable=False)
    basic_salary = db.Column(db.Integer, nullable=False)
    account_number = db.Column(db.String(256), nullable=False)
    
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    organization = db.relationship('Organization', backref='employee_organization')
    department = db.relationship('Department', backref='employee_department')
    role = db.relationship('Role', backref='employee_role')
   

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique = True)
    location = db.Column(db.String(256), nullable=False)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique = True)
    description = db.Column(db.String(256), nullable=True)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique = True)
    code = db.Column(db.String(256), nullable=False, unique = True)
    description = db.Column(db.String(256), nullable=True)


class LeavePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_type = db.Column(db.Enum(LeaveTypeEnum), nullable=False)
    reason = db.Column(db.String(256), nullable=True)
    leave_date = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    
    employee = db.relationship('Employee', backref='employee_leave_plan')

