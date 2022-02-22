import json
import click
from flask.cli import with_appcontext
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from enum import Enum
from datetime import datetime

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
    
    role_id = db.Column(db.Integer, db.ForeignKey("role.id", ondelete="SET NULL"))
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id", ondelete="SET NULL"))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id", ondelete="SET NULL"))

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
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id", ondelete="SET NULL"))
    
    employee = db.relationship('Employee', backref='employee_leave_plan')


@click.command("init-db")
@with_appcontext
def init_db_command():
    print("create database--------------------------------------------")
    db.create_all()

@click.command("testgen")
@with_appcontext
def generate_test_data():
    role = Role(name="Manager", code='MAN', description='Role manager')
    role2 = Role(name="Receptionnist", code='RES', description='Role reception')
    role3 = Role(name="Team Lead", code='TL')
    role4 = Role(name="Associate team lead", code='ATL')
    role5 = Role(name="Developer", code='DEV')
    role6 = Role(name="Quality analysis", code='QA')


    org = Organization(name="Org1", location="oulu")
    org2 = Organization(name="Org2", location="helsinki")

    depat = Department(name="dept1", description="department number one")
    depat2 = Department(name="dept2", description="department number two")
    depat3 = Department(name="dept3", description="department number three")

    emp = Employee(first_name="anusha", last_name="pathirana", address="oulu", gender="F", date_of_birth=datetime(1995, 10, 21, 11, 20, 30), appointment_date=datetime(2018, 11, 21, 11, 20, 30),active_emp=1, suffix_title='MISS', marritial_status='SINGLE', mobile_no='21456', basic_salary=10000, account_number="11233565456", role=role, organization=org, department=depat2)
    emp2 = Employee(first_name="sameera", last_name="panditha", address="raksila", gender="M", date_of_birth=datetime(1998, 8, 25, 11, 20, 30), appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                    active_emp=1, suffix_title='MR', marritial_status='SINGLE', mobile_no='21456', basic_salary=10000, account_number="11233565456", role=role2, organization=org2, department=depat)
    emp3 = Employee(first_name="madu", last_name="wicks", address="kajaanentie", gender="F", date_of_birth=datetime(2000, 5, 2, 11, 20, 30), appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                    active_emp=1, suffix_title='MRS', marritial_status='MARRIED', mobile_no='21456', basic_salary=10000, account_number="11233565456", role=role3, organization=org2, department=depat3)
    emp4 = Employee(first_name="john", last_name="snow", address="helsinki", gender="M", date_of_birth=datetime(1998, 12, 1, 11, 20, 30), appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                    active_emp=1, suffix_title='MR', marritial_status='SINGLE', mobile_no='21456', basic_salary=10000, account_number="11233565456", role=role4, organization=org, department=depat)

    leav = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
        2018, 11, 21, 11, 20, 30), employee=emp)
    leav2 = LeavePlan(leave_type='CASUAL', leave_date=datetime(
        2018, 12, 1, 11, 20, 30), employee=emp3)
    leav3 = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
        2018, 1, 25, 11, 20, 30), employee=emp)


    db.session.add(role)
    db.session.add(role2)
    db.session.add(role3)
    db.session.add(role4)
    db.session.add(role5)
    db.session.add(role6)
    db.session.add(org)
    db.session.add(org2)

    db.session.add(depat)
    db.session.add(depat2)
    db.session.add(depat3)

    db.session.add(emp)
    db.session.add(emp2)
    db.session.add(emp3)
    db.session.add(emp4)

    db.session.add(leav)
    db.session.add(leav2)
    db.session.add(leav3)

    db.session.commit()

