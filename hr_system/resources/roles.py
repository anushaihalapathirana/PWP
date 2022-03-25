"""
    This resource file contains the role related REST calls implementation
"""
import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from hr_system import db
from hr_system.models import Role
from hr_system.utils import create_error_message, HRSystemBuilder
from hr_system.utils import require_admin
from hr_system.constants import *

class RoleCollection(Resource):
    """ This class contains the GET and POST method implementations for role data
        Arguments:
        Returns:
        Endpoint: /api/roles/
    """
    @require_admin
    def get(self):
        """ GET list of roles
            Arguments:
            Returns:
                List of roles
            responses:
                '200':
                description: The Roles retrieve successfully
        """

        body = HRSystemBuilder()
        body.add_namespace('hrsys', LINK_RELATIONS_URL)
        body.add_control('self', url_for("api.rolecollection"))
        body.add_control_get_roles()
        body["item"] = []

        roles = Role.query.all()

        for role in roles:
            item = HRSystemBuilder(
                role.serialize()
            )
            item.add_control("self", url_for("api.roleitem", role = role))
            item.add_control("profile", HRSYSTEM_PROFILE)
            body["item"].append(item)
        return Response(json.dumps(body), 200, mimetype=MASON)


    @require_admin
    def post(self):
        """ Create a new Role
        Arguments:
            request:
                name: Manager
                code: MAN
                description: Manager role
        Returns:
            responses:
                '201':
                description: The Role was created successfully
                '400':
                description: The request body was not valid
                '409':
                description: A role with the same code already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Role.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            db_role = Role.query.filter_by(code=request.json["code"]).first()
            if db_role is not None:
                return create_error_message(
                    409, "Already Exist",
                    "Department id is already exist"
                )
            role = Role()
            role.deserialize(request)
            db.session.add(role)
            db.session.commit()
        except Exception as error:
            if isinstance(error, HTTPException):
                return create_error_message(
                    409, "Already Exist",
                    "role code is already exist"
                )
            return create_error_message(
                500, "Internal Server Error",
                "Internal Server Error occurred!"
            )
        return Response(response={}, status=201)


class RoleItem(Resource):
    """ This class contains the GET, PUT and DELETE method implementations for a single role
        Arguments:
        Returns:
        Endpoint - /api/roles/<role>
    """
    @require_admin
    def get(self, role):
        """ get details of one role
        Arguments:
            role
        Returns:
            Response
                '200':
                description: Data of list of role
                '404':
                description: The role was not found
        """
        response_data = role.serialize()
        body = HRSystemBuilder(
            response_data
        )
        body.add_namespace("hrsys", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.roleitem", role=role))
        body.add_control("profile", HRSYSTEM_PROFILE)
        body.add_control("collection", url_for("api.rolecollection"))
        body.add_control_delete_role(role)
        body.add_control_modify_role(role)
        body.add_control_get_roles()

        return Response(json.dumps(body), 200, mimetype=MASON)


    @require_admin
    def delete(self, role):
        """ Delete the selected role
        Arguments:
            role
        Returns:
            responses:
                '204':
                    description: The role was successfully deleted
                '404':
                    description: The role was not found
        """
        db.session.delete(role)
        db.session.commit()

        return Response(status=204)

    @require_admin
    def put(self, role):
        """ Replace role's basic data with new values
        Arguments:
            role
        Returns:
            responses:
                '204':
                description: The role's attributes were updated successfully
                '400':
                description: The request body was not valid
                '404':
                description: The role was not found
                '409':
                description: A role with the same name already exists
                '415':
                description: Wrong media type was used
        """
        db_role = Role.query.filter_by(code=role.code).first()

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Role.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        db_role.name = request.json["name"]
        db_role.code = request.json["code"]
        db_role.description = request.json["description"]

        try:
            db.session.commit()
        except (Exception, ):
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the role"
            )

        return Response(status=204)
