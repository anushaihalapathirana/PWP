"""
    This resource file contains the role related REST calls implementation
"""
from jsonschema import validate, ValidationError
from flask import Response, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from HRSystem import db
from HRSystem.models import Role
from HRSystem.utils import create_error_message

class RoleCollection(Resource):
    """ This class contains the GET and POST method implementations for role data
        Arguments:
        Returns:
    """
    def get(self):
        """ GET list of roles
            Arguments:
            Returns:
                List
        """
        response_data = []
        roles = Role.query.all()

        for role in roles:
            response_data.append(role.serialize())
        return response_data

    def post(self):
        """ POST roles
        Arguments:
            request
        Returns:
            Response
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
                    "role id is already exist"
            )
        return Response(response={}, status=201)

class RoleItem(Resource):
    """ This class contains the GET, PUT and DELETE method implementations for a single role
        Arguments:
        Returns:
    """
    def get(self, role):
        """ GET departments
        Arguments:
            department
        Returns:
            Response
        """
        response_data =  role.serialize()

        return response_data

    def delete(self, role):
        """ DELETE departments
        Arguments:
            department
        Returns:
            Response
        """
        db.session.delete(role)
        db.session.commit()

        return Response(status=204)

    def put(self, role):
        """ PUT departments
        Arguments:
            department
        Returns:
            Response
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
        except Exception: return create_error_message(
                500, "Internal server Error",
                "Error while updating the role"
            )

        return Response(status = 204)
