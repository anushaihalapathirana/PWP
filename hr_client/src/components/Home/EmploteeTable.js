import React from "react";
import { Button, TextField } from "@material-ui/core";
import {
  TableHead,
  TableRow,
  Paper,
  TableCell,
  TableBody,
  TableContainer,
  Table,
} from "@material-ui/core";

const EmployeeTable = (props) => {
  return (
    <div>
      <TableContainer
        style={{
          height: "500px",
          overflow: "scroll",
        }}
        component={Paper}
      >
        <Table aria-label="simple table" stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell>First Name</TableCell>
              <TableCell align="right">Last Name</TableCell>
              <TableCell align="right">Address</TableCell>
              <TableCell align="right">Gender</TableCell>
              <TableCell align="right">Date of birth</TableCell>
              <TableCell align="right">Date of appointment</TableCell>
              <TableCell align="right">Active</TableCell>
              <TableCell align="right">Mobile No</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.employeeList.map((row) => (
              <TableRow key={row.employee_id}>
                <TableCell component="th" scope="row">
                  {row.first_name}
                </TableCell>
                <TableCell align="right">{row.last_name}</TableCell>
                <TableCell align="right">{row.address}</TableCell>
                <TableCell align="right">{row.gender}</TableCell>
                <TableCell align="right">{row.date_of_birth}</TableCell>
                <TableCell align="right">{row.appointment_date}</TableCell>
                <TableCell align="right">{row.active_emp}</TableCell>
                <TableCell align="right">{row.mobile_no}</TableCell>
                <TableCell align="right">
                  <Button
                    color="primary"
                    variant="contained"
                    onClick={() => {
                      props.viewEmployee(row);
                    }}
                  >
                    View
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export { EmployeeTable };
