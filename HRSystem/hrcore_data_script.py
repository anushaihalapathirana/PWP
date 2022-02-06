# script to insert data to the database

from models import db
from models import Role, Organization, Department, Employee, LeavePlan
from datetime import datetime

db.create_all()
role = Role(name="Manager",code='MAN',description='Role manager')
role2 = Role(name="Receptionnist",code='RES',description='Role reception')
role3 = Role(name="Team Lead",code='TL')
role4 = Role(name="Associate team lead",code='ATL')
role5 = Role(name="Developer",code='DEV')
role6 = Role(name="Quality analysis",code='QA')


org = Organization(name="Org1", location="oulu")
org2 = Organization(name="Org2", location="helsinki")

depat = Department(name="dept1", description="department number one")
depat2 = Department(name="dept2", description="department number two")
depat3 = Department(name="dept3", description="department number three")

emp = Employee(first_name="anusha", last_name = "pathirana", address = "oulu", gender = "F",date_of_birth=datetime(1995, 10, 21, 11, 20, 30),appointment_date = datetime(2018, 11, 21, 11, 20, 30), active_emp = 1, suffix_title = 'MISS', marritial_status = 'SINGLE', mobile_no='21456',basic_salary=10000, account_number="11233565456", role = role, organization=org, department = depat2)
emp2 = Employee(first_name="sameera", last_name = "panditha", address = "raksila", gender = "M",date_of_birth=datetime(1998, 8, 25, 11, 20, 30),appointment_date = datetime(2018, 11, 21, 11, 20, 30), active_emp = 1, suffix_title = 'MR', marritial_status = 'SINGLE', mobile_no='21456',basic_salary=10000, account_number="11233565456", role = role2, organization=org2, department = depat)
emp3 = Employee(first_name="madu", last_name = "wicks", address = "kajaanentie", gender = "F",date_of_birth=datetime(2000, 5, 2, 11, 20, 30),appointment_date = datetime(2018, 11, 21, 11, 20, 30), active_emp = 1, suffix_title = 'MRS', marritial_status = 'MARRIED', mobile_no='21456',basic_salary=10000, account_number="11233565456", role = role3, organization=org2, department = depat3)
emp4 = Employee(first_name="john", last_name = "snow", address = "helsinki", gender = "M",date_of_birth=datetime(1998, 12, 1, 11, 20, 30),appointment_date = datetime(2018, 11, 21, 11, 20, 30), active_emp = 1, suffix_title = 'MR', marritial_status = 'SINGLE', mobile_no='21456',basic_salary=10000, account_number="11233565456", role = role4, organization=org, department = depat)

leav = LeavePlan(leave_type='MEDICAL', leave_date=datetime(2018, 11, 21, 11, 20, 30), employee = emp)
leav2 = LeavePlan(leave_type='CASUAL', leave_date=datetime(2018, 12, 1, 11, 20, 30), employee = emp3)
leav3 = LeavePlan(leave_type='MEDICAL', leave_date=datetime(2018, 1, 25, 11, 20, 30), employee = emp)


db.session.add(role)
db.session.add(role2)
db.session.add(role3)
db.session.add(role4)
db.session.add(role5)
db.session.add(role6)
db.session.add(org)
db.session.add(org2)

db.session.add(depat)
db.session.add(depat2)
db.session.add(depat3)

db.session.add(emp)
db.session.add(emp2)
db.session.add(emp3)
db.session.add(emp4)

db.session.add(leav)
db.session.add(leav2)
db.session.add(leav3)

db.session.commit()


 