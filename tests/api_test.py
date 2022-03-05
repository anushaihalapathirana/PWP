import json
import os
import pytest
import tempfile
import time
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
def app():
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
    db.session.commit()

def _get_role_json(number=10):
    """
    Creates a valid role JSON object to be used for PUT and POST tests.
    """
    
    return {"name": "role-{}".format(number), "model": "role new"}

    
class TestSensorCollection(object):
    
    RESOURCE_URL = "/api/roles/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        print("----------------------")
        print(resp)

        assert resp.status_code == 200
        body = json.loads(resp.data)
        # _check_namespace(client, body)
        # _check_control_post_method("senhub:add-sensor", client, body)
        assert len(body["items"]) == 3
        # for item in body["items"]:
        #     _check_control_get_method("self", client, item)
        #     _check_control_get_method("profile", client, item)

#     def test_post(self, client):
#         valid = _get_sensor_json()
        
#         # test with wrong content type
#         resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
#         assert resp.status_code == 415
        
#         # test with valid and see that it exists afterward
#         resp = client.post(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 201
#         assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
#         resp = client.get(resp.headers["Location"])
#         assert resp.status_code == 200
        
#         # send same data again for 409
#         resp = client.post(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 409
        
#         # remove model field for 400
#         valid.pop("model")
#         resp = client.post(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 400
        
        
# class TestSensorItem(object):
    
#     RESOURCE_URL = "/api/sensors/test-sensor-1/"
#     INVALID_URL = "/api/sensors/non-sensor-x/"
    
#     def test_get(self, client):
#         resp = client.get(self.RESOURCE_URL)
#         assert resp.status_code == 200
#         body = json.loads(resp.data)
#         _check_namespace(client, body)
#         _check_control_get_method("profile", client, body)
#         _check_control_get_method("collection", client, body)
#         _check_control_put_method("edit", client, body)
#         _check_control_delete_method("senhub:delete", client, body)
#         resp = client.get(self.INVALID_URL)
#         assert resp.status_code == 404

#     def test_put(self, client):
#         valid = _get_sensor_json()
        
#         # test with wrong content type
#         resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
#         assert resp.status_code == 415
        
#         resp = client.put(self.INVALID_URL, json=valid)
#         assert resp.status_code == 404
        
#         # test with another sensor's name
#         valid["name"] = "test-sensor-2"
#         resp = client.put(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 409
        
#         # test with valid (only change model)
#         valid["name"] = "test-sensor-1"
#         resp = client.put(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 204
        
#         # remove field for 400
#         valid.pop("model")
#         resp = client.put(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 400
        
#     def test_delete(self, client):
#         resp = client.delete(self.RESOURCE_URL)
#         assert resp.status_code == 204
#         resp = client.delete(self.RESOURCE_URL)
#         assert resp.status_code == 404
#         resp = client.delete(self.INVALID_URL)
#         assert resp.status_code == 404
        
        
        
        
        
        
        
        
        
        
        
    
    

    

        
            
    