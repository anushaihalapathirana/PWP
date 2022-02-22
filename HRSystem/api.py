from flask import Blueprint
from flask_restful import Api

from HRSystem.resources.roles import RoleCollection

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(RoleCollection, "/roles/")
