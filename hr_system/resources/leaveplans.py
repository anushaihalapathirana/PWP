"""
    This resource file contains the leaves related REST calls implementation
"""
import json
from copy import copy
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from hr_system import db
from hr_system.utils import create_error_message, HRSystemBuilder
from hr_system.models import LeavePlan
from hr_system.constants import *


class LeavePlanByEmployeellection(Resource):
    """
    This class contains the GET, POST method implementations for
        leave plan of employees by providing employee id

    Endpoint: /api/employees/<Employee:employee>/leaveplans/

    """

    def get(self, employee=None):
        """ GET list of leaves of given employee
            Arguments: Employee id
            Returns:
                List of leaves
            responses:
                '200':
                description: The leaves retrieve successfully
        """

        body = HRSystemBuilder()
        body.add_namespace('hrsys', LINK_RELATIONS_URL)
        body.add_control('self', url_for(
            "api.leaveplanbyemployeellection", employee=employee))
        body.add_control_add_leave(employee)
        body["items"] = []

        leaves = []

        leaves = LeavePlan.query.join(LeavePlan.employee).filter(
            LeavePlan.employee == employee
        )

        for leave in leaves:
            item = HRSystemBuilder(
                leave.serialize()
            )
            item.add_control("self", url_for(
                "api.leaveplanitem", employee=employee, leaveplan=leave))
            item.add_control("profile", HRSYSTEM_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self, employee):
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
            location = url_for("api.leaveplanitem", leaveplan=leaveplan, employee = employee)
        except Exception as e:
            print(e)
            return create_error_message(
                500, "Internal server Error",
                "Error while adding the leave"
            )
        return Response(response={}, status=201, headers={
            "Location": location
        }, mimetype=MASON)


class LeavePlanItem(Resource):
    """ This class contains the PUT and DELETE method implementations for a single leave
        Arguments:
        Returns:
        Endpoint: /api/employees/<Employee:employee>/leaveplans/<LeavePlan:leaveplan>/
    """

    def get(self, employee, leaveplan):
        """ get details of one leaveplan for an employee
        Arguments:
            employee
            role
        Returns:
            Response
                '200':
                description: Data of leaveplan
                '404':
                description: The leaveplan is not found
        """

        if leaveplan.employee_id != employee.id:
            return create_error_message(400, "Unable to find corrosponding leaveplan")
        response_data = leaveplan.serialize()
        body = HRSystemBuilder(
            response_data
        )
        body.add_namespace("hrsys", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.leaveplanitem",
                         leaveplan=leaveplan, employee=employee))
        body.add_control("profile", HRSYSTEM_PROFILE)
        body.add_control("collection", url_for(
            "api.leaveplanbyemployeellection", employee=employee))
        body.add_control_modify_leave(emp=employee, leave=leaveplan)
        body.add_control_delete_leave(emp=employee, leave=leaveplan)
        body.add_control_get_employee(employee=employee)
        return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, employee, leaveplan):
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
        leave = LeavePlan.query.filter_by(id=leaveplan.id).first()

        if (leave.employee_id != employee.id):
            return create_error_message(
                400, "Bad request",
                "Unable to find corrosponding leaveplan"
            )

        old_leave_plan = copy(leaveplan)
        leaveplan.deserialize(request)
        leaveplan.id = old_leave_plan.id

        try:
            db.session.commit()
        except (Exception, ):
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the employee"
            )

        return Response(status=204, mimetype=MASON)

    def delete(self, employee, leaveplan):
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
        leave = LeavePlan.query.filter_by(id=leaveplan.id).first()
        if (leave.employee_id != employee.id):
            return create_error_message(
                400, "Bad request",
                "Unable to find corrosponding leaveplan"
            )
        db.session.delete(leaveplan)
        db.session.commit()

        return Response(status=204, mimetype=MASON)
