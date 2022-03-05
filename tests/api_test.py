import json
import os
import secrets
import pytest
import tempfile
import time
import base64
from datetime import datetime
from jsonschema import validate
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
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        _populate_db()
        
    yield app.test_client()
    
    os.close(db_fd)
    os.unlink(db_fname)


def _populate_db():
    for i in range(1, 4):
        role = Role(name="Role-{}".format(i),
            code="Code-{}".format(i), 
            description="test roles")
        db.session.add(role)

        org = Organization(organization_id = "O0{}".format(i),
         name="org-{}".format(i), 
         location="location-{}".format(i)
        )
        db.session.add(org)

        dept = Department(department_id = "D0{}".format(i),
         name="dept-{}".format(i), 
         description="description-{}".format(i)
        )
        db.session.add(dept)

        employee = Employee(employee_id = "00{}".format(i), first_name="test{}".format(i),
                last_name="lastname-{}".format(i),
                address="oulu", gender="F", date_of_birth=datetime(1995, 10, 21, 11, 20, 30),
                appointment_date=datetime(2018, 11, 21, 11, 20, 30),
                active_emp=1, prefix_title='MISS', marritial_status='SINGLE',
                mobile_no='21456', basic_salary=10000, account_number="11233565456",
                role=role, organization=org, department=dept)
        db.session.add(employee)

        leave = LeavePlan(leave_type='MEDICAL', leave_date=datetime(
                        2018, 11, 21, 11, 20, 30), employee=employee)
        db.session.add(leave)

    token = secrets.token_urlsafe()
    db_key = ApiKey(key=ApiKey.key_hash(token),admin=True)
    db.session.add(db_key)

        
    db.session.commit()

def _get_role_json(number=10):
    """
    Creates a valid role JSON object to be used for POST tests.
    """
    return {"name": "role-{}".format(number), "code": "Code-5", "description":"new role"}

def _get_role_json_put(number=10):
    """
    Creates a valid role JSON object to be used for PUT tests.
    """
    return {"name": "role-{}".format(number), "code": "Code-2", "description":"new role"}

def _get_org_json():
    """
    Creates a valid role JSON object to be used for POST tests.
    """
    return {"organization_id": "O05", "name": "org-5", "location":"location-5"}

def _get_org_json_put():
    """
    Creates a valid role JSON object to be used for PUT tests.
    """
    return {"organization_id": "O01", "name": "org-new", "location":"location-1"}

def _get_dept_json():
    """
    Creates a valid role JSON object to be used for POST tests.
    """
    return {"department_id": "D05", "name": "dept-5", "description":"department-5"}

def _get_dept_json_put():
    """
    Creates a valid role JSON object to be used for PUT tests.
    """
    return {"department_id": "D01", "name": "dept-new", "description":"department 1"}

def _get_employee_json():
    """
    Creates a valid role JSON object to be used for POST tests.
    """
    return {
    "employee_id":"005",
    "first_name":"Sameera123", 
    "last_name":"pathirana222",
    "address":"oulu",
    "gender":"F", 
    "date_of_birth":"1991-11-13T20:20:39+00:00", 
    "appointment_date":"2018-11-13T20:20:39+00:00",
    "active_emp":1, 
    "mobile_no":"21456", 
    "basic_salary":10000, 
    "account_number":"11233565456"
}

def _get_employee_json_put():
    """
    Creates a valid role JSON object to be used for PUT tests.
    """
    return {
    "employee_id":"001",
    "first_name":"Sameera123", 
    "last_name":"pathirana222",
    "address":"oulu",
    "gender":"F", 
    "date_of_birth":"1991-11-13T20:20:39+00:00", 
    "appointment_date":"2018-11-13T20:20:39+00:00",
    "active_emp":1, 
    "mobile_no":"21456", 
    "basic_salary":10000, 
    "account_number":"11233565456"
}

def _get_leave_json():
    """
    Creates a valid role JSON object to be used for POST tests.
    """
    return {"leave_type": "MEDICAL", "reason":"sick", "leave_date": "2018-11-13T20:20:39+00:00"}

def _get_leave_json_put():
    """
    Creates a valid role JSON object to be used for PUT tests.
    """
    return {"id":1,"leave_type": "CASUAL", "reason":"sick", "leave_date": "2018-11-13T20:20:39+00:00"}

