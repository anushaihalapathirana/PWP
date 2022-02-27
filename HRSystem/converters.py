

from werkzeug.routing import BaseConverter
from HRSystem.models import Role, Department, Organization, LeavePlan, Employee
from werkzeug.exceptions import NotFound
from HRSystem.utils import create_error_message

# Converter for Role entity in URL parameter
class RoleConverter(BaseConverter):
    def to_python(self, roleId):
        role = Role.query.filter_by(id=roleId).first()
        if role is None:
            return create_error_message(
                404, "Not found",
                "Role not found"
            )
        return role

    def to_url(self, role):
        return str(role.id)


# Converter for Department entity in URL parameter
class DepartmentConverter(BaseConverter):
    def to_python(self, departmentId):
        department = Department.query.filter_by(id=departmentId).first()
        if department is None:
            return create_error_message(
                404, "Not found",
                "Department not found"
            )
        return department

    def to_url(self, department):
        return str(department.id)


# Converter for Organization entity in URL parameter
class OrganizationConverter(BaseConverter):
    def to_python(self, organizationId):
        organization = Organization.query.filter_by(id=organizationId).first()
        if organization is None:
            return create_error_message(
                404, "Not found",
                "Organization not found"
            )
        return organization

    def to_url(self, organization):
        return str(organization.id)

# Converter for leave plan entity in URL parameter
class LeavePlanConverter(BaseConverter):
    def to_python(self, leaveplanId):
        leaveplan = LeavePlan.query.filter_by(id=leaveplanId).first()
     
        if leaveplan is None:
            return create_error_message(
                404, "Not found",
                "leave plan not found"
            )
        return leaveplan

    def to_url(self, leaveplan):
        return str(leaveplan.id)


# Converter for employee entity in URL parameter
class EmployeeConverter(BaseConverter):
    def to_python(self, employeeId):
        employee = Employee.query.filter_by(id=employeeId).first()
        if employee is None:
            return create_error_message(
                404, "Not found",
                "employee not found"
            )
        return employee

    def to_url(self, employee):
        return str(employee.id)
