
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import LeavePlan, Employee
from jsonschema import validate, ValidationError
from flask import Response, request, url_for, Response
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from HRSystem.utils import create_error_message
from copy import copy

'''
This class contains the GET, POST method implementations for leave plan of employees by providing employee id
                
'''


class LeavePlanByEmployeellection(Resource):

    def get(self, employee=None):

        leaveplan_response = []
        leaves = []

        if employee is not None:
            leaves = LeavePlan.query.join(LeavePlan.employee).filter(
                LeavePlan.employee == employee
            )
        else:
            return create_error_message(
                404, "Not found",
                "Employee is not found"
            )

        for leave in leaves:
            leaveplan_response.append(leave.serialize())

        return leaveplan_response

    def post(self, employee):
        try:
            validate(request.json, LeavePlan.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            leaveplan = LeavePlan()
            leaveplan.deserialize(request)

            leaveplan.employee = employee

            db.session.add(leaveplan)
            db.session.commit()
        except Exception as e:
            print(e)
            return create_error_message(
                500, "Internal Server error",
                "Cannot create a leave plan"
            )
        return Response(response={}, status=201)


class LeavePlanItem(Resource):

    def put(self, leaveplan):

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, LeavePlan.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        oldLeavePlan = copy(leaveplan)
        leaveplan.deserialize(request)
        leaveplan.id = oldLeavePlan.id

        try:
            db.session.commit()
        except Exception as e:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the employee"
            )

        return Response(status=204)

    def delete(self, leaveplan):

        db.session.delete(leaveplan)
        db.session.commit()

        return Response(status=204)
