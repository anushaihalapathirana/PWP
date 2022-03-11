# run command python3 -m pytest

import os
import pytest
import tempfile
import time
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError
from HRSystem import create_app, db
from HRSystem.models import *

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        
    yield app
    
    os.close(db_fd)
    os.unlink(db_fname)

def _get_role(rolecode="MN"):
    return Role(
        name = "Manager",
        code = rolecode,
        description = "Role manager"
    )

def _get_org(organization_id="O001"):
    return Organization(
        organization_id = organization_id,
        name="Org1", 
        location="oulu"
    )
    
def _get_department(department_id="D01"):
    return Department(
        department_id=department_id,
        name="dept1", 
        description="department number one")
    
def _get_employee(employee_id="001"):
    return Employee(employee_id = employee_id, first_name="anusha", last_name="pathirana",
                address="oulu", gender="F", date_of_birth=datetime(1995, 10, 21, 11, 20, 30),
                appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                active_emp=1, prefix_title='MISS', marritial_status='SINGLE',
                mobile_no='21456', basic_salary=10000, account_number="11233565456")

def _get_leave():
    return LeavePlan(
        leave_type = 'CASUAL',
        reason = "sick",
        leave_date = datetime(2018, 11, 21, 11, 20, 30)
    )
    
def test_create_instances(app):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns. After creation, test that 
    everything can be found from database, and that all relationships have been
    saved correctly.
    """
    
    with app.app_context():
        # Create everything
        role = _get_role()
        organization = _get_org()
        department = _get_department()
        employee = _get_employee()

        employee.organization = organization
        employee.role = role
        employee.department = department
        db.session.add(employee)

        db.session.commit()
        
        # Check that everything exists
        assert Employee.query.count() == 1
        assert Role.query.count() == 1
        assert Department.query.count() == 1
        assert Organization.query.count() == 1
        db_employee = Employee.query.first()
        db_role = Role.query.first()
        db_organization = Organization.query.first()
        db_department = Department.query.first()
        
        # Check all relationships (both sides)
        assert db_employee.role == db_role
        assert db_employee.organization == db_organization
        assert db_employee.department == db_department
    
def test_employee_organization_one_to_many(app):
    """
    Tests that the relationship between employee and organization is one-to-many.
    i.e. that we can assign the same organization for two employees.
    """
    
    with app.app_context():
        organization1 = _get_org()
        emp1 = _get_employee("002")
        emp2 = _get_employee("003")
        emp1.organization = organization1
        emp2.organization = organization1
        db.session.add(organization1)
        db.session.add(emp1)
        db.session.add(emp2)
        db.session.commit()

        assert Employee.query.count() == 2
        assert Organization.query.count() == 1
        
def test_employee_role_one_to_many(app):
    """
    Tests that the relationship between employee and role is one-to-many.
    i.e. that we can assign the same role for two employees.
    """
    
    with app.app_context():
        role = _get_role()
        emp1 = _get_employee("002")
        emp2 = _get_employee("003")
        emp1.role = role
        emp2.role = role
        db.session.add(role)
        db.session.add(emp1)
        db.session.add(emp2)
        db.session.commit()

        assert Employee.query.count() == 2
        assert role.query.count() == 1

def test_employee_department_one_to_many(app):
    """
    Tests that the relationship between employee and department is one-to-many.
    i.e. that we can assign the same department for two employees.
    """
    
    with app.app_context():
        department = _get_department()
        emp1 = _get_employee("002")
        emp2 = _get_employee("003")
        emp1.department = department
        emp2.department = department
        db.session.add(department)
        db.session.add(emp1)
        db.session.add(emp2)
        db.session.commit()

        assert Employee.query.count() == 2
        assert Department.query.count() == 1

def test_emp_ondelete_organization(app):
    """
    Tests that employee's organization foreign key is set to null when the employee
    is deleted.
    """
    
    with app.app_context():
        organization = _get_org()
        emp = _get_employee()
        emp.Organization = organization
        db.session.add(emp)
        db.session.add(organization)
        db.session.commit()
        db.session.delete(organization)
        db.session.commit()
        assert emp.organization is None

def test_emp_ondelete_department(app):
    """
    Tests that employee's department foreign key is set to null when the employee
    is deleted.
    """
    
    with app.app_context():
        department = _get_department()
        emp = _get_employee()
        emp.Department = department
        db.session.add(emp)
        db.session.add(department)
        db.session.commit()
        db.session.delete(department)
        db.session.commit()
        assert emp.department is None

def test_measurement_ondelete_role(app):
    """
    Tests that employee's role foreign key is set to null when the employee
    is deleted.
    """
    
    with app.app_context():
        role = _get_role()
        emp = _get_employee()
        emp.Role = role
        db.session.add(emp)
        db.session.add(role)
        db.session.commit()
        db.session.delete(role)
        db.session.commit()
        assert emp.role is None
        
def test_role_columns(app):
    """
    Tests the types and restrictions of role columns. Checks that numerical
    values only accepts numbers, name must be present and is unique, and that
    all of the columns are optional. 
    """
    
    with app.app_context():
        
        role = _get_role()
        role.code = None
        db.session.add(role)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
    
        role = _get_role()
        role.name = None
        db.session.add(role)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        role_1 = _get_role()
        role_2 = _get_role()
        db.session.add(role_1)
        db.session.add(role_2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        role = Role(name="test", code="TEST")
        db.session.add(role)
        db.session.commit()
    
def test_department_columns(app):
    """
    Tests the types and restrictions of department columns. Checks that numerical
    values only accepts numbers, name must be present and is unique, and that
    all of the columns are optional. 
    """
    
    with app.app_context():
        
        department = _get_department()
        department.department_id = None
        db.session.add(department)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
    
        department = _get_department()
        department.name = None
        db.session.add(department)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        department_1 = _get_department()
        department_2 = _get_department()
        db.session.add(department_1)
        db.session.add(department_2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        department = Department(name="test", department_id="D03")
        db.session.add(department)
        db.session.commit()

def test_Org_columns(app):
    """
    Tests the types and restrictions of organization columns. Checks that numerical
    values only accepts numbers, name must be present and is unique, and that
    all of the columns are optional. 
    """
    
    with app.app_context():
        
        organization = _get_org()
        organization.organization_id = None
        db.session.add(organization)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
    
        organization = _get_org()
        organization.name = None
        db.session.add(organization)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        organization = _get_org()
        organization.location = None
        db.session.add(organization)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        org_1 = _get_org()
        org_2 = _get_org()
        db.session.add(org_1)
        db.session.add(org_2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        organization = Organization(name="test", organization_id="O03", location="oulu")
        db.session.add(organization)
        db.session.commit()

def test_emp_columns(app):
    """
    Tests the types and restrictions of employee columns. Checks that numerical
    values only accepts numbers, name must be present and is unique, and that
    all of the columns are optional. 
    """
    
    with app.app_context():

        emp = _get_employee()
        emp.appointment_date = ""
        db.session.add(emp)
        with pytest.raises(StatementError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.date_of_birth = ""
        db.session.add(emp)
        with pytest.raises(StatementError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.employee_id = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()
    
        emp = _get_employee()
        emp.first_name = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.last_name = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.address = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.gender = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.appointment_date = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.mobile_no = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.basic_salary = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp = _get_employee()
        emp.account_number = None
        db.session.add(emp)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

        emp1 = _get_employee()
        emp2 = _get_employee()
        db.session.add(emp1)
        db.session.add(emp2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        emp = Employee(employee_id = '001', first_name="anusha", last_name="pathirana",
                address="oulu", gender="F", date_of_birth=datetime(1995, 10, 21, 11, 20, 30),
                appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                active_emp=1, prefix_title='MISS', marritial_status='SINGLE',
                mobile_no='21456', basic_salary=10000, account_number="11233565456")
        db.session.add(emp)
        db.session.commit()

def test_leave_columns(app):
    """
    Tests the types and restrictions of leave plan columns. Checks that numerical
    values only accepts numbers, name must be present and is unique, and that
    all of the columns are optional. 
    """
    
    with app.app_context():
        
        leave = _get_leave()
        leave.leave_date = ""
        db.session.add(leave)
        with pytest.raises(StatementError):
            db.session.commit()
        
        db.session.rollback()
    
        leave = _get_leave()
        leave.leave_type = None
        db.session.add(leave)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        leave = _get_leave()
        leave.leave_date = None
        db.session.add(leave)
        with pytest.raises(IntegrityError):
            db.session.commit()        
        db.session.rollback()

        leave = LeavePlan(leave_type='MEDICAL', leave_date=datetime(2018, 11, 21, 11, 20, 30))
        db.session.add(leave)
        db.session.commit()