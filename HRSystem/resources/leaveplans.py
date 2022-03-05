"""
    This resource file contains the leaves related REST calls implementation
"""
from copy import copy
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask import Response, request
from HRSystem import db
from HRSystem.utils import create_error_message
from HRSystem.models import LeavePlan

class LeavePlanByEmployeellection(Resource):
    """
    This class contains the GET, POST method implementations for leave plan of employees by providing employee id
    """
    def get(self, employee=None):
        """ GET list of leaves
            Arguments:
            Returns:
                List
        """
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
        """ POST leave
        Arguments:
            request
        Returns:
            Response
        """
        try:
            validate(request.json, LeavePlan.get_schema())
        except ValidationError:
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
        except Exception:
            return create_error_message(
                500, "Internal Server error",
                "Cannot create a leave plan"
            )
        return Response(response={}, status=201)


class LeavePlanItem(Resource):
    """ This class contains the PUT and DELETE method implementations for a single leave
        Arguments:
        Returns:
    """
    def put(self, leaveplan):
        """ PUT departments
        Arguments:
            department
        Returns:
            Response
        """
        if leaveplan is None:
            return create_error_message(
                404, "Not found",
                "Leave plan not found"
            )

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, LeavePlan.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        oldLeavePlan = copy(leaveplan)
        leaveplan.deserialize(request)
        leaveplan.id = oldLeavePlan.id

        try:
            db.session.commit()
        except Exception:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the employee"
            )

        return Response(status=204)

    def delete(self, leaveplan):
        """ DELETE departments
        Arguments:
            department
        Returns:
            Response
        """
        db.session.delete(leaveplan)
        db.session.commit()

        return Response(status=204)
