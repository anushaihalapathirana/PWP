"""
    This resource file contains the organization related REST calls implementation
"""
from jsonschema import validate, ValidationError
from flask import Response, request
from werkzeug.exceptions import HTTPException
from flask_restful import Resource
from hr_system import db
from hr_system.models import Organization
from hr_system.utils import create_error_message
from hr_system.utils import require_admin

class OrganizationCollection(Resource):
    """ This class contains the GET and POST method implementations for organization data
        Arguments:
        Returns:
        Endpoint: /api/organizations/

    """
    @require_admin
    def get(self):
        """ GET list of organizations
            Arguments:
            Returns:
                List of organizations
            responses:
                '200':
                description: The organizations retrieve successfully
        """
        response_data = []
        orgs = Organization.query.all()

        for org in orgs:
            response_data.append(org.serialize())
        return response_data

    @require_admin
    def post(self):
        """ Create a new organization
        Arguments:
            request:
                name: abc
                location: oulu
                organization_id: D01
        Returns:
            responses:
                '201':
                description: The organization was created successfully
                '400':
                description: The request body was not valid
                '409':
                description: A organization with the same id already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Invalid JSON document",
                "JSON format is not valid"
            )
        try:
            validate(request.json, Organization.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Unsupported media type",
                "Payload format is in an unsupported format"
            )
        try:
            db_org = Organization.query.filter_by(
                organization_id=request.json["organization_id"]
            ).first()
            if db_org is not None:
                return create_error_message(
                    409, "Already Exist",
                    "Department id is already exist"
                )
            org = Organization()
            org.deserialize(request)

            db.session.add(org)
            db.session.commit()
        except Exception as error:
            if isinstance(error, HTTPException):
                return create_error_message(
                    409, "Already Exist",
                    "Department id is already exist"
                )
            return create_error_message(
                500, "Internal Server Error",
                "Internal Server Error occurred!"
            )
        return Response(response={}, status=201)


class OrganizationItem(Resource):
    """ This class contains the GET, PUT and DELETE method implementations for a single org
        Arguments:
        Returns:
        Endpoint: /api/organization/<organization>/
    """
    @require_admin
    def get(self, organization):
        """ get details of one organization
        Arguments:
            organization
        Returns:
            Response
                '200':
                description: Data of list of organization
                '404':
                description: The organization was not found
        """
        response_data = organization.serialize()
        return response_data

    @require_admin
    def delete(self, organization):
        """ Delete the selected organization
        Arguments:
            organization
        Returns:
            responses:
                '204':
                    description: The organization was successfully deleted
                '404':
                    description: The organization was not found
        """
        db.session.delete(organization)
        db.session.commit()
        return Response(status=204)

    @require_admin
    def put(self, organization):
        """ Replace organization's basic data with new values
        Arguments:
            organization
        Returns:
            responses:
                '204':
                description: The organization's attributes were updated successfully
                '400':
                description: The request body was not valid
                '404':
                description: The organization was not found
                '409':
                description: A organization with the same name already exists
                '415':
                description: Wrong media type was used
        """
        db_org = Organization.query.filter_by(
            organization_id=organization.organization_id).first()

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Organization.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        db_org.name = request.json["name"]
        db_org.location = request.json["location"]

        try:
            db.session.commit()
        except (Exception, ):
            return create_error_message(
                500, "Internal server Error",
                "Error while adding the role"
            )

        return Response(status=204)
