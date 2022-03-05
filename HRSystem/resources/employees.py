"""
    This resource file contains the employee related REST calls implementation
"""
from copy import copy
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask import Response, request
from HRSystem import db
from HRSystem.models import Employee
from HRSystem.utils import create_error_message
from HRSystem import cache
from HRSystem import api
from HRSystem.utils import require_admin


class EmployeeByRlationCollection(Resource):
    """
    This class contains the GET method implementations for employee by organization, department and role data

    support to
        - GET employee list by providing organization, department and role data
        - GET employee list by providing organization and department data
        - GET employee list by providing organization and role
        - GET employee by providing organization data
        - GET all the employees
    """

    @require_admin
    def get(self, organization=None, department=None, role=None):
        """ GET list of employees
            Arguments:
            Returns:
                List
        """
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


class EmployeeCollection(Resource):
    """
    This class contains the POST method implementations for employee - Add employees to the system by providing organization, department and role

    - Note - Only method to add employees to the system is by giving organization, department and role
    """

    def _clear_cache(self, department, organnization, role):
        cache.delete_many(
            *[api.api.url_for(
                EmployeeByRlationCollection, organization=organnization, department=department, role=role
            ),
                api.api.url_for(
                EmployeeByRlationCollection, organization=organnization, department=department, role=None
            ),
                api.api.url_for(
                EmployeeByRlationCollection, organization=organnization, department=None, role=role
            ),
                api.api.url_for(
                EmployeeByRlationCollection, organization=None, department=None, role=None
            )]
        )

    def post(self, organization, department, role):
        """ POST departments
        Arguments:
            request
        Returns:
            Response
        """
        try:
            validate(request.json, Employee.get_schema())
        except ValidationError:
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

            self._clear_cache(department=department,
                              organnization=organization, role=role)
        except Exception as e:
            print("Error while POST operation : ", e)
            return create_error_message(
                404, "Not found",
                "Employee not found"
            )
        return Response(response={}, status=201)


class EmployeeItem(Resource):
    """ This class contains the GET, PUT and DELETE method implementations for a single employee
        Arguments:
        Returns:
    """

    def _clear_cache(self, department, organnization, role):
        cache.delete_many(
            *[api.api.url_for(
                EmployeeByRlationCollection, organization=organnization, department=department, role=role
            ),
                api.api.url_for(
                EmployeeByRlationCollection, organization=organnization, department=department, role=None
            ),
                api.api.url_for(
                EmployeeByRlationCollection, organization=organnization, department=None, role=role
            ),
                api.api.url_for(
                EmployeeByRlationCollection, organization=None, department=None, role=None
            )]
        )

    def get(self, employee):
        """ GET employee
        Arguments:
            employee
        Returns:
            Response
        """
        return employee.serialize()

    def put(self, employee):
        """ PUT employee
        Arguments:
            employee
        Returns:
            Response
        """
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Employee.get_schema())
        except ValidationError as e:
            print("Error while validating PUT operation : ", e)
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        old_employee = copy(employee)
        employee.deserialize(request)
        employee.id = old_employee.id
        employee.employee_id = old_employee.employee_id

        try:
            db.session.commit()
            self._clear_cache(department=employee.department,
                              organnization=employee.organization, role=employee.role)
        except Exception as e:
            print("Error while PUT operation : ", e)
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the employee"
            )

        return Response(status=204)

    def delete(self, employee):
        """ DELETE employee
        Arguments:
            employee
        Returns:
            Response
        """

        dept = copy(employee.department)
        org = copy(employee.organization)
        role = copy(employee.role)
        db.session.delete(employee)
        try:
            db.session.commit()
            self._clear_cache(department=dept,
                              organnization=org, role=role)
        except Exception as e:
            print("Error while DELETE operation : ", e)
            return create_error_message(
                500, "Internal server Error",
                "Error while deleting the employee"
            )

        return Response(status=204)
