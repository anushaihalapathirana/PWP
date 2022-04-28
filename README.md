# PWP SPRING 2021
# Human Resource Management System
# Group information

* Student 1. Anusha Ihalapathirana - aihalapa20@student.oulu.fi
* Student 2. Sameera Wickramasekara - spandith21@student.oulu.fi

# Setup Libraries and configs

The database we are using for the project is SQLAlchemy version 1.4

- Requirements : Python3, Pip

- Libraries used : flask, flask_sqlalchemy

Clone the project using below command

``` git clone https://github.com/anushaihalapathirana/PWP.git```

Please install all the dependencies using
```  
    pip install -r requirements.txt
```

Configurations - If necessary

```
export FLASK_ENV=development
export FLASK_APP=hr_system
```

# Setup database

Our system contains with 2 databases. HR Core database and Payroll database.

This project only contains HR core API

Follow below instructions to setup the databases

***Note*** : _the sqlite db files are already present in the project (hrcodedb). Please delete them first to run these scripts_


1. __init__.py file contains the script to create the HRCore database and then insert data to the database. You can change/add/delete insert values in there.

```  
    flask init-db
    flask testgen
```

More details about the database can be found here - https://github.com/anushaihalapathirana/PWP/wiki/Database-design-and-implementation

# How to run API

Use below commands to run API

```
flask run
```

Development server will run on http://127.0.0.1:5000/

Swagger API documentation can found in http://127.0.0.1:5000/apidocs/


# Code quality

Note - Please note these commands are exicuted of linux environment

This project use Pylint for code quality.

Install pylit using below command

```
pip install pylint
```

Run below command to run pylint in project

``` 
pylint hr_system
```

# How to run tests

Note - Please note these commands are exicuted of linux environment

How to install required libries for testing - pytest, pytest-cov

```
pip install pytest
pip install pytest-cov
```

Run database tests and api tests using below command

```
python3 -m pytest tests/db_test.py 
python3 -m pytest tests/api_test.py 
```


Test coverage using 

```
python3 -m pytest --cov=.
```

Test coverage html report - You can view test coverage report by using below command.

```
python3 -m pytest --cov-report html --cov=.
```

test cases can be use to detect 400, 404, 409, 415 and 403 errors

# Run swagger

Install flasgger and pyyaml. These are covered in requirement.txt file

```
pip install flasgger
pip install pyyaml
```

Run the application using ``` flask run ``` command and you can access swagger in http://127.0.0.1:5000/apidocs/

# Setup and run client

Client written in React JS. Install Node and react (Tutorial - https://www.codecademy.com/article/react-setup-i)

use below commands to setup react and run client

```
cd hr_client
npm install
npm start
```

client will up and run in http://localhost:3000/

ESlint is set up for client. Run below command to run eslint

```
cd hr_client
npm run eslint-run
```

