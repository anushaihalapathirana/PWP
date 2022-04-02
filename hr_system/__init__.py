"""
Init file
"""
import os
from flask import Flask
from flasgger import Swagger, swag_from
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from hr_system.constants import *

db = SQLAlchemy()
cache = Cache()


def create_app(test_config=None):
    """
    method to create application

    - Note reference to this method - course materials
        https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master
    """
    app = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='')
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" +
        os.path.join(app.instance_path, "hrcore.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    app.config["SWAGGER"] = {
        "title": "HR System API",
        "openapi": "3.0.3",
        "uiversion": 3,
    }
    swagger = Swagger(app, template_file="doc/hrsystem.yml")

    app.config["CACHE_TYPE"] = "FileSystemCache"
    app.config["CACHE_DIR"] = "cache"

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    cache.init_app(app)

    from hr_system.converters import (RoleConverter,
                                    DepartmentConverter,
                                    OrganizationConverter,
                                    LeavePlanConverter,
                                    EmployeeConverter)

    # Add converters
    app.url_map.converters["Role"] = RoleConverter
    app.url_map.converters["Department"] = DepartmentConverter
    app.url_map.converters["Organization"] = OrganizationConverter
    app.url_map.converters["LeavePlan"] = LeavePlanConverter
    app.url_map.converters["Employee"] = EmployeeConverter

    from hr_system.dbutils import init_db_command, generate_test_data
    from . import api

    app.cli.add_command(init_db_command)
    app.cli.add_command(generate_test_data)
    app.register_blueprint(api.api_bp)

    @app.route(LINK_RELATIONS_URL)
    def send_link_relations():
        return app.send_static_file("linkrelation.html")

    @app.route("/profiles/<profile>/")
    def send_profile(profile):
        # return "you requests {} profile".format(profile)
        if profile == 'role_item':
            return app.send_static_file("html/roleitem.html")
        elif profile == 'role_collection':
            return app.send_static_file("html/rolecollection.html")
        elif profile == 'organization_item':
            return app.send_static_file("html/organizationitem.html")
        elif profile == 'organization_collection':
            return app.send_static_file("html/organizationcollection.html")
        elif profile == 'department_item':
            return app.send_static_file("html/departmentitem.html")
        elif profile == 'department_collection':
            return app.send_static_file("html/departmentcollection.html")
        elif profile == 'employee_item':
            return app.send_static_file("html/employee.html")
        elif profile == 'employee_by_relation_collection':
            return app.send_static_file("html/employeecollection.html")
        elif profile == 'leaveplan_item':
            return app.send_static_file("html/leaveitem.html")
        elif profile == 'leaveplan_collection':
            return app.send_static_file("html/leavecollection.html")
        elif profile == 'error':
            return app.send_static_file("html/error.html")
        else:
            return "Not available"

    @app.route("/admin/")
    def admin_site():
        return app.send_static_file("admin.html")

    return app
