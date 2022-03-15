"""
This file contains the mapping of api resources
"""
from flask import Blueprint
from flask_restful import Api
from hr_system.resources.roles import RoleCollection, RoleItem
from hr_system.resources.organizations import OrganizationCollection, OrganizationItem
from hr_system.resources.departments import DepartmentCollection, DepartmentItem
from hr_system.resources.employees import (
    EmployeeByRlationCollection, EmployeeCollection, EmployeeItem
)
from hr_system.resources.leaveplans import LeavePlanByEmployeellection, LeavePlanItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# roles related resources
api.add_resource(RoleCollection, "/roles/")
api.add_resource(RoleItem, "/roles/<Role:role>/")

# organization related resources
api.add_resource(OrganizationCollection, "/organizations/")
api.add_resource(
    OrganizationItem,
    "/organizations/<Organization:organization>/")

# departments related resources
api.add_resource(DepartmentCollection, "/departments/")
api.add_resource(DepartmentItem, "/departments/<Department:department>/")

# employee related resources
api.add_resource(
    EmployeeByRlationCollection,
    "/organizations/<Organization:organization>/departments/<Department:department>/roles/<Role:role>/employees/",
    "/organizations/<Organization:organization>/departments/<Department:department>/employees/",
    "/organizations/<Organization:organization>/employees/",
    "/organizations/<Organization:organization>/roles/<Role:role>/employees/",
    "/employees/")
api.add_resource(
    EmployeeCollection,
    "/organizations/<Organization:organization>/departments/<Department:department>/roles/<Role:role>/employees/")
api.add_resource(EmployeeItem,
                 "/employees/<Employee:employee>/")

# leave plan related resources
api.add_resource(LeavePlanByEmployeellection,
                 "/employees/<Employee:employee>/leaveplans/")
api.add_resource(LeavePlanItem,
                 "/leaveplans/<LeavePlan:leaveplan>/")
