import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for, Response
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import Organization
from HRSystem.utils import create_error_message

'''
This class contains the GET and POST method implementations for organization data
'''
class OrganizationCollection(Resource):

    def get(self):
        response_data = []
        orgs = Organization.query.all()
        
        for org in orgs:
            response_data.append(org.serialize())         
        return response_data
    

    def post(self):

        try:
            validate(request.json, Organization.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )
        try:
            org = Organization()
            org.deserialize()

            db.session.add(org)
            db.session.commit()
        except Exception:
            return create_error_message(
                    500, "Internal server Error",
                    "Error while adding the organization"
                )
        return Response(response = {}, status = 201)


'''
This class contains the GET, PUT and DELETE method implementations for a single organization
'''
class OrganizationItem(Resource):

    def get(self, organization):
        response_data = organization.serialize()
            
        return response_data

    def delete(self, organization):
            
        db.session.delete(organization)
        db.session.commit()

        return Response(status=204)

    def put(self, organization):
        db_org = Organization.query.filter_by(organization_id=organization.organization_id).first()
        if db_org is None:
            return create_error_message(
                404, "Not found",
                "Organization not found"
            )

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Organization.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        db_org.name = request.json["name"]
        db_org.location = request.json["location"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_message(
                409, "Already exists",
                "Organization is already exist"
            )

        return Response(status=204)