class TestRoleCollection(object):
    
    RESOURCE_URL = "/api/roles/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3

    def test_post(self, client):
        valid = _get_role_json()  
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        
        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove model field for 400
        valid.pop("name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestRoleItem(object):
    
    RESOURCE_URL = "/api/roles/Code-2/"
    INVALID_URL = "/api/roles/role-ne/"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        valid = _get_role_json_put()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with valid (only change model)
        valid["description"] = "new code"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405
        
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
        
        
class TestOrganizationCollection(object):
    
    RESOURCE_URL = "/api/organizations/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3

    def test_post(self, client):
        valid = _get_org_json()  
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        
        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove model field for 400
        valid.pop("name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
         

class TestOranizationItem(object):
    
    RESOURCE_URL = "/api/organizations/O01/"
    INVALID_URL = "/api/organizations/org-new/"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        valid = _get_org_json_put()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with valid (only change model)
        valid["location"] = "put method location update"
        print(valid)
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405
        
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

class TestDepartmentCollection(object):
    
    RESOURCE_URL = "/api/departments/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3

    def test_post(self, client):
        valid = _get_dept_json()  
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        
        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove model field for 400
        valid.pop("name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
         

class TestDepartmentItem(object):
    
    RESOURCE_URL = "/api/departments/D01/"
    INVALID_URL = "/api/departments/dept-new/"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        valid = _get_dept_json_put()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with valid (only change model)
        valid["location"] = "put method location update"
        print(valid)
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405
        
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404


class TestEmployeeByRlationCollection(object):
    
    RESOURCE_URL = "/api/employees/"
    RESOURCE_URL_1 = "/api/organizations/O01/roles/Code-1/employees/"
    RESOURCE_URL_2 = "/api/organizations/O01/employees/"
    RESOURCE_URL_3 = "/api/organizations/O01/departments/D01/employees/"
    RESOURCE_URL_4 = "/api/organizations/O01/departments/D01/roles/Code-1/employees/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL, headers={"HRSystem-Api-Key": "aCO8xWKY2qGN3wQVPPqUao44Y9w4w8bfc4HlHu8j-3M"})
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3
    
    def test_get_by_role(self, client):
        resp = client.get(self.RESOURCE_URL_1, headers={"HRSystem-Api-Key": "aCO8xWKY2qGN3wQVPPqUao44Y9w4w8bfc4HlHu8j-3M"})
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 1
    
    def test_get_by_org(self, client):
        resp = client.get(self.RESOURCE_URL_2, headers={"HRSystem-Api-Key": "aCO8xWKY2qGN3wQVPPqUao44Y9w4w8bfc4HlHu8j-3M"})
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 1
    
    def test_get_by_dept(self, client):
        resp = client.get(self.RESOURCE_URL_3, headers={"HRSystem-Api-Key": "aCO8xWKY2qGN3wQVPPqUao44Y9w4w8bfc4HlHu8j-3M"})
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 1
    
    def test_get_by_all(self, client):
        resp = client.get(self.RESOURCE_URL_4, headers={"HRSystem-Api-Key": "aCO8xWKY2qGN3wQVPPqUao44Y9w4w8bfc4HlHu8j-3M"})
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 1

class TestEmployeeCollection(object):
    
    RESOURCE_URL = "/api/organizations/O01/departments/D01/roles/Code-1/employees/"

    def test_post(self, client):
        valid = _get_employee_json()  
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        
        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove model field for 400
        valid.pop("first_name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

         
class TestEmployeeItem(object):
    
    RESOURCE_URL = "/api/employees/001/"
    INVALID_URL = "/api/employees/new/"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        valid = _get_employee_json_put()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with valid (only change model)
        valid["first_name"] = "name changed in put"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("last_name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405
        
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

class TestLeavePlanByEmployeellection(object):
    
    RESOURCE_URL = "/api/employees/001/leaveplans/"
    ERROR_URL = "/api/employees/071/leaveplans/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 1

        resp = client.get(self.ERROR_URL)
        assert resp.status_code == 404


    def test_post(self, client):
        valid = _get_leave_json()  
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        
        # remove model field for 400
        valid.pop("leave_type")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestLeavePlanItem(object):
    
    RESOURCE_URL = "/api/leaveplans/1/"
    INVALID_URL = "/api/leaveplans/new/"
    
    def test_put(self, client):
        valid = _get_leave_json_put()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with valid (only change model)
        valid["leave_type"] = "UNPAID"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("leave_type")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405

    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
