import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for, Response
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import Role
from sqlalchemy.exc import IntegrityError
from HRSystem.utils import create_error_message
from werkzeug.exceptions import HTTPException
'''
This class contains the GET and POST method implementations for Role data
'''


class RoleCollection(Resource):

    def get(self):
        response_data = []
        roles = Role.query.all()

        for role in roles:
            response_data.append(role.serialize())
        return response_data

    def post(self):

        try:
            validate(request.json, Role.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            role = Role()
            role.deserialize()
            
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            return create_error_message(
                    500, "Internal server Error",
                    "Error while adding the role"
                )
            
        return Response(response={}, status=201)


'''
This class contains the GET, PUT and DELETE method implementations for a single role
'''


class RoleItem(Resource):

    def get(self, role):
    
        response_data =  role.serialize()

        return response_data

    def delete(self, role):
      
        db.session.delete(role)
        db.session.commit()

        return Response(status=204)

    def put(self, role):
        db_role = Role.query.filter_by(id=role.id).first()
        if db_role is None:
            return create_error_message(
                404, "Not found",
                "Role not exist"
            )

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Role.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        db_role.name = request.json["name"]
        db_role.code = request.json["code"]
        db_role.description = request.json["description"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_message(
                409, "Already exists",
                "Role is already exist"
            )

        return Response(status = 204)
