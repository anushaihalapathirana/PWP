import React, { useEffect, useState } from "react";
import { Button} from '@material-ui/core';
import { Alert } from '@mui/material';
import Dropdown from 'react-dropdown';
import './home.css'
import {EmployeeForm} from './EmployeeForm';
import {EmployeeTable} from './EmploteeTable';
import 'react-dropdown/style.css';
import { getResource } from "../../services/hrservice";
import { UI_LOADING_STATES } from "../../util/constants";

const Home = () => {
  const [orgState, setOrgState] = useState(UI_LOADING_STATES.INIT);
  const [orgs, setOrgs] = useState([]);
  const [organization, setOrganization] = useState('Select');

  const [depts, setDepts] = useState([]);
  const [department, setDepartment] = useState('Select');

  const [roles, setRoles] = useState([]);
  const [role, setRole] = useState('Select')

  const [employeebyOrgDeptRoleURL, setEmployeebyOrgDeptRoleURL ] = useState([]);
  const [employeebyOrgDeptRoleList, setemployeebyOrgDeptRoleList ] = useState([]);
  const [employeeAllList, setEmployeeAllList ] = useState([]);


  const [employeeAllURL, setEmployeeAllURL ] = useState([]);
  const [isAddEmp, setisAddEmp ] = useState(false);

  const [isShowAllRoles, setIsShowAllRoles] = useState(false);


  useEffect(() => {
    setOrgState(UI_LOADING_STATES.LOADING);
    async function callResource() {
      try {
        let orgBody = await getResource("/api/organizations/");
        let deptsBody = await getResource(orgBody['@controls']['hrsys:departments-all']['href']);
        let rolesBody = await getResource(orgBody['@controls']['hrsys:roles-all']['href']);
        setEmployeebyOrgDeptRoleURL(orgBody['@controls']['hrsys:by-org-dept-role-url-param']['href'])
        setEmployeeAllURL(orgBody['@controls']['hrsys:employee-all']['href'])
        setOrgs(orgBody['items']);
        setDepts(deptsBody['items']);
        setRoles(rolesBody['items']);
        
      } catch (error) {
        setOrgState(UI_LOADING_STATES.ERROR);
      }
    }
    callResource();
  }, []);

  const handleOrganizationChange = (event) => {
    console.log(event)
    setOrganization(event.value.key);
  };

  const handleDepartmentChange = (event) => {
    setDepartment(event.value.key)
  }

  const handleRoleChange = (event) => {
    setRole(event.value.key)
  }

  const replaceTemplateVals = (url) => {
    url = url.replace("{organization}", organization);
    url = url.replace("{department}", department);
    url = url.replace("{role}", role);
    return url
  }

  // employee list by org dept and role
  const getEmployeesList = async () => {
    setisAddEmp(false)
    let url = replaceTemplateVals(employeebyOrgDeptRoleURL)
    let empBody = await getResource(url);
    setEmployeeAllList([])
    setemployeebyOrgDeptRoleList(empBody['items']);

  };

  //  all employee list
  const getAllEmployees = async () => {
    setisAddEmp(false)
    let empBody = await getResource(employeeAllURL)
    setemployeebyOrgDeptRoleList([])
    setEmployeeAllList(empBody['items'])
  }

  const getAllRoles = () => {
    setIsShowAllRoles(true)
  }

  const addEmployee = () => {
    setisAddEmp(true)
  }

  let orgItems = orgs.map((item) =>
      <option key={item.organization_id}>{item.name}</option>
  );

  let deptItems = depts.map((item) =>
      <option key={item.department_id}>{item.name}</option>
  );

  let roleItems = roles.map((item) =>
      <option key={item.code}>{item.name}</option>
  );

  return (
    <div>
      <div className='menu-bar'>
        <div className='drop-down'>
          <Dropdown className='org-drop'
            placeholder='Search categories...'
            label="Select organization"
            options={orgItems}
            value={organization}
            onChange={handleOrganizationChange}
          />
        </div>

        <div className='drop-down'>
          <Dropdown className='dept-drop'
            placeholder='Search categories...'
            label="Select Departments"
            options={deptItems}
            value={department}
            onChange={handleDepartmentChange}
          />
        </div>

        <div className='drop-down'>
          <Dropdown className='dept-drop'
            placeholder='Search categories...'
            label="Select Roles"
            options={roleItems}
            value={role}
            onChange={handleRoleChange}
          />
        </div>

        <div className='btn'>
          <Button className='btn-get-data'
           color="primary"
           variant="contained"
           onClick={getEmployeesList}
          >
            Filter
          </Button>

          <Button className='btn-get-data'
           color="primary"
           variant="outlined"
           onClick={addEmployee}
          >
            Add Employee
          </Button>

          
            <Button className='btn-get-data'
            color="primary"
            variant="contained"
            onClick={getAllEmployees}
            >
              Get All Employees
            </Button>

            <Button className='btn-get-data'
            color="primary"
            variant="contained"
            onClick={getAllRoles}
            >
              Get All Roles
            </Button>

            <Button className='btn-get-data'
            color="primary"
            variant="contained"
            onClick={getAllEmployees}
            >
              Get All Departments
            </Button>

            <Button className='btn-get-data'
            color="primary"
            variant="contained"
            onClick={getAllEmployees}
            >
              Get All Organizations
            </Button>

        </div>

      </div>

      <div className='table-data'>
        {(() => {
          if (organization !== 'Select' && department !== 'Select' && role !== 'Select' && isAddEmp) {
            return (
              <EmployeeForm/>
            )
          } if (organization === 'Select' || department === 'Select' || role === 'Select') {
            return (
              <Alert severity="info">Plese select organization, department and role to add an employee</Alert>
            )
          } if ( employeeAllList.length > 0  && !isAddEmp){
            return (
              <div>
                <EmployeeTable employeeList={employeeAllList}
                />
              </div>
            )
          }
          if (employeebyOrgDeptRoleList.length > 0 && !isAddEmp){
            return (
              <div>
                <EmployeeTable employeeList = {employeebyOrgDeptRoleList}
                />
              </div>
            )
          }
          else {
            return (<div></div>)
          }
        })()}
     
      
      </div>
    </div>
  );
};

export { Home };
