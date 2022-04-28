import React, { useCallback, useEffect } from "react";
import { useState } from "react";
import { Button, InputAdornment, TextField } from "@material-ui/core";
import Dropdown from "react-dropdown";
import { EmployeeTable } from "../Home/EmploteeTable";
import Search from "@mui/icons-material/Search";

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
  const [searchValue, setSearchvalue] = useState("");
  const [filteredList, setFilteredSet] = useState([]);

  useEffect(() => {
    setFilteredSet(employeeList.items);
  }, [employeeList.items]);
  useEffect(() => {
    let items = employeeList.items;
    if (items && items.length > 0) {
      if (searchValue === "") {
        setFilteredSet(items);
      } else {
        items = items.filter((value) => {
          return (
            value.first_name
              .toLowerCase()
              .includes(searchValue.toLowerCase()) ||
            value.last_name.toLowerCase().includes(searchValue.toLowerCase())
          );
        });
        setFilteredSet(items);
      }
    }
  }, [searchValue]);

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
        marginTop: "65px",
        marginLeft: "240px",
      }}
    >
      <h1
        style={{
          justifyContent: "left",
          display: "flex",
          marginLeft: "20px",
        }}
      >
        Employees
      </h1>
      <div
        style={{
          position: "relative",
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
        }}
      >
        <TextField
          style={{
            marginLeft: "10px",
          }}
          label="Filter results"
          value={searchValue}
          onChange={(e) => {
            e.preventDefault();
            setSearchvalue(e.target.value);
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="end">
                <Search />
              </InputAdornment>
            ),
          }}
        ></TextField>
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
            Get Employees
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
            Clear Filters
          </Button>

          <Button
            className="btn-get-data"
            color="primary"
            variant="contained"
            disabled={
              !(employeeControl && employeeControl["hrsys:add-employee"])
            }
            onClick={() => {
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
          employeeList={filteredList}
          viewEmployee={viewEmployee}
        />
      </div>
    </div>
  );
};

export { EmployeeHome };
