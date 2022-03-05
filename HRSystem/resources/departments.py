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


class DepartmentCollection(Resource):

    """ This class contains the GET and POST method implementations for department data
        Arguments:
        Returns:
    """
    def get(self):
        """ GET list of departments
            Arguments:
            Returns:
                List
        """
        response_data = []
        depts = Department.query.all()

        for dept in depts:
            response_data.append(dept.serialize())
        return response_data

    def post(self):
        """ POST departments
        Arguments:
            request
        Returns:
            Response
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
        except Exception as error:
            if isinstance (error, HTTPException):
                return create_error_message(
                    409, "Already Exist",
                    "Department id is already exist"
                )

        return Response(response={}, status=201)


class DepartmentItem(Resource):

    """ This class contains the GET, PUT and DELETE method implementations for a single department
        Arguments:
        Returns:
    """

    def get(self, department):
        """ GET departments
        Arguments:
            department
        Returns:
            Response
        """
        response_data = department.serialize()

        return response_data

    def delete(self, department):
        """ DELETE departments
        Arguments:
            department
        Returns:
            Response
        """
        db.session.delete(department)
        db.session.commit()

        return Response(status=204)


    def put(self, department):
        """ PUT departments
        Arguments:
            department
        Returns:
            Response
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
        except Exception: return create_error_message(
                500, "Internal server Error",
                "Error while updating the department"
            )

        return Response(status=204)
