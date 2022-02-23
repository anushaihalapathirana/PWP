

from werkzeug.routing import BaseConverter
from HRSystem.models import Role, Department, Organization
from werkzeug.exceptions import NotFound


# Converter for Role entity in URL parameter
class RoleConverter(BaseConverter):
    def to_python(self, roleId):
        role = Role.query.filter_by(id=roleId).first()
        if role is None:
            raise NotFound
        return role

    def to_url(self, role):
        return str(role.id)


# Converter for Department entity in URL parameter
class DepartmentConverter(BaseConverter):
    def to_python(self, departmentId):
        department = Department.query.filter_by(id=departmentId).first()
        if department is None:
            raise NotFound
        return department

    def to_url(self, department):
        return str(department.id)


# Converter for Organization entity in URL parameter
class OrganizationConverter(BaseConverter):
    def to_python(self, organizationId):
        organization = Organization.query.filter_by(id=organizationId).first()
        if organization is None:
            raise NotFound
        return organization

    def to_url(self, organization):
        return str(organization.id)
