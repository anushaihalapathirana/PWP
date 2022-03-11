"""
This class use to generate database and its data
"""
import secrets
from datetime import datetime
import click
from flask.cli import with_appcontext
from HRSystem import db
from HRSystem.models import Role, Employee, Department, Organization, LeavePlan, ApiKey

@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Method to initializa database
    """
    print("create database--------------------------------------------")
    db.create_all()


@click.command("testgen")
@with_appcontext
def generate_test_data():
    """
    Method to generate fake data
    """
    role = Role(name="Manager", code='MAN', description='Role manager')
    role2 = Role(name="Receptionnist", code='RES',
                 description='Role reception')
    role3 = Role(name="Team Lead", code='TL')
    role4 = Role(name="Associate team lead", code='ATL')
    role5 = Role(name="Developer", code='DEV')
    role6 = Role(name="Quality analysis", code='QA')

    org = Organization(organization_id = "O01", name="Org11", location="oulu")
    org2 = Organization(organization_id = "O02", name="Org21", location="helsinki")

    depat = Department(department_id ='D01', name="dept34", description="department number one")
    depat2 = Department(department_id ='D02', name="dept44", description="department number two")
    depat3 = Department(department_id ='D03', name="dept55", description="department number three")

    emp = Employee(employee_id = '001', first_name="anusha", last_name="pathirana",
                address="oulu", gender="F", date_of_birth=datetime(1995, 10, 21, 11, 20, 30),
                appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                active_emp=1, prefix_title='MISS', marritial_status='SINGLE',
                mobile_no='21456', basic_salary=10000, account_number="11233565456",
                role=role, organization=org, department=depat2)
    emp2 = Employee(employee_id = '002', first_name="sameera", last_name="panditha",
                    address="raksila", gender="M", date_of_birth=datetime(1998, 8, 25, 11, 20, 30),
                    appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                    active_emp=1, prefix_title='MR', marritial_status='SINGLE', mobile_no='21456',
                    basic_salary=10000, account_number="11233565456", role=role2, organization=org2,
                    department=depat)
    emp3 = Employee(employee_id = '003', first_name="madu", last_name="wicks",
                    address="kajaanentie",
                    gender="F", date_of_birth=datetime(2000, 5, 2, 11, 20, 30),
                    appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                    active_emp=1, prefix_title='MRS', marritial_status='MARRIED',
                    mobile_no='21456', basic_salary=10000, account_number="11233565456",
                    role=role3, organization=org2, department=depat3)
    emp4 = Employee(employee_id = '004', first_name="john", last_name="snow",
                    address="helsinki", gender="M", date_of_birth=datetime(1998, 12, 1, 11, 20, 30),
                    appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                    active_emp=1, prefix_title='MR', marritial_status='SINGLE',
                    mobile_no='21456', basic_salary=10000, account_number="11233565456",
                    role=role4, organization=org, department=depat)

    leav = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
        2018, 11, 21, 11, 20, 30), employee=emp)
    leav2 = LeavePlan(leave_type='CASUAL', leave_date=datetime(
        2018, 12, 1, 11, 20, 30), employee=emp3)
    leav3 = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
        2018, 1, 25, 11, 20, 30), employee=emp)

    # employee auth data
    token1 = secrets.token_urlsafe()
    token2 = secrets.token_urlsafe()
    db_key1 = ApiKey(key=ApiKey.key_hash(token1),admin=False, employee=emp2)
    db_key2 = ApiKey(key=ApiKey.key_hash(token2),admin=False, employee=emp)

    #admin auth data
    token = secrets.token_urlsafe()
    db_key = ApiKey(key=ApiKey.key_hash(token),admin=True)

    db.session.add(db_key)
    db.session.add(db_key1)
    db.session.add(db_key2)

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

    print("ADMIN TOKEN", token)
    print("EMP2 TOKEN", token1)
    print("EMP1 TOKEN", token2)

# ADMIN TOKEN HSWIouJioATKxVbu0MDGhhYSzeUIgTNUzFQnoJDjJeY
# EMP2 TOKEN 5NTb-arH7DEZrIjnEIC1XGffjJtP-qbKswTwW8anohA
# EMP1 TOKEN 84BWovWBq3klV95Q_i2YOP49eiT-QNeMT1iYKohqNY8