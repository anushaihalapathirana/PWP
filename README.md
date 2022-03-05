# PWP SPRING 2021
# Human Resource Management System
# Group information

* Student 1. Anusha Ihalapathirana - aihalapa20@student.oulu.fi
* Student 2. Sameera Wickramasekara - spandith21@student.oulu.fi

# Setup database

The database we are using for the project is SQLAlchemy version 1.4

- Requirements : Python3, Pip

- Libraries used : flask, flask_sqlalchemy

Please install all the dependencies using
```  
    pip install -r requirements.txt
```
# Setup database

Our system contains with 2 databases. HR Core database and Payroll database.

Follow below instructions to setup the databases

***Note*** : _the sqlite db files are already present in the project (hrcodedb and payrolldb). Please delete them first to run these scripts_


1. __init__.py file contains the script to create the HRCore database and then insert data to the database. You can change/add/delete insert values in there.

```  
    flask init-db
    flask testgen
```

2. run payrolldb_data_script.py file using below command. it will generate the payroll database and insert data to the table.

```
    python payrolldb_data_script.py
```

More details about the database can be found here - https://github.com/anushaihalapathirana/PWP/wiki/Database-design-and-implementation


# Code quality

This project use Pylint for code quality.

Run below command to run pylint

``` 
    pylint HRSystem
```

# How to run tests

Run database tests using below command

```
    python3 -m pytest tests/db_test.py 
```


Test coverage using 

```
    python3 -m pytest --cov=PWP
```
