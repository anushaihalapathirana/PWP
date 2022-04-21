import React from "react";
import { useState } from "react";
import { Button } from "@material-ui/core";
import Dropdown from "react-dropdown";
import { EmployeeTable } from "../Home/EmploteeTable";

const EmployeeHome = ({
  orgList,
  deptList,
  roleList,
  employeeList,
  employeeControl,
  viewEmployee,
}) => {
  const [organization, setOrganization] = useState("Select");
  const [department, setDepartment] = useState("Select");
  const [currentRole, setRole] = useState("Select");

  let orgItems = orgList.items.map((item) => (
    <option key={item.organization_id}>{item.name}</option>
  ));

  let deptItems = deptList.items.map((item) => (
    <option key={item.department_id}>{item.name}</option>
  ));

  let roleItems = roleList.items.map((item) => (
    <option key={item.code}>{item.name}</option>
  ));

  const handleOrganizationChange = (event) => {
    // console.log(event);
    setOrganization(event.value.key);
  };

  const handleDepartmentChange = (event) => {
    setDepartment(event.value.key);
  };

  const handleRoleChange = (event) => {
    setRole(event.value.key);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
        }}
      >
        <div className="drop-down">
          <Dropdown
            className="org-drop"
            placeholder="Search categories..."
            label="Select organization"
            options={orgItems}
            value={organization}
            onChange={handleOrganizationChange}
          />
        </div>

        <div className="drop-down">
          <Dropdown
            className="dept-drop"
            placeholder="Search categories..."
            label="Select Departments"
            options={deptItems}
            value={department}
            onChange={handleDepartmentChange}
          />
        </div>

        <div className="drop-down">
          <Dropdown
            className="dept-drop"
            placeholder="Search categories..."
            label="Select Roles"
            options={roleItems}
            value={currentRole}
            onChange={handleRoleChange}
          />
        </div>

        <div className="btn">
          <Button
            className="btn-get-data"
            color="primary"
            variant="contained"
            onClick={() =>
              employeeList.get(organization, department, currentRole)
            }
          >
            Filter
          </Button>

          <Button
            className="btn-get-data"
            color="primary"
            variant="contained"
            onClick={() => {
              setDepartment("Select");
              setRole("Select");
              setOrganization("Select");
            }}
          >
            Clear
          </Button>

          <Button
            className="btn-get-data"
            color="primary"
            variant="contained"
            disabled={
              !(employeeControl && employeeControl["hrsys:add-employee"])
            }
            onClick={() => {
              // console.log(employeeControl);
              if (employeeControl["hrsys:add-employee"]) {
                employeeList.add();
              }
            }}
          >
            Add Employee
          </Button>
        </div>
      </div>
      <div className="table-data">
        <EmployeeTable
          employeeList={employeeList.items}
          viewEmployee={viewEmployee}
        />
      </div>
    </div>
  );
};

export { EmployeeHome };
