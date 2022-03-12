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
    This class contains the GET, POST method implementations for
        leave plan of employees by providing employee id

    Endpoint: /api/employees/<Employee:employee>/leaveplans/

    """

    @classmethod
    def get(cls, employee=None):
        """ GET list of leaves of given employee
            Arguments: Employee id
            Returns:
                List of leaves
            responses:
                '200':
                description: The leaves retrieve successfully
        """
        leaveplan_response = []
        leaves = []

        leaves = LeavePlan.query.join(LeavePlan.employee).filter(
            LeavePlan.employee == employee
        )

        for leave in leaves:
            leaveplan_response.append(leave.serialize())

        return leaveplan_response

    @classmethod
    def post(cls, employee):
        """ Create a new leave
        Arguments:
            employee
            request:
                leave_type: CASUAL
                reason: fever
                leave_date: 1998-08-25T11:20:30
        Returns:
            responses:
                '201':
                description: The leave was created successfully
                '400':
                description: The request body was not valid
                '409':
                description: A leave with the same id already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Invalid JSON document",
                "JSON format is not valid"
            )
        try:
            validate(request.json, LeavePlan.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            leaveplan = LeavePlan()
            leaveplan.deserialize(request)

            leaveplan.employee = employee

            db.session.add(leaveplan)
            db.session.commit()
        except (Exception, ):
            return create_error_message(
                500, "Internal server Error",
                "Error while adding the leave"
            )
        return Response(response={}, status=201)


class LeavePlanItem(Resource):
    """ This class contains the PUT and DELETE method implementations for a single leave
        Arguments:
        Returns:
        Endpoint: /api/leaveplans/<LeavePlan:leaveplan>/
    """

    @classmethod
    def put(cls, leaveplan):
        """ Replace leaveplan's basic data with new values
        Arguments:
            leaveplan
        Returns:
            responses:
                '204':
                description: The leaveplan's attributes were updated successfully
                '400':
                description: The request body was not valid
                '404':
                description: The leaveplan was not found
                '409':
                description: A leaveplan with the same name already exists
                '415':
                description: Wrong media type was used
        """
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

        old_Leave_Plan = copy(leaveplan)
        leaveplan.deserialize(request)
        leaveplan.id = old_Leave_Plan.id

        try:
            db.session.commit()
        except (Exception, ):
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the employee"
            )

        return Response(status=204)

    @classmethod
    def delete(cls, leaveplan):
        """ Delete the selected leaveplan
        Arguments:
            leaveplan
        Returns:
            responses:
                '204':
                    description: The leaveplan was successfully deleted
                '404':
                    description: The leaveplan was not found
        """
        db.session.delete(leaveplan)
        db.session.commit()

        return Response(status=204)
