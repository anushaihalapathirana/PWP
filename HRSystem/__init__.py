"""
Init file
"""
import os
from flask import Flask
from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from HRSystem.constants import *
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache()

def create_app(test_config=None):
    """
    method to create application

    - Note reference to this method - course materials https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master
    """
    app = Flask(__name__, instance_relative_config=True)
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

    from HRSystem.converters import RoleConverter, DepartmentConverter, OrganizationConverter, LeavePlanConverter, EmployeeConverter
    # Add converters
    app.url_map.converters["Role"] = RoleConverter
    app.url_map.converters["Department"] = DepartmentConverter
    app.url_map.converters["Organization"] = OrganizationConverter
    app.url_map.converters["LeavePlan"] = LeavePlanConverter
    app.url_map.converters["Employee"] = EmployeeConverter

    from HRSystem.dbutils import init_db_command, generate_test_data
    from . import api

    app.cli.add_command(init_db_command)
    app.cli.add_command(generate_test_data)
    app.register_blueprint(api.api_bp)

    return app
