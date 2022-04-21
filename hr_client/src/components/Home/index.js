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
import "react-dropdown/style.css";
import { APP_PATH, UI_LOADING_STATES } from "../../util/constants";
import { EmployeeHome } from "../Employee";
import { RoleHome } from "../Role";
import { AddEmployee } from "../Employee/AddEmployee";
import { ViewEmployee } from "../Employee/ViewEmployee";
import { OrgHome } from "../Org";
import { DeptHome } from "../Dept";
import { ViewRole } from "../Role/ViewRole";
import { AddRole } from "../Role/AddRole";
import { AddOrg } from "../Org/AddOrg";
import { ViewOrg } from "../Org/ViewOrg";
import { AddDept } from "../Dept/AddDept";
import { ViewDept } from "../Dept/ViewDept";

const Home = () => {
  const [appPath, setAppPath] = useState(APP_PATH.EMPLOYEE_HOME);

  const [orgState, setOrgState] = useState(UI_LOADING_STATES.INIT);
  const [orgs, setOrgs] = useState([]);
  const [depts, setDepts] = useState([]);
  const [roles, setRoles] = useState([]);

  const [employeeAllList, setEmployeeAllList] = useState([]);

  const [employeebyOrgDeptRoleURL, setEmployeebyOrgDeptRoleURL] = useState([]);
  const [employeeAllURL, setEmployeeAllURL] = useState([]);
  const [roleAllURL, setRoleAllURL] = useState([]);
  const [deptAllURL, setDeptAllURL] = useState([]);
  const [orgAllURL, setOrgAllURL] = useState([]);

  const [errorMsg, setErrorMsg] = useState(false);

  const [employeeControl, setEmployeeControl] = useState();
  const [roleControl, setRoleControl] = useState();
  const [orgControl, setOrgControl] = useState();
  const [deptControl, setDeptControl] = useState();


  const [currentEmployee, setCurrentEmployee] = useState();
  const [currentRole, setCurrentRole] = useState();
  const [currentOrg, setCurrentOrg] = useState();
  const [currentDept, setCurrentDept] = useState();


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
        setRoleControl(rolesBody["@controls"]);
        setOrgControl(orgBody["@controls"]);
        setDeptControl(deptsBody["@controls"]);

      } catch (error) {
        setOrgState(UI_LOADING_STATES.ERROR);
      }
    }
    callResource();
  }, []);

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

  //  all employee list
  const getAllEmployees = async () => {
    setAppPath(APP_PATH.EMPLOYEE_HOME);
    let empBody = await getResource(employeeAllURL);
    setEmployeeAllList(empBody["items"]);
    setErrorMsg("");
  };

  const getAllRoles = async () => {
    setAppPath(APP_PATH.ROLE_HOME);
    let roleBody = await getResource(roleAllURL);
    setRoles(roleBody["items"]);
    setErrorMsg("");
  };

  const getAllDepts = async () => {
    setAppPath(APP_PATH.DEPT_HOME);
    let deptBody = await getResource(deptAllURL);
    setDepts(deptBody["items"]);
    setErrorMsg("");
  };

  const getAllOrgs = async() => {
    setAppPath(APP_PATH.ORG_HOME);
    let orgBody = await getResource(orgAllURL);
    setOrgs(orgBody["items"]);
    setErrorMsg("");
  };

  const addEmployee = () => {
    setAppPath(APP_PATH.ADD_EMPLOYEE);
  };

  const addRole = () => {
    setAppPath(APP_PATH.ADD_ROLE);
  };

  const addOrg = () => {
    setAppPath(APP_PATH.ADD_ORG);
  };

  const addDept = () => {
    setAppPath(APP_PATH.ADD_DEPT);
  };

  const handleAddEmployee = async (url, body) => {
    let res = await addResource(url, body);
    if (res) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
    }
  };

  const handleAddRole = async (url, body) => {
    let res = await addResource(url, body);
    if (res) {
      setAppPath(APP_PATH.ROLE_HOME);
      getAllRoles();
    }
  };

  const handleAddOrg = async (url, body) => {
    let res = await addResource(url, body);
    if (res) {
      setAppPath(APP_PATH.ORG_HOME);
      getAllOrgs();
    }
  };

  const handleAddDept = async (url, body) => {
    let res = await addResource(url, body);
    if (res) {
      setAppPath(APP_PATH.DEPT_HOME);
      getAllDepts();
    }
  };

  const handleEditEmployee = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
    }
  };

  const handleEditRole = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res) {
      setAppPath(APP_PATH.ROLE_HOME);
      getAllRoles();
    }
  };

  const handleEditOrg = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res) {
      setAppPath(APP_PATH.ORG_HOME);
      getAllOrgs();
    }
  };

  const handleEditDept = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res) {
      setAppPath(APP_PATH.DEPT_HOME);
      getAllDepts();
    }
  };

  const viewEmployee = (employee) => {
    setCurrentEmployee(employee);
    setAppPath(APP_PATH.VIEW_EMPLOYEE);
  };

  const viewRole = (role) => {
    setCurrentRole(role);
    setAppPath(APP_PATH.VIEW_ROLE);
  };

  const viewOrg = (org) => {
    setCurrentOrg(org);
    setAppPath(APP_PATH.VIEW_ORG);
  };

  const viewDept = (dept) => {
    setCurrentDept(dept);
    setAppPath(APP_PATH.VIEW_DEPT);
  };

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
              add: addRole,
            }}
            viewRole={viewRole}
            roleControl={roleControl}
          ></RoleHome>
        );
      case APP_PATH.ADD_ROLE:
        return (
          <AddRole
            addRoleControl={roleControl["hrsys:add-role"]}
            addRole={handleAddRole}
          ></AddRole>
        );
      case APP_PATH.VIEW_ROLE:
        return (
          <ViewRole
            role={currentRole}
            editRole={handleEditRole}
          ></ViewRole>
          );
      case APP_PATH.ORG_HOME:
        return (
          <OrgHome
            orgList={{
              items: orgs,
              add: addOrg,
            }}
            viewOrg={viewOrg}
            orgControl={orgControl}
          ></OrgHome>
        );
      case APP_PATH.ADD_ORG:
        return (
          <AddOrg
            addOrgControl={orgControl["hrsys:add-organization"]}
            addOrg={handleAddOrg}
          ></AddOrg>
        );
      case APP_PATH.VIEW_ORG:
        return (
          <ViewOrg
            org={currentOrg}
            editOrg={handleEditOrg}
          ></ViewOrg>
          );
      case APP_PATH.DEPT_HOME:
        return (
          <DeptHome
            deptList={{
              items: depts,
              add: addDept,
            }}
            viewDept={viewDept}
            deptControl={deptControl}
          ></DeptHome>
        );
      case APP_PATH.ADD_DEPT:
        return (
          <AddDept
            addDeptControl={deptControl["hrsys:add-dept"]}
            addDept={handleAddDept}
          ></AddDept>
        );
      case APP_PATH.VIEW_DEPT:
        return (
          <ViewDept
            dept={currentDept}
            editDept={handleEditDept}
          ></ViewDept>
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
