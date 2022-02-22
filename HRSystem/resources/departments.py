import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for, abort, Response
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import Department


class DepartmentCollection(Resource):

    def get(self):
        response_data = []
        depts = Department.query.all()
        
        for dept in depts:
            obj = {
                'id': dept.id,
                'name': dept.name,
                'description': dept.description,
            }
            response_data.append(obj)        
        return response_data
    

    def post(self):

        try:
            validate(request.json, Department.get_schema())
        except ValidationError as e:
            abort(400, 'Invalid JSON document')

        name = request.json['name']
        description = request.json['description']

        try:
            dept = Department.query.filter_by(name=name).first()
            
            if dept:
                abort(409, 'Department exist')
            dept = Department(
                name=name,
                description=description
            )
            db.session.add(dept)
            db.session.commit()
        except Exception:
            abort(404, 'Not found')
        return Response(response = {}, status = 201)


class DepartmentItem(Resource):

    def get(self, dept):
        dept = Department.query.filter_by(id=dept).first()
        
        if dept is None:
            abort(404, 'Not found')

        response_data = {
                'id': dept.id,
                'name': dept.name,
                'description': dept.description
            }
            
        return response_data

    def delete(self, dept):
        dept_db = Department.query.filter_by(id=dept).first()
        
        if dept_db is None:
            abort(404, 'Not found')
        
        db.session.delete(dept_db)
        db.session.commit()

        return Response(status=204)

    def put(self, dept):
        db_dept = Department.query.filter_by(id=dept).first()
        if db_dept is None:
            abort(404, 'Not found')

        if not request.json:
            abort(415, 'Unsupported media type')

        try:
            validate(request.json, Department.get_schema())
        except ValidationError as e:
            abort(400, 'Invalid JSON document')

        db_dept.name = request.json["name"]
        db_dept.description = request.json["description"]

        try:
            db.session.commit()
        except IntegrityError:
            abort(409, 'Already exists')

        return Response(status=204)