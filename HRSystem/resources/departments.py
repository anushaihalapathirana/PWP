import json
from jsonschema import validate, ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from flask import Response, request, url_for, Response
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import Department
from HRSystem.utils import create_error_message
from copy import copy

'''
This class contains the GET and POST method implementations for department data
'''


class DepartmentCollection(Resource):

    def get(self):
        response_data = []
        depts = Department.query.all()

        for dept in depts:
            response_data.append(dept.serialize())
        return response_data

    def post(self):

        try:
            validate(request.json, Department.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
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
        except Exception:
            return create_error_message(
                500, "Internal server Error",
                "Error while adding the department"
            )

        return Response(response={}, status=201)


'''
This class contains the GET, PUT and DELETE method implementations for a single department
'''


class DepartmentItem(Resource):

    def get(self, department):

        response_data = department.serialize()

        return response_data

    def delete(self, department):

        db.session.delete(department)
        db.session.commit()

        return Response(status=204)

    def put(self, department):
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Department.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        oldDept = copy(department)
        department.deserialize(request)
        department.id = oldDept.id
        department.department_id = oldDept.department_id

        try:
            db.session.commit()
        except Exception:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the department"
            )

        return Response(status=204)
