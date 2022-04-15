"""
This file contains the util functions

"""
import secrets
import json
from flask import abort, request, url_for, Response
from hr_system.models import ApiKey
from hr_system.constants import *
from hr_system.models import *


class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href


class HRSystemBuilder(MasonBuilder):
    """
    HR system mason builder. this class manage all mason objects
    """
    # role

    def add_control_delete_role(self, role):
        """
        custom relation method to add control to delete roles
        """
        self.add_control(
            "hrsys:delete-role",
            url_for("api.roleitem", role=role),
            method="DELETE",
            title="Delete this role"
        )

    def add_control_add_role(self):
        """
        custom relation method to add control to add roles
        """
        self.add_control(
            "hrsys:add-role",
            url_for("api.rolecollection"),
            method="POST",
            encoding="json",
            title="Add a new role",
            schema=Role.get_schema()
        )

    def add_control_modify_role(self, role):
        """
        custom relation method to add control to modify roles
        """
        self.add_control(
            "edit",
            url_for("api.roleitem", role=role),
            method="PUT",
            encoding="json",
            title="Edit this role",
            schema=Role.get_schema()
        )

    # organization

    def add_control_delete_organization(self, organization):
        """
        custom relation method to add control to delete org
        """
        self.add_control(
            "hrsys:delete-organization",
            url_for("api.organizationitem", organization=organization),
            method="DELETE",
            title="Delete this organization"
        )

    def add_control_add_organization(self):
        """
        custom relation method to add control to add org
        """
        self.add_control(
            "hrsys:add-organization",
            url_for("api.organizationcollection"),
            method="POST",
            encoding="json",
            title="Add a new organization",
            schema=Organization.get_schema()
        )

    def add_control_modify_organization(self, organization):
        """
        custom relation method to add control to modify org
        """
        self.add_control(
            "edit",
            url_for("api.organizationitem", organization=organization),
            method="PUT",
            encoding="json",
            title="Edit this organization",
            schema=Organization.get_schema()
        )

    def add_control_add_employee(self, role, department, organization):
        """
        custom relation method to add control to add employee
        """
        self.add_control(
            "hrsys:add-employee",
            url_for("api.employeecollection", organization=organization,
                    department=department, role=role),
            method="POST",
            encoding="json",
            title="Add a new employee given the organization department and role",
            schema=Employee.get_schema()
        )

    def add_control_modify_employee(self, employee):
        """
        custom relation method to add control to modify employee
        """
        self.add_control(
            "edit",
            url_for("api.employeeitem", employee=employee),
            method="PUT",
            encoding="json",
            title="Edit this employee",
            schema=Employee.get_schema()
        )

    def add_control_get_employee(self, employee):
        """
        custom relation method to add control to get employee
        """
        self.add_control(
            "hrsys: employee",
            url_for("api.employeeitem", employee=employee),
            method="GET",
            title="Get this employee",
        )

    def add_control_delete_employee(self, employee):
        """
        custom relation method to add control to delete employee
        """
        self.add_control(
            "hrsys:delete-employee",
            url_for("api.employeeitem", employee=employee),
            method="DELETE",
            title="Delete this employee"
        )

    def add_control_organization(self, organization):
        """
        custom relation method to add control to get one org
        """
        self.add_control(
            "hrsys:organization",
            url_for("api.organizationitem", organization=organization),
            method="GET",
            title="get organization"
        )

    def add_control_department(self, department):
        """
        custom relation method to add control to get one dept
        """
        self.add_control(
            "hrsys:department",
            url_for("api.departmentitem", department=department),
            method="GET",
            title="get department",
        )

    def add_control_department_list(self):
        """
        custom relation method to add control to get depts
        """
        self.add_control(
            "hrsys:departments-all",
            url_for("api.departmentcollection"),
            method="GET",
            title="get departments",
        )

    def add_control_role(self, role):
        """
        custom relation method to add control to get one role
        """
        self.add_control(
            "hrsys:role",
            url_for("api.roleitem", role=role),
            method="GET",
            title="get role"
        )
    
    def add_control_role_list(self):
        """
        custom relation method to add control to roles
        """
        self.add_control(
            "hrsys:roles-all",
            url_for("api.rolecollection"),
            method="GET",
            title="get roles"
        )

    def add_control_employee_by_org(self, organization):
        """
        custom relation method to add control to get employees by org
        """
        self.add_control(
            "hrsys:by-org",
            url_for("api.employeebyrlationcollection",
                    organization=organization, role=None, department=None),
            method="GET",
            title="get employees by organization"
        )

    def add_control_employee_by_org_dept(self, organization, department):
        """
        custom relation method to add control to get employees by org and dept
        """
        self.add_control(
            "hrsys:by-org-dept",
            url_for("api.employeebyrlationcollection",
                    organization=organization, role=None, department=department),
            method="GET",
            title="get employees by organization and department"
        )

    def add_control_employee_by_org_role(self, organization, role):
        """
        custom relation method to add control to get employees by org and role
        """
        self.add_control(
            "hrsys:by-org-role",
            url_for("api.employeebyrlationcollection",
                    organization=organization, role=role, department=None),
            method="GET",
            title="get employees by organization and role"
        )

    def add_control_employee_by_org_dept_role(self, organization, department, role):
        """
        custom relation method to add control to get employees by org, dept and role
        """
        self.add_control(
            "hrsys:by-org-dept-role",
            url_for("api.employeebyrlationcollection",
                    organization=organization, role=role, department=department),
            method="GET",
            title="get employees by organization,department and role"
        )
    
    def add_control_employee_by_org_dept_role_hrf(self):
        """
        custom relation method to add control to get employees by org, dept and role 
        using url parameters
        """
        self.add_control(
            "hrsys:by-org-dept-role-url-param",
            "/api/organizations/{organization}/departments/{department}/roles/{role}/employees/",
            isHrefTemplate= True,
            method="GET",
            title="get employees by organization,department and role",
            schema=self._org_dept_role_schema()
            
        )
    
    def add_control_get_employee_all(self):
        """
        custom relation method to add control to get emp collection
        """
        self.add_control(
            "hrsys:employee-all",
            url_for("api.employeebyrlationcollection",
                    organization=None, role=None, department=None),
            method="GET",
            title="get employees"
        )

    # department
    def add_control_add_department(self):
        """
        custom relation method to add control to add department
        """
        self.add_control(
            "hrsys:add-dept",
            url_for("api.departmentcollection"),
            method="POST",
            encoding="json",
            title="Add a new department",
            schema=Department.get_schema()
        )

    def add_control_delete_department(self, department):
        """
        custom relation method to add control to delete dept
        """
        self.add_control(
            "hrsys:delete-dept",
            url_for("api.departmentitem", department=department),
            method="DELETE",
            title="Delete this department"
        )

    def add_control_modify_department(self, department):
        """
        custom relation method to add control to edit dept
        """
        self.add_control(
            "edit",
            url_for("api.departmentitem", department=department),
            method="PUT",
            encoding="json",
            title="Edit this department",
            schema=Department.get_schema()
        )

    # leaveplan
    def add_control_add_leave(self, emp):
        """
        custom relation method to add control to add leave
        """
        self.add_control(
            "hrsys:add-leave",
            url_for("api.leaveplanbyemployeellection", employee=emp),
            method="POST",
            encoding="json",
            title="Add a new leave",
            schema=LeavePlan.get_schema()
        )

    def add_control_get_leave(self, emp):
        """
        custom relation method to add control to get leave
        """
        uri = url_for("api.leaveplanbyemployeellection", employee=emp)
        self.add_control(
            "hrsys:leaves",
            uri,
            method="GET",
            title="get employee leave plans"
        )

    def add_control_delete_leave(self, emp, leave):
        """
        custom relation method to add control to delete leave
        """
        self.add_control(
            "hrsys:delete-leave",
            url_for("api.leaveplanitem", employee=emp, leaveplan=leave),
            method="DELETE",
            title="Delete this leave"
        )

    def add_control_modify_leave(self, emp, leave):
        """
        custom relation method to add control to edit leave
        """
        self.add_control(
            "edit",
            url_for("api.leaveplanitem", employee=emp, leaveplan=leave),
            method="PUT",
            encoding="json",
            title="Edit this leave",
            schema=LeavePlan.get_schema()
        )

    @staticmethod
    def _paginator_schema():
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        props = schema["properties"]
        props["index"] = {
            "description": "Starting index for pagination",
            "type": "integer",
            "default": "0"
        }
        return schema

    @staticmethod
    def _org_dept_role_schema():
        schema = {
            "type": "object",
            "required": []
        }
        props = schema["properties"] = {}
        props["organization"] = {
            "description": "department id",
            "type": "string",
            "default": "O01"
        }
        props["department"] = {
            "description": "get emploees by dept",
            "type": "string",
            "default": "D01"
        }
        props["role"] = {
            "description": "get emploees by role",
            "type": "string",
            "default": "MAN",
        }
        return schema
    


