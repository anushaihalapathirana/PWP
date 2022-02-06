# this script use to enter data to the payroll database
from payrollModel import db
from payrollModel import Payroll
from datetime import datetime

db.create_all()
payroll = Payroll(date=datetime(2018, 12, 21, 11, 20, 30), amount = 125553, employee_id = 1)
payroll2 = Payroll(date=datetime(2018, 11, 21, 11, 20, 30), amount = 125553, employee_id = 1)
payroll3 = Payroll(date=datetime(2018, 10, 21, 11, 20, 30), amount = 125553, employee_id = 1)
payroll4 = Payroll(date=datetime(2018, 9, 21, 11, 20, 30), amount = 125553, employee_id = 1)
payroll5 = Payroll(date=datetime(2018, 12, 21, 11, 20, 30), amount = 125553, employee_id = 2)
payroll6 = Payroll(date=datetime(2018, 11, 21, 11, 20, 30), amount = 125553, employee_id = 2)
payroll7 = Payroll(date=datetime(2018, 12, 21, 11, 20, 30), amount = 125553, employee_id = 3)
payroll8 = Payroll(date=datetime(2018, 12, 21, 11, 20, 30), amount = 125553, employee_id = 4)

db.session.add(payroll)
db.session.add(payroll2)
db.session.add(payroll3)
db.session.add(payroll4)
db.session.add(payroll5)
db.session.add(payroll6)
db.session.add(payroll7)
db.session.add(payroll8)

db.session.commit()