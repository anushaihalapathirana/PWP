"""
Database model file
"""
import hashlib
from enum import Enum
from datetime import datetime
from hr_system import db


class TitleEnum(Enum):
    """
    Enum class for employee suffix
    """
    MR = 'Mr'
    MISS = 'Miss'
    MRS = 'Mrs'
    DR = 'Dr'


class MarritialEnum(Enum):
    """
    Enum class for maritial status
    """
    MARRIED = 'Married'
    DIVORCED = 'Divorced'
    SINGLE = 'Single'
    WIDOWED = 'Widowed'
    UNAVAILABLE = 'Unavailable'


class LeaveTypeEnum(Enum):
    """
    Leave type enum class
    """
    MEDICAL = 'Medical'
    CASUAL = 'Casual'
    PATERNITY = 'Paternity'
    MATERNITY = 'Maternity'
    SABBATICAL = 'Sabbatical'
    UNPAID = 'Unpaid'


class Employee(db.Model):
    """
    Employee model class
    """
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    middle_name = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(32), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    active_emp = db.Column(db.Boolean, default=True, nullable=False)
    prefix_title = db.Column(db.Enum(TitleEnum), nullable=True)
    marritial_status = db.Column(db.Enum(MarritialEnum), nullable=True)
    mobile_no = db.Column(db.String(256), nullable=False)
    basic_salary = db.Column(db.Integer, nullable=False)
    account_number = db.Column(db.String(256), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey(
        "role.id", ondelete="SET NULL"))
    organization_id = db.Column(db.Integer, db.ForeignKey(
        "organization.id", ondelete="SET NULL"))
    department_id = db.Column(db.Integer, db.ForeignKey(
        "department.id", ondelete="SET NULL"))

    organization = db.relationship(
        'Organization', backref='employee_organization')
    department = db.relationship('Department', backref='employee_department')
    role = db.relationship('Role', backref='employee_role')

    def serialize(self):
        """
        Serialize method
        """
        employee = {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name and self.middle_name,
            "address": self.address,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.isoformat(),
            "appointment_date": self.appointment_date.isoformat(),
            "active_emp": self.active_emp,
            "prefix_title": self.prefix_title and self.prefix_title.name,
            "marritial_status": self.marritial_status and self.marritial_status.name,
            "mobile_no": self.mobile_no,
            "basic_salary": self.basic_salary,
            "account_number": self.account_number}
        return employee

    def deserialize(self, request):
        """
        Desrialize method
        """
        self.employee_id = request.json.get('employee_id', None)
        self.first_name = request.json['first_name']
        self.middle_name = request.json.get('middle_name', None)
        self.last_name = request.json['last_name']
        self.address = request.json['address']
        self.gender = request.json['gender']
        self.date_of_birth = datetime.fromisoformat(
            request.json['date_of_birth'])
        self.appointment_date = datetime.fromisoformat(
            request.json['appointment_date'])
        self.active_emp = request.json['active_emp']
        self.prefix_title = request.json.get(
            'prefix_title', None) and TitleEnum[request.json['prefix_title']]
        self.marritial_status = request.json.get(
            'marritial_status', None) and MarritialEnum[request.json['marritial_status']]
        self.mobile_no = request.json['mobile_no']
        self.basic_salary = request.json['basic_salary']
        self.account_number = request.json['account_number']

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": [
                "first_name",
                "last_name",
                "address",
                "gender",
                "appointment_date",
                "active_emp",
                "mobile_no",
                "basic_salary",
                "account_number"]}
        props = schema["properties"] = {}
        props["employee_id"] = {
            "description": "Employee unique id",
            "type": "string"
        }
        props["first_name"] = {
            "description": "Employee First name",
            "type": "string"
        }
        props["middle_name"] = {
            "description": "Employee middle name",
            "type": ["string", "null"]
        }
        props["last_name"] = {
            "description": "Employee last name",
            "type": "string"
        }
        props["address"] = {
            "description": "Employee address",
            "type": "string"
        }
        props["gender"] = {
            "description": "Employee gender",
            "type": "string"
        }
        props["date_of_birth"] = {
            "description": "Employee date of birth",
            "type": ["string", "null"],
            "format": "date-time"
        }
        props["appointment_date"] = {
            "description": "Employee date of appoinment",
            "type": "string",
            "format": "date-time"
        }
        props["prefix_title"] = {
            "description": "Employee name title",
            "type": ["string", "null"],
            "enum": [e.name for e in TitleEnum]
        }
        props["marritial_status"] = {
            "description": "Employee merritial status",
            "enum": [e.name for e in MarritialEnum],
            "type": ["string", "null"]
        }
        props["mobile_no"] = {
            "description": "Employee mobile number",
            "type": "string"
        }
        props["basic_salary"] = {
            "description": "Employee basic salary",
            "type": "number"
        }
        props["account_number"] = {
            "description": "Employee bank account number",
            "type": "string"
        }

        return schema