def create_error_message(status_code, error, message=None):
    """
    Method to create error message
    Return
        - Error object
    """
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(error, message)
    body.add_control("profile", href=ERROR_PROFILE)
    error_response = Response(json.dumps(body), status_code, mimetype=MASON)
    return abort(error_response)


def require_admin(func):
    """
    Method to validate admin key
    """

    def wrapper(*args, **kwargs):
        api_key = request.headers.get("HRSystem-Api-Key")
        if api_key is None:
            return create_error_message(403, "Authentication Error")
        key_hash = ApiKey.key_hash(
            request.headers.get("HRSystem-Api-Key").strip())
        db_key = ApiKey.query.filter_by(admin=True).first()
        if secrets.compare_digest(key_hash, db_key.key):
            return func(*args, **kwargs)
        return create_error_message(403, "Authentication Error")
    return wrapper


def require_employee_key(func):
    """
    Method to validate employee key
    """

    def wrapper(self, employee, *args, **kwargs):
        api_key = request.headers.get("HRSystem-Api-Key")
        if api_key is None:
            return create_error_message(403, "Authentication Error")
        key_hash = ApiKey.key_hash(
            request.headers.get("HRSystem-Api-Key").strip())
        admin_db_key = ApiKey.query.filter_by(admin=True).first()
        if secrets.compare_digest(key_hash, admin_db_key.key):
            return func(self, employee, *args, **kwargs)
        else:
            db_key = ApiKey.query.filter_by(employee=employee).first()
            if db_key is not None and secrets.compare_digest(
                    key_hash, db_key.key):
                return func(self, employee, *args, **kwargs)
            return create_error_message(403, "Authentication Error")

    return wrapper
