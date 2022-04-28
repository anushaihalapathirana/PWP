"""
This class use to generate database and its data
"""
import secrets
from datetime import datetime
import click
from flask.cli import with_appcontext
from hr_system import db
from hr_system.models import Role, Employee, Department, Organization, LeavePlan, ApiKey


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

    org = Organization(organization_id="O01", name="Org11", location="oulu")
    org2 = Organization(
        organization_id="O02",
        name="Org21",
        location="helsinki")
    org3 = Organization(organization_id="O03", name="Org13", location="alsijdais")
    org4 = Organization(organization_id="O04", name="Org14", location="askjd")
    org5 = Organization(organization_id="O05", name="Org15", location="ouajsdhlu")


    depat = Department(
        department_id='D01',
        name="dept1",
        description="department number one")
    depat2 = Department(
        department_id='D02',
        name="dept2",
        description="department number two")
    depat3 = Department(
        department_id='D03',
        name="dept3",
        description="department number three")
    depat4 = Department(
        department_id='D04',
        name="dept4",
        description="department number 4")
    depat5 = Department(
        department_id='D05',
        name="dept5",
        description="department number 5")

    emp = Employee(
        employee_id='E01',
        first_name="anusha",
        last_name="pathirana",
        address="oulu",
        gender="F",
        date_of_birth=datetime(
            1995,
            10,
            21,
            11,
            20,
            30),
        appointment_date=datetime(
            2018,
            11,
            21,
            11,
            20,
            30),
        active_emp=1,
        prefix_title='MISS',
        marritial_status='SINGLE',
        mobile_no='21456',
        basic_salary=10000,
        account_number="11233565456",
        role=role,
        organization=org,
        department=depat)
    emp2 = Employee(
        employee_id='E02',
        first_name="sameera",
        last_name="panditha",
        address="raksila",
        gender="M",
        date_of_birth=datetime(
            1998,
            8,
            25,
            11,
            20,
            30),
        appointment_date=datetime(
            2018,
            11,
            21,
            11,
            20,
            30),
        active_emp=1,
        prefix_title='MR',
        marritial_status='SINGLE',
        mobile_no='21456',
        basic_salary=12000,
        account_number="15898965456",
        role=role2,
        organization=org2,
        department=depat)
    emp3 = Employee(
        employee_id='E03',
        first_name="madu",
        last_name="wicks",
        address="kajaanentie",
        gender="F",
        date_of_birth=datetime(
            2000,
            5,
            2,
            11,
            20,
            30),
        appointment_date=datetime(
            2018,
            11,
            21,
            11,
            20,
            30),
        active_emp=1,
        prefix_title='MRS',
        marritial_status='MARRIED',
        mobile_no='21456',
        basic_salary=9500,
        account_number="58745665456",
        role=role3,
        organization=org2,
        department=depat3)
    emp4 = Employee(
        employee_id='E04',
        first_name="john",
        last_name="snow",
        address="helsinki",
        gender="M",
        date_of_birth=datetime(
            1998,
            12,
            1,
            11,
            20,
            30),
        appointment_date=datetime(
            2018,
            11,
            21,
            11,
            20,
            30),
        active_emp=1,
        prefix_title='MR',
        marritial_status='SINGLE',
        mobile_no='21456',
        basic_salary=10000,
        account_number="11233565456",
        role=role4,
        organization=org,
        department=depat)

    leav = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
        2022, 4, 21, 11, 20, 30), employee=emp)
    leav2 = LeavePlan(leave_type='CASUAL', leave_date=datetime(
        2022, 4, 1, 11, 20, 30), employee=emp3)
    leav3 = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
        2022, 4, 5, 11, 20, 30), employee=emp)
    leav3 = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
        2022, 4, 6, 11, 20, 30), employee=emp)

    # employee auth data
    token1 = secrets.token_urlsafe()
    token2 = secrets.token_urlsafe()
    db_key1 = ApiKey(key=ApiKey.key_hash(token1), admin=False, employee=emp2)
    db_key2 = ApiKey(key=ApiKey.key_hash(token2), admin=False, employee=emp)

    # admin auth data
    token = secrets.token_urlsafe()
    db_key = ApiKey(key=ApiKey.key_hash(token), admin=True)

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
    db.session.add(org3)
    db.session.add(org4)
    db.session.add(org5)

    db.session.add(depat)
    db.session.add(depat2)
    db.session.add(depat3)
    db.session.add(depat4)
    db.session.add(depat5)


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

# ADMIN TOKEN Hz7FWRIDVX8MyK2h8XLPkGj8ToGgWofHlS01lLBKvzY
# EMP2 TOKEN SM_6rfSJXCk67DKdN9bQm2l9IYbme_VmPR600Xkn-FQ
# EMP1 TOKEN uBjtLDpS_J6MlPBAlGGftltOGnCcNjBQi1JGRO3sr3Q
