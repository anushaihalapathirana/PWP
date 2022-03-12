"""
    This resource file contains the employee related REST calls implementation
"""
from copy import copy
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask import Response, request
from werkzeug.exceptions import HTTPException
from HRSystem import db
from HRSystem.models import Employee
from HRSystem.utils import create_error_message
from HRSystem import cache
from HRSystem import api
from HRSystem.utils import require_admin, require_employee_key


class EmployeeByRlationCollection(Resource):
    """
    This class contains the GET method implementations for employee by organization,
    department and role data

    Method support to
        - GET employee list by providing organization, department and role data
        - GET employee list by providing organization and department data
        - GET employee list by providing organization and role
        - GET employee by providing organization data
        - GET all the employees

    """
    def page_key(*args, **kwargs):
        return str(request.path)

    @classmethod
    @require_admin
    @cache.cached(make_cache_key=page_key)
    def get(cls, organization=None, department=None, role=None):
        """ GET list of employees
            Endpoint:
        "/organizations/<Organization:organization>/departments/
            <Department:department>/roles/<Role:role>/employees/",
        "/organizations/<Organization:organization>/departments/
            <Department:department>/employees/",
        "/organizations/<Organization:organization>/employees/",
        "/organizations/<Organization:organization>/roles/<Role:role>/employees/",
        "/employees/"
            Arguments:
                organization
                department
                role
            Returns:
                List of employees
            responses:
                '200':
                description: The organizations retrieve successfully
        """
        employees_response = []
        employees = []
        if organization is not None and department is not None and role is not None:
            employees = Employee.query.join(
                Employee.organization).join(
                Employee.role).join(
                Employee.department).filter(
                Employee.organization == organization,
                Employee.role == role,
                Employee.department == department)

        elif organization is not None and department is not None:
            employees = Employee.query.join(
                Employee.organization).join(
                Employee.department).filter(
                Employee.organization == organization,
                Employee.department == department)

        elif organization is not None and role is not None:
            employees = Employee.query.join(
                Employee.organization).join(
                Employee.role).filter(
                Employee.organization == organization, Employee.role == role)
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
    This class contains the POST method implementations for employee
        - Add employees to the system by providing organization, 
          department and role

    - Note - Only method to add employees to the system is by giving organization,
        department and role

    Endpoint:
        api/organizations/<Organization:organization>/departments/
            <Department:department>/roles/<Role:role>/employees/
    """

    def _clear_cache(self, department, organnization, role):
        cache.delete_many(
            *
            [
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=organnization,
                    department=department,
                    role=role),
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=organnization,
                    department=department,
                    role=None),
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=organnization,
                    department=None,
                    role=role),
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=None,
                    department=None,
                    role=None)])

    @require_admin
    def post(self, organization, department, role):
        """ Create a new employee
        Arguments:
            organization
            department
            role
            request:
                employee_id: 001
                first_name: test 1
                middle_name: middle 1
                last_name: last name 1
                address: oulu
                gender: M
                date_of_birth: 1998-08-25T11:20:30
                appointment_date: 2005-08-25T11:20:30
                active_emp: 1
                prefix_title: MR
                marritial_status: SINGLE
                mobile_no: N756982365
                basic_salary: 56665
                account_number: FI545455
        Returns:
            responses:
                '201':
                description: The employee was created successfully
                '400':
                description: The request body was not valid
                '409':
                description: A employee with the same id already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Invalid JSON document",
                "JSON format is not valid"
            )
        try:
            validate(request.json, Employee.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            db_emp = Employee.query.filter_by(
                employee_id=request.json["employee_id"]).first()
            if db_emp is not None:
                return create_error_message(
                    409, "Already Exist",
                    "Department id is already exist"
                )
            employee = Employee()
            employee.deserialize(request)

            employee.role = role
            employee.organization = organization
            employee.department = department

            db.session.add(employee)
            db.session.commit()

            self._clear_cache(department=department,
                              organnization=organization, role=role)
        except Exception as error:
            if isinstance(error, HTTPException):
                return create_error_message(
                    409, "Already Exist",
                    "employee id is already exist"
                )
            return create_error_message(
                500, "Internal Server Error",
                "Internal Server Error occurred!"
            )
        return Response(response={}, status=201)


class EmployeeItem(Resource):
    """ This class contains the GET, PUT and DELETE method implementations for a single employee
        Arguments:
        Returns:
        Endpoints: /api/employees/<Employee:employee>/
    """

    def _clear_cache(self, department, organnization, role):
        cache.delete_many(
            *
            [
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=organnization,
                    department=department,
                    role=role),
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=organnization,
                    department=department,
                    role=None),
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=organnization,
                    department=None,
                    role=role),
                api.api.url_for(
                    EmployeeByRlationCollection,
                    organization=None,
                    department=None,
                    role=None)])

    def page_key(*args, **kwargs):
        return str(request.path)

    @classmethod
    @require_employee_key
    @cache.cached(make_cache_key=page_key)
    def get(cls, employee):
        """ get details of one employee
            Arguments:
                employee
            Returns:
                Response
                    '200':
                    description: Data of list of employees
                    '404':
                    description: The employee was not found
        """
        return employee.serialize()

    @require_employee_key
    def put(self, employee):
        """ Replace employee's basic data with new values
        Arguments:
            employee
        Returns:
            responses:
                '204':
                description: The employee's attributes were updated successfully
                '400':
                description: The request body was not valid
                '404':
                description: The employee was not found
                '409':
                description: A employee with the same name already exists
                '415':
                description: Wrong media type was used
        """
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Employee.get_schema())
        except ValidationError:
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
            self._clear_cache(
                department=employee.department,
                organnization=employee.organization,
                role=employee.role)
        except Exception:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the employee"
            )

        return Response(status=204)

    @require_employee_key
    def delete(self, employee):
        """ Delete the selected employee
        Arguments:
            employee
        Returns:
            responses:
                '204':
                    description: The employee was successfully deleted
                '404':
                    description: The employee was not found
        """
        dept = copy(employee.department)
        org = copy(employee.organization)
        role = copy(employee.role)
        db.session.delete(employee)
        try:
            db.session.commit()
            self._clear_cache(department=dept,
                              organnization=org, role=role)
        except Exception:
            return create_error_message(
                500, "Internal server Error",
                "Error while deleting the employee"
            )

        return Response(status=204)
