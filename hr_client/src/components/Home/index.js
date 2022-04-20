import React, { useEffect, useState } from "react";
import { Button} from '@material-ui/core';
import { Alert, fabClasses } from '@mui/material';
import Dropdown from 'react-dropdown';
import './home.css'
import {EmployeeForm} from './EmployeeForm';
import {EmployeeTable} from './EmploteeTable';
import 'react-dropdown/style.css';
import { getResource, deleteResource, addResource } from "../../services/hrservice";
import { UI_LOADING_STATES } from "../../util/constants";
import { RoleTable } from "./RoleTable";
import {DepartmentTable} from "./DepartmentTable";
import {OrganizationTable} from "./OrganizationTable";
import {AddForm} from "./AddForm";

const Home = () => {
  const [orgState, setOrgState] = useState(UI_LOADING_STATES.INIT);
  const [orgs, setOrgs] = useState([]);
  const [organization, setOrganization] = useState('Select');

  const [depts, setDepts] = useState([]);
  const [department, setDepartment] = useState('Select');

  const [roles, setRoles] = useState([]);
  const [role, setRole] = useState('Select')

  const [employeebyOrgDeptRoleURL, setEmployeebyOrgDeptRoleURL ] = useState([]);
  const [employeeAllURL, setEmployeeAllURL ] = useState([]);
  const [roleAllURL, setRoleAllURL ] = useState([]);
  const [deptAllURL, setDeptAllURL ] = useState([]);
  const [orgAllURL, setOrgAllURL ] = useState([]);

  const [employeebyOrgDeptRoleList, setemployeebyOrgDeptRoleList ] = useState([]);
  const [employeeAllList, setEmployeeAllList ] = useState([]);


  const [isAddEmp, setisAddEmp ] = useState(false);

  const [isShowAllEmps, setIsShowAllEmps] = useState(false);
  const [isShowAllRoles, setIsShowAllRoles] = useState(false);
  const [isShowAllDepts, setIsShowAllDepts] = useState(false);
  const [isShowAllOrgs, setIsShowAllOrgs] = useState(false);
  const [isDisplayAddForm, setIsDisplayAddForm] = useState(false);
  const [errorMsg, setErrorMsg] = useState(false);


  

  useEffect(() => {
    setOrgState(UI_LOADING_STATES.LOADING);
    async function callResource() {
      try {
        let orgBody = await getResource("/api/organizations/");
        let deptsBody = await getResource(orgBody['@controls']['hrsys:departments-all']['href']);
        let rolesBody = await getResource(orgBody['@controls']['hrsys:roles-all']['href']);
        setEmployeebyOrgDeptRoleURL(orgBody['@controls']['hrsys:by-org-dept-role-url-param']['href'])
        setEmployeeAllURL(orgBody['@controls']['hrsys:employee-all']['href'])
        setRoleAllURL(orgBody['@controls']['hrsys:roles-all']['href'])
        setDeptAllURL(orgBody['@controls']['hrsys:departments-all']['href'])
        setOrgAllURL('/api/organizations/')

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
    setIsShowAllRoles(false)
    setIsShowAllDepts(false)
    setIsShowAllOrgs(false)
    setIsShowAllEmps(false)
    setIsDisplayAddForm(false)
    setErrorMsg('')

  };

  //  all employee list
  const getAllEmployees = async () => {
    setisAddEmp(false)
    setIsShowAllEmps(true)
    let empBody = await getResource(employeeAllURL)
    setemployeebyOrgDeptRoleList([])
    setEmployeeAllList(empBody['items'])
    setIsShowAllRoles(false)
    setIsShowAllDepts(false)
    setIsShowAllOrgs(false)
    setIsDisplayAddForm(false)
    setErrorMsg('')

    
  }

  const getAllRoles = () => {
    setIsShowAllRoles(true)
    setIsShowAllDepts(false)
    setIsShowAllOrgs(false)
    setisAddEmp(false)
    setIsShowAllEmps(false)
    setIsDisplayAddForm(false)
    setErrorMsg('')

  }

  const getAllDepts = () => {
    setIsShowAllRoles(false)
    setIsShowAllDepts(true)
    setIsShowAllOrgs(false)
    setisAddEmp(false)
    setIsShowAllEmps(false)
    setIsDisplayAddForm(false)
    setErrorMsg('')

  }

  const getAllOrgs = () => {
    setIsShowAllRoles(false)
    setIsShowAllDepts(false)
    setIsShowAllOrgs(true)
    setisAddEmp(false)
    setIsShowAllEmps(false)
    setIsDisplayAddForm(false)
    setErrorMsg('')

  }

  const addEmployee = () => {
    setErrorMsg('')
    if((organization === 'Select' || department === 'Select' || role === 'Select') && isAddEmp) {
      setErrorMsg('Please select organization, department and role to add employee')
    }
    setisAddEmp(true)
    setIsShowAllRoles(false)
    setIsShowAllDepts(false)
    setIsShowAllOrgs(false)
    setIsShowAllEmps(false)
    setIsDisplayAddForm(false)
  }

  const handleCellClickDelete = async(data) => {
    let del = await deleteResource(data);
    let rolesBody = await getResource(roleAllURL);
    setRoles(rolesBody['items']);
  }

  const onDeleteOrg = async(data) => {
    let del = await deleteResource(data);
    let orgBody = await getResource(orgAllURL);
    setOrgs(orgBody['items']);
  }

  const onDeleteDept = async(data) => {
    let del = await deleteResource(data);
    let deptBody = await getResource(deptAllURL);
    setDepts(deptBody['items']);
  }

  const onClickAddRole = () => {
    setIsDisplayAddForm(true)
    setErrorMsg('')
  }

  const submitRole =  async(e) => {
    e.preventDefault();
    let code = e.target.id.value;
    let name = e.target.name.value;
    let desc = e.target.desc.value;

    console.log(code, name, desc)
    let body = {
      code:code,
      name:name,
      description:desc
    }
    let res = await addResource(roleAllURL, body);
    let roleBody = await getResource(roleAllURL);
    setRoles(roleBody['items']);
    if (res && res.ok) {
      setIsShowAllRoles(true)
      setIsDisplayAddForm(false)

    } else if (res && !res.ok) {
      let err = res.status +' '+res.statusText
      setErrorMsg(err)
    }
  };

  const onClickEditRole = async(data) => {
    console.log(data)
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
            onClick={getAllDepts}
            >
              Get All Departments
            </Button>

            <Button className='btn-get-data'
            color="primary"
            variant="contained"
            onClick={getAllOrgs}
            >
              Get All Organizations
            </Button>

        </div>

      </div>

      <div className='table-data'>
        {(() => {
          if(errorMsg) {
            return (
              <Alert severity="error">{errorMsg}</Alert>
            )
          }
          if (organization !== 'Select' && department !== 'Select' && role !== 'Select' && isAddEmp) {
            return (
              <EmployeeForm/>
            )
          } 
          if ( employeeAllList.length > 0  && isShowAllEmps){
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
          if (isDisplayAddForm) {
            return (
              <div>
                <AddForm
                  title={'Add Role'}
                  labelid={'Role Code'}
                  nameid={'code'}
                  label={'Role Name'}
                  name={'name'}
                  labeldesc={'Role Description'}
                  namedesc={'description'}
                  onSubmit = {submitRole}
                />
              </div>
            )
          }
          if (isShowAllRoles &&  roles.length >0) {
            return (
              <div>
                <RoleTable 
                data = {roles}
                onClickDelete={handleCellClickDelete}
                onClickEdit = {onClickEditRole}
                onClickAdd = {onClickAddRole}
                />
              </div>
            )
          }
          if (isShowAllDepts &&  depts.length >0) {
            return (
              <div>
                <DepartmentTable data = {depts}
                onClickDelete={onDeleteDept}/>
              </div>
            )
          }
          if (isShowAllOrgs &&  orgs.length >0) {
            return (
              <div>
                <OrganizationTable data = {orgs}
                onClickDelete={onDeleteOrg}/>
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
