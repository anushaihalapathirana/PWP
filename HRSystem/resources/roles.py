import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for, abort, Response
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import Role

'''
This class contains the GET and POST method implementations for Role data
'''
class RoleCollection(Resource):

    def get(self):
        response_data = []
        roles = Role.query.all()
        
        for role in roles:
            obj = {
                'id': role.id,
                'name': role.name,
                'code': role.code,
                'description': role.description,
            }
            response_data.append(obj)        
        return response_data
    

    def post(self):

        try:
            validate(request.json, Role.get_schema())
        except ValidationError as e:
            abort(400, 'Invalid JSON document')

        name = request.json['name']
        code = request.json['code']
        description = request.json['description']

        try:
            role = Role.query.filter_by(code=code).first()
            
            if role:
                abort(409, 'Role exist')
            role = Role(
                name=name,
                code=code,
                description=description
            )
            db.session.add(role)
            db.session.commit()
        except Exception:
            abort(404, 'Not found')
        return Response(response = {}, status = 201)


'''
This class contains the GET, PUT and DELETE method implementations for a single role
'''
class RoleItem(Resource):

    def get(self, role):
        role = Role.query.filter_by(id=role).first()
        
        if role is None:
            abort(404, 'Not found')

        response_data = {
                'id': role.id,
                'name': role.name,
                'code': role.code,
                'description': role.description
            }
            
        return response_data

    def delete(self, role):
        role_db = Role.query.filter_by(id=role).first()
        
        if role_db is None:
            abort(404, 'Not found')
        
        db.session.delete(role_db)
        db.session.commit()

        return Response(status=204)

    def put(self, role):
        db_role = Role.query.filter_by(id=role).first()
        if db_role is None:
            abort(404, 'Not found')

        if not request.json:
            abort(415, 'Unsupported media type')

        try:
            validate(request.json, Role.get_schema())
        except ValidationError as e:
            abort(400, 'Invalid JSON document')

        db_role.name = request.json["name"]
        db_role.code = request.json["code"]
        db_role.description = request.json["description"]

        try:
            db.session.commit()
        except IntegrityError:
            abort(409, 'Already exists')

        return Response(status=204)