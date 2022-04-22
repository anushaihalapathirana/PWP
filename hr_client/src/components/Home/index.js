import React, { useEffect, useState } from "react";
import "./home.css";
import "react-dropdown/style.css";
import {
  getResource,
  deleteResource,
  addResource,
} from "../../services/hrservice";
import "./home.css";
import "react-dropdown/style.css";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import {
  AppBar,
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
import { ViewLeave } from "../Leave/ViewLeave";
import { AddOrg } from "../Org/AddOrg";
import { ViewOrg } from "../Org/ViewOrg";
import { AddDept } from "../Dept/AddDept";
import { ViewDept } from "../Dept/ViewDept";
import { AddLeave } from "../Leave/AddLeave";

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

  const [errorMsg, setErrorMsg] = useState([]);
  const [errorTitle, setErrorTitle] = useState([]);
  const [isError, setIsError] = useState(false);

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

    if (org !== "Select" && dept !== "Select" && role !== "Select") {
      url = employeebyOrgDeptRoleURL;
    }
    url = replaceTemplateVals(url, org, dept, role);
    let empBody = await getResource(url);
    if(empBody["items"]){
      setEmployeeAllList(empBody["items"]);
      setEmployeeControl(empBody["@controls"]);
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (empBody && empBody["@controls"] && empBody["@error"]) {
      let err = empBody["@error"]["@messages"][0];
      setErrorTitle(empBody["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  //  all employee list
  const getAllEmployees = async () => {
    setAppPath(APP_PATH.EMPLOYEE_HOME);
    let empBody = await getResource(employeeAllURL);
    if(empBody["items"]) {
      setEmployeeControl(empBody["@controls"]);
      setEmployeeAllList(empBody["items"]);
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (empBody && empBody["@controls"] && empBody["@error"]) {
      let err = empBody["@error"]["@messages"][0];
      setErrorTitle(empBody["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const getAllRoles = async () => {
    setAppPath(APP_PATH.ROLE_HOME);
    let roleBody = await getResource(roleAllURL);
    if(roleBody["items"]) {
      setRoles(roleBody["items"]);
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (roleBody && roleBody["@controls"] && roleBody["@error"]) {
      let err = roleBody["@error"]["@messages"][0];
      setErrorTitle(roleBody["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const getAllDepts = async () => {
    setAppPath(APP_PATH.DEPT_HOME);
    let deptBody = await getResource(deptAllURL);
    if(deptBody["items"]) {
      setDepts(deptBody["items"]);
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (deptBody && deptBody["@controls"] && deptBody["@error"]) {
      let err = deptBody["@error"]["@messages"][0];
      setErrorTitle(deptBody["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
    
  };

  const getAllOrgs = async () => {
    setAppPath(APP_PATH.ORG_HOME);
    let orgBody = await getResource(orgAllURL);
    if(orgBody["items"]) {
      setOrgs(orgBody["items"]);
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (orgBody && orgBody["@controls"] && orgBody["@error"]) {
      let err = orgBody["@error"]["@messages"][0];
      setErrorTitle(orgBody["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const addEmployee = () => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false);
    setAppPath(APP_PATH.ADD_EMPLOYEE);
  };

  const addRole = () => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false);
    setAppPath(APP_PATH.ADD_ROLE);
  };

  const addOrg = () => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false);
    setAppPath(APP_PATH.ADD_ORG);
  };

  const addDept = () => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false);
    setAppPath(APP_PATH.ADD_DEPT);
  };

  const addLeave = () => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false);
    setAppPath(APP_PATH.ADD_LEAVE);
  };  

  const handleAddEmployee = async (url, body) => {
    let res = await addResource(url, body);
    if (res === true) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleAddRole = async (url, body) => {
    let res = await addResource(url, body);
    if (res === true) {
      setAppPath(APP_PATH.ROLE_HOME);
      getAllRoles();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleAddOrg = async (url, body) => {
    let res = await addResource(url, body);
    if (res === true) {
      setAppPath(APP_PATH.ORG_HOME);
      getAllOrgs();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleAddDept = async (url, body) => {
    let res = await addResource(url, body);
    if (res === true) {
      setAppPath(APP_PATH.DEPT_HOME);
      getAllDepts();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleAddLeave = async (url, body) => {
    let res = await addResource(url, body);
    if (res === true) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleEditEmployee = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res === true) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleEditRole = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res === true) {
      setAppPath(APP_PATH.ROLE_HOME);
      getAllRoles();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleDeleteRole = async (url, method) => {
    let res = await deleteResource(url, method);
    if (res === true) {
      setAppPath(APP_PATH.ROLE_HOME);
      getAllRoles();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleDeleteOrg = async (url, method) => {
    let res = await deleteResource(url, method);
    if (res === true) {
      setAppPath(APP_PATH.ORG_HOME);
      getAllOrgs();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const viewEmployeeLeaves = (employee) => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false)
    setAppPath(APP_PATH.VIEW_LEAVE);
  };

  const handleDeleteDept = async (url, method) => {
    let res = await deleteResource(url, method);
    if (res === true) {
      setAppPath(APP_PATH.DEPT_HOME);
      getAllDepts();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleDeleteEmployee = async (url, method) => {
    let res = await deleteResource(url, method);
    if (res === true) {
      setAppPath(APP_PATH.EMPLOYEE_HOME);
      getAllEmployees();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleEditOrg = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res === true) {
      setAppPath(APP_PATH.ORG_HOME);
      getAllOrgs();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const handleEditDept = async (url, body) => {
    let res = await addResource(url, body, "PUT");
    if (res === true) {
      setAppPath(APP_PATH.DEPT_HOME);
      getAllDepts();
      setErrorTitle([]);
      setErrorMsg([]);
      setIsError(false)
    } else if (res && res["@controls"] && res["@error"]) {
      let err = res["@error"]["@messages"][0];
      setErrorTitle(res["@error"]["@message"]);
      setErrorMsg(err);
      setIsError(true);
    }
  };

  const viewEmployee = (employee) => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false)
    setCurrentEmployee(employee);
    setAppPath(APP_PATH.VIEW_EMPLOYEE);
  };

  const viewRole = (role) => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false)
    setCurrentRole(role);
    setAppPath(APP_PATH.VIEW_ROLE);
  };

  const viewOrg = (org) => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false)
    setCurrentOrg(org);
    setAppPath(APP_PATH.VIEW_ORG);
  };

  const viewDept = (dept) => {
    setErrorTitle([]);
    setErrorMsg([]);
    setIsError(false)
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
            setEmployeeControl={setEmployeeControl}
            editEmployee={handleEditEmployee}
            viewLeaves={viewEmployeeLeaves}
            addLeaves = {addLeave}
            deleteEmployee={handleDeleteEmployee}
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
            deleteRole={handleDeleteRole}
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
            deleteOrg={handleDeleteOrg}
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
      case APP_PATH.VIEW_LEAVE:
        return <ViewLeave
         employee={employeeControl}
         ></ViewLeave>;
      case APP_PATH.ADD_LEAVE:
        return (
          <AddLeave
           employee={employeeControl}
           addLeave={handleAddLeave}
          >
          </AddLeave>
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
            deleteDept={handleDeleteDept}
          ></ViewDept>
        );
      default:
        return <RoleHome></RoleHome>;
    }
  };

  return (
    <div>
      <AppBar
        position="fixed"
        style={{
          width: `calc(100% - 240px)`,
          marginLeft: `240px`,
        }}
      >
        {
          isError ? 
          <Alert severity="error">
            <AlertTitle style={{justifyContent:"left", display: "flex"}}>Error</AlertTitle>
              {errorTitle} - <strong>{errorMsg}</strong>
          </Alert> : <div></div>
        }
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

      {/* {getRenderRoute(appPath)} */}
    </div>
  );
};

export { Home };
