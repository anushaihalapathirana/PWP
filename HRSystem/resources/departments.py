"""
    This resource file contains the department related REST calls implementation
"""
from copy import copy
from jsonschema import validate, ValidationError
from flask import Response, request
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from HRSystem import db
from HRSystem.models import Department
from HRSystem.utils import create_error_message
from HRSystem.utils import require_admin

class DepartmentCollection(Resource):

    """ This class contains the GET and POST method implementations for department data
        Arguments:
        Returns:
        Endpoint: /api/departments/
    """
    @classmethod
    @require_admin
    def get(cls):
        """ GET list of departments
            Arguments:
            Returns:
                List of departments
            responses:
                '200':
                description: The departments retrieve successfully
        """
        response_data = []
        depts = Department.query.all()

        for dept in depts:
            response_data.append(dept.serialize())
        return response_data

    @classmethod
    @require_admin
    def post(cls):
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

        return Response(response={}, status=201)


class DepartmentItem(Resource):

    """ This class contains the GET, PUT and DELETE method implementations for a single department
        Arguments:
        Returns:
        Endpoint: /api/departments/<Department:department>/
    """
    @classmethod
    @require_admin
    def get(cls, department):
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
        response_data = department.serialize()

        return response_data

    @classmethod
    @require_admin
    def delete(cls, department):
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

        return Response(status=204)

    @classmethod
    @require_admin
    def put(cls, department):
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

        return Response(status=204)
