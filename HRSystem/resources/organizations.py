import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for, abort, Response
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import Organization


class OrganizationCollection(Resource):

    def get(self):
        response_data = []
        orgs = Organization.query.all()
        
        for org in orgs:
            obj = {
                'id': org.id,
                'name': org.name,
                'location': org.location,
            }
            response_data.append(obj)        
        return response_data
    

    def post(self):

        try:
            validate(request.json, Organization.get_schema())
        except ValidationError as e:
            abort(400, 'Invalid JSON document')

        name = request.json['name']
        location = request.json['location']

        try:
            org = Organization.query.filter_by(name=name).first()
            
            if org:
                abort(409, 'Organization exist')
            org = Organization(
                name=name,
                location=location
            )
            db.session.add(org)
            db.session.commit()
        except Exception:
            abort(404, 'Not found')
        return Response(response = {}, status = 201)


class OrganizationItem(Resource):

    def get(self, org):
        org = Organization.query.filter_by(id=org).first()
        
        if org is None:
            abort(404, 'Not found')

        response_data = {
                'id': org.id,
                'name': org.name,
                'location': org.location
            }
            
        return response_data

    def delete(self, org):
        org_db = Organization.query.filter_by(id=org).first()
        
        if org_db is None:
            abort(404, 'Not found')
        
        db.session.delete(org_db)
        db.session.commit()

        return Response(status=204)

    def put(self, org):
        db_org = Organization.query.filter_by(id=org).first()
        if db_org is None:
            abort(404, 'Not found')

        if not request.json:
            abort(415, 'Unsupported media type')

        try:
            validate(request.json, Organization.get_schema())
        except ValidationError as e:
            abort(400, 'Invalid JSON document')

        db_org.name = request.json["name"]
        db_org.location = request.json["location"]

        try:
            db.session.commit()
        except IntegrityError:
            abort(409, 'Already exists')

        return Response(status=204)