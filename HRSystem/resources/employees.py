
from flask_restful import Resource
from HRSystem import db
from HRSystem.models import Employee, MarritialEnum
from jsonschema import validate, ValidationError
from flask import Response, request, url_for, Response
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from HRSystem.utils import create_error_message

'''
This class contains the GET method implementations for employee by organization, department and role data
                
support to
    - GET employee list by providing organization, department and role data
    - GET employee list by providing organization and department data
    - GET employee list by providing organization and role
    - GET employee by providing organization data
    - GET all the employees
'''
class EmployeeByRlationCollection(Resource):

    def get(self, organization=None, department=None, role=None):

        employees_response = []
        employees = []
        if organization is not None and department is not None and role is not None:
            employees = Employee.query.join(Employee.organization).join(Employee.role).join(Employee.department).filter(
                Employee.organization == organization, Employee.role == role, Employee.department == department
            )

        elif organization is not None and department is not None:
            employees = Employee.query.join(Employee.organization).join(Employee.department).filter(
                Employee.organization == organization, Employee.department == department
            )

        elif organization is not None and role is not None:
            employees = Employee.query.join(Employee.organization).join(Employee.role).filter(
                Employee.organization == organization, Employee.role == role
            )
        elif organization is not None:
            employees = Employee.query.join(Employee.organization).filter(
                Employee.organization == organization
            )
        else:
            employees = Employee.query.all()

        for employee in employees:
            employees_response.append(employee.serialize())

        return employees_response



'''
This class contains the POST method implementations for employee - Add employees to the system by providing organization, department and role
                
- Note - Only method to add employees to the system is by giving organization, department and role 
'''
class EmployeeCollection(Resource):

    def post(self, organization, department, role):
        try:
            validate(request.json, Employee.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            employee = Employee()
            employee.deserialize(request)

            employee.role = role
            employee.organization = organization
            employee.department = department

            db.session.add(employee)
            db.session.commit()
        except Exception as e:
            return create_error_message(
                404, "Not found",
                "Employee not found"
            )
        return Response(response={}, status=201)


class EmployeeItem(Resource):

    def get(self, employee):
        print("uuuuu")
        employee = Employee.query.filter_by(id=employee).first()

        if employee is None:
            return create_error_message(
                404, "Not found",
                "Employee not found"
            )

        return employee.serialize()

    def put(self, employee):
        db_employee = Employee.query.filter_by(id=employee).first()
        if db_employee is None:
            return create_error_message(
                404, "Not found",
                "Employee not found"
            )

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Employee.get_schema())
        except ValidationError as e:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        employee = Employee()
        employee.deserialize(employee)
        employee.id = db_employee.id

        try:
            db.session.commit()
        except Exception:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the employee"
            )

        return Response(status=204)

    def delete(self, employee):
        db_employee = Employee.query.filter_by(id=employee).first()

        if db_employee is None:
            return create_error_message(
                404, "Not found",
                "Employee not found"
            )

        db.session.delete(db_employee)
        db.session.commit()

        return Response(status=204)
