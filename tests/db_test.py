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
        code = "MN",
        description = "Role manager"
    )

def _get_org(name="Org1"):
    return Organization(
        name="Org1", location="oulu"
    )
    
def _get_department():
    return Department(name="dept1", description="department number one")
    
def _get_employee():
    return Employee(first_name="anusha", last_name="pathirana", address="oulu", gender="F", date_of_birth=datetime(1995, 10, 21, 11, 20, 30), appointment_date=datetime(2018, 11, 21, 11, 20, 30),
               active_emp=1, prefix_title='MISS', marritial_status='SINGLE', mobile_no='21456', basic_salary=10000, account_number="11233565456")

    
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
    
# def test_location_sensor_one_to_one(app):
#     """
#     Tests that the relationship between sensor and location is one-to-one.
#     i.e. that we cannot assign the same location for two sensors.
#     """
    
#     with app.app_context():
#         location = _get_location()
#         sensor_1 = _get_sensor(1)
#         sensor_2 = _get_sensor(2)
#         sensor_1.location = location
#         sensor_2.location = location
#         db.session.add(location)
#         db.session.add(sensor_1)
#         db.session.add(sensor_2)    
#         with pytest.raises(IntegrityError):
#             db.session.commit()
        
# def test_measurement_ondelete_sensor(app):
#     """
#     Tests that measurement's sensor foreign key is set to null when the sensor
#     is deleted.
#     """
    
#     with app.app_context():
#         measurement = _get_measurement()
#         sensor = _get_sensor()
#         measurement.sensor = sensor
#         db.session.add(measurement)
#         db.session.commit()
#         db.session.delete(sensor)
#         db.session.commit()
#         assert measurement.sensor is None
        
# def test_location_columns(app):
#     """
#     Tests the types and restrictions of location columns. Checks that numerical
#     values only accepts numbers, name must be present and is unique, and that
#     all of the columns are optional. 
#     """
    
#     with app.app_context():
#         location = _get_location()
#         location.latitude = str(location.latitude) + "°"
#         db.session.add(location)
#         with pytest.raises(StatementError):
#             db.session.commit()
            
#         db.session.rollback()
            
#         location = _get_location()
#         location.longitude = str(location.longitude) + "°"
#         db.session.add(location)
#         with pytest.raises(StatementError):
#             db.session.commit()
        
#         db.session.rollback()

#         location = _get_location()
#         location.altitude = str(location.altitude) + "m"
#         db.session.add(location)
#         with pytest.raises(StatementError):
#             db.session.commit()
        
#         db.session.rollback()
        
#         location = _get_location()
#         location.name = None
#         db.session.add(location)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
        
#         db.session.rollback()

#         location_1 = _get_location()
#         location_2 = _get_location()
#         db.session.add(location_1)
#         db.session.add(location_2)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
        
#         db.session.rollback()

#         location = Location(name="site-test")
#         db.session.add(location)
#         db.session.commit()
    
# def test_sensor_columns(app):
#     """
#     Tests sensor columns' restrictions. Name must be unique, and name and model
#     must be mandatory.
#     """

#     with app.app_context():
#         sensor_1 = _get_sensor()
#         sensor_2 = _get_sensor()
#         db.session.add(sensor_1)
#         db.session.add(sensor_2)    
#         with pytest.raises(IntegrityError):
#             db.session.commit()

#         db.session.rollback()
        
#         sensor = _get_sensor()
#         sensor.name = None
#         db.session.add(sensor)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
        
#         db.session.rollback()
        
#         sensor = _get_sensor()
#         sensor.model = None
#         db.session.add(sensor)
#         with pytest.raises(IntegrityError):
#             db.session.commit()    
    
# def test_measurement_columns(app):
#     """
#     Tests that a measurement value only accepts floating point values and that
#     time only accepts datetime values.
#     """
    
#     with app.app_context():
#         measurement = _get_measurement()
#         measurement.value = str(measurement.value) + "kg"
#         db.session.add(measurement)
#         with pytest.raises(StatementError):
#             db.session.commit()
            
#         db.session.rollback()
        
#         measurement = _get_measurement()
#         measurement.time = time.time()
#         db.session.add(measurement)
#         with pytest.raises(StatementError):
#             db.session.commit()
    
# def test_deployment_columns(app):
#     """
#     Tests that all columns in the deployment table are mandatory. Also tests
#     that start and end only accept datetime values.
#     """
    
#     with app.app_context():
#         # Tests for nullable
#         deployment = _get_deployment()
#         deployment.start = None
#         db.session.add(deployment)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
        
#         db.session.rollback()

#         deployment = _get_deployment()
#         deployment.end = None
#         db.session.add(deployment)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
        
#         db.session.rollback()

#         deployment = _get_deployment()
#         deployment.name = None
#         db.session.add(deployment)
#         with pytest.raises(IntegrityError):
#             db.session.commit()
        
#         db.session.rollback()
            
#         # Tests for column type
#         deployment = _get_deployment()
#         deployment.start = time.time()
#         db.session.add(deployment)
#         with pytest.raises(StatementError):
#             db.session.commit()
        
#         db.session.rollback()
        
#         deployment = _get_deployment()
#         deployment.end = time.time()
#         db.session.add(deployment)
#         with pytest.raises(StatementError):
#             db.session.commit()
    
#         db.session.rollback()
