"""
    This resource file contains the department related REST calls implementation
"""
import json
from copy import copy
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from hr_system import db
from hr_system.models import Department
from hr_system.utils import create_error_message
from hr_system.utils import require_admin, HRSystemBuilder
from hr_system.constants import *


class DepartmentCollection(Resource):

    """ This class contains the GET and POST method implementations for department data
        Arguments:
        Returns:
        Endpoint: /api/departments/
    """
    @require_admin
    def get(self):
        """ GET list of departments
            Arguments:
            Returns:
                List of departments
            responses:
                '200':
                description: The departments retrieve successfully
        """
        body = HRSystemBuilder()
        body.add_namespace('hrsys', LINK_RELATIONS_URL)
        body.add_control('self', url_for("api.departmentcollection"))
        body.add_control_add_department()
        body.add_control_get_employee_all()
        body["items"] = []

        depts = Department.query.all()

        for dept in depts:
            item = HRSystemBuilder(dept.serialize())
            item.add_control("self", url_for(
                "api.departmentitem", department=dept))
            item.add_control("profile", DEPARTMENT_COLLECTION_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

    @require_admin
    def post(self):
        """ Create a new department
        Arguments:
            request:
                name: abc
                description: deptartment of tech
                department_id: D01
        Returns:
            responses:
                '201':
                description: The department was created successfully
                '400':
                description: The request body was not valid
                '409':
                description: A department with the same id already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            validate(request.json, Department.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            db_dept = Department.query.filter_by(
                department_id=request.json["department_id"]).first()
            if db_dept is not None:
                return create_error_message(
                    409, "Already Exist",
                    "Department id is already exist"
                )
            dept = Department()
            dept.deserialize(request)

            db.session.add(dept)
            db.session.commit()

            location = url_for("api.departmentitem", department=dept)
        except (Exception, RuntimeError) as error:
            print("error", error)
            if isinstance(error, HTTPException):
                return create_error_message(
                    409, "Already Exist",
                    "Department id is already exist"
                )
            return create_error_message(
                500, "Internal Server Error",
                "Internal Server Error occurred!"
            )

        return Response(response={}, status=201, headers={
            "Location": location
        }, mimetype=MASON)


class DepartmentItem(Resource):

    """ This class contains the GET, PUT and DELETE method implementations for a single department
        Arguments:
        Returns:
        Endpoint: /api/departments/<Department:department>/
    """
    @require_admin
    def get(self, department):
        """ get details of one department
        Arguments:
            department
        Returns:
            Response
                '200':
                description: Data of list of department
                '404':
                description: The department was not found
        """
        body = HRSystemBuilder(department.serialize())
        body.add_namespace('hrsys', LINK_RELATIONS_URL)
        body.add_control('self', url_for(
            "api.departmentitem", department=department))
        body.add_control("profile", DEPARTMENT_ITEM_PROFILE)
        body.add_control("collection", url_for("api.departmentcollection"))
        body.add_control_delete_department(department)
        body.add_control_modify_department(department)
        return Response(json.dumps(body), status=200, mimetype=MASON)

    @require_admin
    def delete(self, department):
        """ Delete the selected department
        Arguments:
            department
        Returns:
            responses:
                '204':
                    description: The department was successfully deleted
                '404':
                    description: The department was not found
        """
        db.session.delete(department)
        db.session.commit()

        return Response(status=204, mimetype=MASON)

    @require_admin
    def put(self, department):
        """ Replace department's basic data with new values
        Arguments:
            department
        Returns:
            responses:
                '204':
                description: The department's attributes were updated successfully
                '400':
                description: The request body was not valid
                '404':
                description: The department was not found
                '409':
                description: A department with the same name already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Department.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        old_dept = copy(department)
        department.deserialize(request)
        department.id = old_dept.id
        department.department_id = old_dept.department_id

        try:
            db.session.commit()
        except (Exception, RuntimeError):
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the department"
            )

        return Response(status=204, mimetype=MASON)
