import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from HRSystem.constants import *

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" +
        os.path.join(app.instance_path, "hrcore.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

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

    @app.route(LINK_RELATIONS_URL)
    def send_link_relations():
        return "link relations"

    @app.route("/profiles/<profile>/")
    def send_profile(profile):
        return "you requests {} profile".format(profile)

    @app.route("/admin/")
    def admin_site():
        return app.send_static_file("html/admin.html")

    return app
