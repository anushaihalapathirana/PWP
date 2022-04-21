import React, { useEffect, useState } from "react";
import { Alert, fabClasses } from "@mui/material";
import Dropdown from "react-dropdown";
import "./home.css";
import "react-dropdown/style.css";
import {
  getResource,
  deleteResource,
  addResource,
} from "../../services/hrservice";
import { AddForm } from "./AddForm";

import "./home.css";
import "react-dropdown/style.css";
import {
  AppBar,
  Box,
  Button,
  Divider,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Toolbar,
  Typography,
} from "@material-ui/core";
import "./home.css";
import { EmployeeForm } from "./EmployeeForm";
import { EmployeeTable } from "./EmploteeTable";
import "react-dropdown/style.css";
import { APP_PATH, UI_LOADING_STATES } from "../../util/constants";
import { EmployeeHome } from "../Employee";
import { RoleHome } from "../Role";
import { AddEmployee } from "../Employee/AddEmployee";
import { ViewEmployee } from "../Employee/ViewEmployee";
import { OrgHome } from "../Org";
import { DeptHome } from "../Dept";

const Home = () => {
  const [appPath, setAppPath] = useState(APP_PATH.EMPLOYEE_HOME);

  const [orgState, setOrgState] = useState(UI_LOADING_STATES.INIT);
  const [orgs, setOrgs] = useState([]);
  const [organization, setOrganization] = useState("Select");

  const [depts, setDepts] = useState([]);
  const [department, setDepartment] = useState("Select");

  const [roles, setRoles] = useState([]);
  const [role, setRole] = useState("Select");

  const [isAddEmp, setisAddEmp] = useState(false);
  const [employeebyOrgDeptRoleList, setemployeebyOrgDeptRoleList] = useState(
    []
  );
  const [employeeAllList, setEmployeeAllList] = useState([]);

  const [employeebyOrgDeptRoleURL, setEmployeebyOrgDeptRoleURL] = useState([]);
  const [employeeAllURL, setEmployeeAllURL] = useState([]);
  const [roleAllURL, setRoleAllURL] = useState([]);
  const [deptAllURL, setDeptAllURL] = useState([]);
  const [orgAllURL, setOrgAllURL] = useState([]);

  const [isShowAllEmps, setIsShowAllEmps] = useState(false);
  const [isShowAllRoles, setIsShowAllRoles] = useState(false);
  const [isShowAllDepts, setIsShowAllDepts] = useState(false);
  const [isShowAllOrgs, setIsShowAllOrgs] = useState(false);
  const [isDisplayAddForm, setIsDisplayAddForm] = useState(false);
  const [errorMsg, setErrorMsg] = useState(false);

  const [employeeControl, setEmployeeControl] = useState();

  const [currentEmployee, setCurrentEmployee] = useState();

  useEffect(() => {
    setOrgState(UI_LOADING_STATES.LOADING);
    async function callResource() {
      try {
        let orgBody = await getResource("/api/organizations/");
        let deptsBody = await getResource(
          orgBody["@controls"]["hrsys:departments-all"]["href"]
        );
        let rolesBody = await getResource(
          orgBody["@controls"]["hrsys:roles-all"]["href"]
        );
        setEmployeebyOrgDeptRoleURL(
          orgBody["@controls"]["hrsys:by-org-dept-role-url-param"]["href"]
        );
        setEmployeeAllURL(orgBody["@controls"]["hrsys:employee-all"]["href"]);
        setRoleAllURL(orgBody["@controls"]["hrsys:roles-all"]["href"]);
        setDeptAllURL(orgBody["@controls"]["hrsys:departments-all"]["href"]);
        setOrgAllURL("/api/organizations/");

        setOrgs(orgBody["items"]);
        setDepts(deptsBody["items"]);
        setRoles(rolesBody["items"]);
      } catch (error) {
        setOrgState(UI_LOADING_STATES.ERROR);
      }
    }
    callResource();
  }, []);

  const handleOrganizationChange = (event) => {
    console.log(event);
    setOrganization(event.value.key);
  };

  const handleDepartmentChange = (event) => {
    setDepartment(event.value.key);
  };

  const handleRoleChange = (event) => {
    setRole(event.value.key);
  };

  const replaceTemplateVals = (url, organization, department, role) => {
    if (organization) {
      url = url.replace("{organization}", organization);
    }
    if (department) {
      url = url.replace("{department}", department);
    }
    if (url) {
      url = url.replace("{role}", role);
    }
    return url;
  };

  const getEmployees = async (org, dept, role) => {
    let url = employeeAllURL;

    if (org != "Select" && dept != "Select" && role != "Select") {
      url = employeebyOrgDeptRoleURL;
    }
    url = replaceTemplateVals(url, org, dept, role);
    let empBody = await getResource(url);
    setEmployeeAllList(empBody["items"]);
    console.log(empBody);
    setEmployeeControl(empBody["@controls"]);
  };
  // employee list by org dept and role
  const getEmployeesList = async () => {
    setisAddEmp(false);
    let url = replaceTemplateVals(employeebyOrgDeptRoleURL);
    let empBody = await getResource(url);
    setEmployeeAllList([]);
    setemployeebyOrgDeptRoleList(empBody["items"]);
    setIsShowAllRoles(false);
    setIsShowAllDepts(false);
    setIsShowAllOrgs(false);
    setIsShowAllEmps(false);
    setIsDisplayAddForm(false);
    setErrorMsg("");
  };

  //  all employee list
  const getAllEmployees = async () => {
    setAppPath(APP_PATH.EMPLOYEE_HOME);
    setisAddEmp(false);
    setIsShowAllEmps(true);
    let empBody = await getResource(employeeAllURL);
    setemployeebyOrgDeptRoleList([]);
    setEmployeeAllList(empBody["items"]);
    setIsShowAllRoles(false);
    setIsShowAllDepts(false);
    setIsShowAllOrgs(false);
    setIsDisplayAddForm(false);
    setErrorMsg("");
  };

  const getAllRoles = () => {
    setAppPath(APP_PATH.ROLE_HOME);
    setIsShowAllRoles(true);
    setIsShowAllDepts(false);
    setIsShowAllOrgs(false);
    setisAddEmp(false);
    setIsShowAllEmps(false);
    setIsDisplayAddForm(false);
    setErrorMsg("");
  };

  const getAllDepts = () => {
    setAppPath(APP_PATH.DEPT_HOME);
    setIsShowAllRoles(false);
    setIsShowAllDepts(true);
    setIsShowAllOrgs(false);
    setisAddEmp(false);
    setIsShowAllEmps(false);
    setIsDisplayAddForm(false);
    setErrorMsg("");
  };

  const getAllOrgs = () => {
    setAppPath(APP_PATH.ORG_HOME);
    setIsShowAllRoles(false);
    setIsShowAllDepts(false);
    setIsShowAllOrgs(true);
    setisAddEmp(false);
    setIsShowAllEmps(false);
    setIsDisplayAddForm(false);
    setErrorMsg("");
  };

  const addEmployee = () => {
    setAppPath(APP_PATH.ADD_EMPLOYEE);
  };

  const handleAddEmployee = async (url, body) => {
    let res = await addResource(url, body);
    if (res) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
    }
  };

  // const getEmployees = async (org, dept, role) => {
  //   let url = employeeAllURL;

  //   if (org != "Select" && dept != "Select" && role != "Select") {
  //     url = employeebyOrgDeptRoleURL;
  //   }
  //   url = replaceTemplateVals(url, org, dept, role);
  //   let empBody = await getResource(url);
  //   setEmployeeAllList(empBody["items"]);
  // };

  // const addEmployee = () => {
  //   setErrorMsg('')
  //   if((organization === 'Select' || department === 'Select' || role === 'Select') && isAddEmp) {
  //     setErrorMsg('Please select organization, department and role to add employee')
  //   }
  //   setisAddEmp(true)
  //   setIsShowAllRoles(false)
  //   setIsShowAllDepts(false)
  //   setIsShowAllOrgs(false)
  //   setIsShowAllEmps(false)
  //   setIsDisplayAddForm(false)
  // }

  const onDeleteRole = async (data) => {
    let del = await deleteResource(data);
    let rolesBody = await getResource(roleAllURL);
    setRoles(rolesBody["items"]);
  };

  const onDeleteOrg = async (data) => {
    let del = await deleteResource(data);
    let orgBody = await getResource(orgAllURL);
    setOrgs(orgBody["items"]);
  };

  const handleEditEmployee = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
    }
  };

  const viewEmployee = (employee) => {
    setCurrentEmployee(employee);
    setAppPath(APP_PATH.VIEW_EMPLOYEE);
  };

  const onDeleteDept = async (data) => {
    let del = await deleteResource(data);
    let deptBody = await getResource(deptAllURL);
    setDepts(deptBody["items"]);
  };

  const onClickAddRole = () => {
    setIsDisplayAddForm(true);
    setErrorMsg("");
  };

  const submitRole = async (e) => {
    e.preventDefault();
    let code = e.target.id.value;
    let name = e.target.name.value;
    let desc = e.target.desc.value;

    console.log(code, name, desc);
    let body = {
      code: code,
      name: name,
      description: desc,
    };
    let res = await addResource(roleAllURL, body);
    let roleBody = await getResource(roleAllURL);
    setRoles(roleBody["items"]);
    if (res && res.ok) {
      setIsShowAllRoles(true);
      setIsDisplayAddForm(false);
    } else if (res && !res.ok) {
      let err = res.status + " " + res.statusText;
      setErrorMsg(err);
    }
  };

  const onEditRole = async (data) => {
    console.log(data);
  };

  const onEditOrg = async (data) => {
    console.log(data);
  };

  const onEditDept = async (data) => {
    console.log(data);
  };

  const onAddOrg = async (data) => {
    console.log(data);
  };

  const onAddDept = async (data) => {
    console.log(data);
  };

  let orgItems = orgs.map((item) => (
    <option key={item.organization_id}>{item.name}</option>
  ));

  let deptItems = depts.map((item) => (
    <option key={item.department_id}>{item.name}</option>
  ));

  let roleItems = roles.map((item) => (
    <option key={item.code}>{item.name}</option>
  ));
  let drawerWidth = 240;

  const getRenderRoute = (path) => {
    switch (path) {
      case APP_PATH.EMPLOYEE_HOME:
        return (
          <EmployeeHome
            orgList={{
              items: orgs,
            }}
            deptList={{
              items: depts,
            }}
            roleList={{
              items: roles,
            }}
            employeeList={{
              items: employeeAllList,
              get: getEmployees,
              add: addEmployee,
            }}
            employeeControl={employeeControl}
            viewEmployee={viewEmployee}
          ></EmployeeHome>
        );

      case APP_PATH.ADD_EMPLOYEE:
        return (
          <AddEmployee
            addEmployeeControl={employeeControl["hrsys:add-employee"]}
            addEmployee={handleAddEmployee}
          ></AddEmployee>
        );
      case APP_PATH.VIEW_EMPLOYEE:
        return (
          <ViewEmployee
            employee={currentEmployee}
            editEmployee={handleEditEmployee}
          ></ViewEmployee>
        );
      case APP_PATH.ROLE_HOME:
        return (
          <RoleHome
            roleList={{
              items: roles,
              edit: onEditRole,
              delete: onDeleteRole,
              add: onClickAddRole,
            }}
          ></RoleHome>
        );
      case APP_PATH.ORG_HOME:
        return (
          <OrgHome
            orgList={{
              items: orgs,
              delete: onDeleteOrg,
              get: onEditOrg,
              add: onAddOrg,
            }}
          ></OrgHome>
        );
      case APP_PATH.DEPT_HOME:
        return (
          <DeptHome
            deptList={{
              items: depts,
              delete: onDeleteDept,
              get: onEditDept,
              add: onAddDept,
            }}
          ></DeptHome>
        );
      default:
        return <RoleHome></RoleHome>;
    }
  };

  return (
    <div>
      <Box style={{ display: "flex" }}>
        <AppBar
          position="fixed"
          style={{
            width: `calc(100% - 240px)`,
            marginLeft: `240px`,
          }}
        >
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              HR System
            </Typography>
          </Toolbar>
        </AppBar>

        <Drawer
          sx={{
            width: 240,
          }}
          variant="permanent"
          anchor="left"
        >
          <div
            style={{
              width: "240px",
            }}
          >
            <Toolbar />

            <List>
              <ListItem button onClick={getAllEmployees}>
                <ListItemText primary={"Employees"} />
              </ListItem>
              <Divider />
              <ListItem button onClick={getAllRoles}>
                <ListItemText primary={"Roles"} />
              </ListItem>
              <Divider />
              <ListItem button onClick={getAllDepts}>
                <ListItemText primary={"Departments"} />
              </ListItem>
              <Divider />
              <ListItem button onClick={getAllOrgs}>
                <ListItemText primary={"Organizations"} />
              </ListItem>
            </List>
          </div>
        </Drawer>
        {getRenderRoute(appPath)}
      </Box>

      {/* {getRenderRoute(appPath)} */}
    </div>
  );
};

export { Home };
