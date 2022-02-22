from flask import Blueprint
from flask_restful import Api

from HRSystem.resources.roles import RoleCollection, RoleItem
from HRSystem.resources.organizations import OrganizationCollection, OrganizationItem
from HRSystem.resources.departments import DepartmentCollection, DepartmentItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(RoleCollection, "/roles/")
api.add_resource(RoleItem, "/roles/<role>/")
api.add_resource(OrganizationCollection, "/organizations/")
api.add_resource(OrganizationItem, "/organizations/<org>/")
api.add_resource(DepartmentCollection, "/departments/")
api.add_resource(DepartmentItem, "/departments/<dept>/")

