from flask import Blueprint
from flask_restful import Api

from HRSystem.resources.roles import RoleCollection, RoleItem
from HRSystem.resources.organizations import OrganizationCollection, OrganizationItem
from HRSystem.resources.departments import DepartmentCollection, DepartmentItem
from HRSystem.resources.employees import EmployeeByRlationCollection, EmployeeCollection, EmployeeItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(RoleCollection, "/roles/")
api.add_resource(RoleItem, "/roles/<role>/")
api.add_resource(OrganizationCollection, "/organizations/")
api.add_resource(OrganizationItem, "/organizations/<org>/")
api.add_resource(DepartmentCollection, "/departments/")
api.add_resource(DepartmentItem, "/departments/<dept>/")
print("api registered")
api.add_resource(EmployeeByRlationCollection,
                 "/organizations/<Organization:organization>/departments/<Department:department>/roles/<Role:role>/employees/",
                 "/organizations/<Organization:organization>/departments/<Department:department>/employees/",
                 "/organizations/<Organization:organization>/employees/",
                 "/organizations/<Organization:organization>/roles/<Role:role>/employees/",
                 "/employees/")
api.add_resource(EmployeeCollection,
                 "/organizations/<Organization:organization>/departments/<Department:department>/roles/<Role:role>/employees/")
api.add_resource(EmployeeItem,
                 "/employees/<employee>")