class Organization(db.Model):
    """
    organization model class
    """
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, unique=True)
    location = db.Column(db.String(256), nullable=False)

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["organization_id", "name", "location"]
        }
        props = schema["properties"] = {}
        props["organization_id"] = {
            "description": "organization id",
            "type": "string"
        }
        props["name"] = {
            "description": "organization name",
            "type": "string"
        }
        props["location"] = {
            "description": "organization location",
            "type": "string"
        }
        return schema

    def serialize(self):
        """
        Serialize method
        """
        org = {
            "organization_id": self.organization_id,
            "name": self.name,
            "location": self.location
        }
        return org

    def deserialize(self, request):
        """
        Desrialize method
        """
        self.organization_id = request.json['organization_id']
        self.name = request.json['name']
        self.location = request.json['location']


class Department(db.Model):
    """
    department model class
    """
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=True)

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["department_id", "name"]
        }
        props = schema["properties"] = {}
        props["department_id"] = {
            "description": "department id",
            "type": "string"
        }
        props["name"] = {
            "description": "department name",
            "type": "string"
        }
        props["description"] = {
            "description": "department description",
            "type": ["string", "null"]
        }
        return schema

    def serialize(self):
        """
        Serialize method
        """
        department = {
            "department_id": self.department_id,
            "name": self.name,
            "description": self.description and self.description
        }
        return department

    def deserialize(self, request):
        """
        Desrialize method
        """
        self.department_id = request.json['department_id']
        self.name = request.json['name']
        self.description = request.json.get('description', None)


class Role(db.Model):
    """
    role model class
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    code = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=True)

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["name", "code"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Role's unique name",
            "type": "string"
        }
        props["code"] = {
            "description": "unique code of role",
            "type": "string"
        }
        props["description"] = {
            "description": "description of role",
            "type": ["string", "null"]
        }
        return schema

    def serialize(self):
        """
        Serialize method
        """
        role = {
            "name": self.name,
            "code": self.code,
            "description": self.description and self.description
        }
        return role

    def deserialize(self, request):
        """
        Deserialize method
        """
        self.name = request.json['name']
        self.code = request.json['code']
        self.description = request.json.get('description', None)


class LeavePlan(db.Model):
    """
    leave plan model class
    """
    id = db.Column(db.Integer, primary_key=True)
    leave_type = db.Column(db.Enum(LeaveTypeEnum), nullable=False)
    reason = db.Column(db.String(256), nullable=True)
    leave_date = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        "employee.id", ondelete="SET NULL"))

    employee = db.relationship('Employee', backref='employee_leave_plan')

    @staticmethod
    def get_schema():
        """
        method to get schema
        """
        schema = {
            "type": "object",
            "required": ["leave_type", "leave_date"]
        }
        props = schema["properties"] = {}
        props["leave_type"] = {
            "description": "Type of leave",
            "type": "string",
            "enum": [e.name for e in LeaveTypeEnum]
        }
        props["leave_date"] = {
            "description": "leave date",
            "type": "string",
            "format": "date-time"
        }
        props["reason"] = {
            "description": "reason for leave",
            "type": ["string", "null"]
        }
        return schema

    def serialize(self):
        """
        Serialize method
        """
        leaveplan = {
            "id": self.id,
            "leave_type": self.leave_type and self.leave_type.name,
            "reason": self.reason and self.reason,
            "leave_date": self.leave_date.isoformat(),
        }
        return leaveplan

    def deserialize(self, request):
        """
        Desrialize method
        """
        self.leave_type = request.json['leave_type'] and LeaveTypeEnum[request.json['leave_type']]
        self.reason = request.json.get('reason', None)
        self.leave_date = datetime.fromisoformat(
            request.json['leave_date'])


class ApiKey(db.Model):
    """
    API key model class
    """
    key = db.Column(db.String(32), nullable=False,
                    unique=True, primary_key=True)
    employee_id = db.Column(
        db.Integer, db.ForeignKey("employee.id"), nullable=True)
    admin = db.Column(db.Boolean, default=False)
    employee = db.relationship('Employee', backref='api_key')
    # employee = db.relationship("Employee", back_populates="api_key", uselist=False)

    @staticmethod
    def key_hash(key):
        """
        static method to get hash key
        """
        return hashlib.sha256(key.encode()).digest()
