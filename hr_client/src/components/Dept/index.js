import React from "react";
import {Button} from "@material-ui/core";
import './index.css'
import { 
    TableHead, 
    TableRow, 
    Paper,
    TableCell,
    TableBody,
    TableContainer,
    Table
} from '@material-ui/core';

const DeptHome = ({ deptList, viewDept, deptControl }) => {

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        marginTop: "65px",
        marginLeft: "240px",
      }}
    >
      <h1 style={{
        justifyContent: "left",
        display: "flex",
        marginLeft: "20px",
      }}>Departments</h1>
      <div
        style={{
          position: "relative",
          display: "flex",
          flexDirection: "row",
          // alignItems: "center",
        }}
      >
        <div className="drop-down">
      <Button
            className="btn-get-data"
            color="primary"
            variant="contained"
            onClick={() => {
              if (deptControl["hrsys:add-dept"]) {
                deptList.add();
              }
            }}
          >
            Add Department
          </Button>
        </div>
      </div>
      <div style={{margin: "20px"}}>
        <TableContainer
         style={{
          height:"500px",
          width: "50%",
          overflow: "scroll"
        }} 
         component={Paper}>
            <Table aria-label="simple table" stickyHeader>
                <TableHead>
                  <TableRow>
                        <TableCell align="right">ID</TableCell>
                        <TableCell align="right">Name</TableCell>
                        <TableCell align="right">Description</TableCell>
                        <TableCell align="right"></TableCell>

                  </TableRow>
                </TableHead>
                <TableBody>
                      {deptList.items.map((row) => (
                        <TableRow key={row.department_id}>
                          <TableCell component="th" scope="row">
                            {row.department_id}
                          </TableCell>
                          <TableCell align="right">{row.name}</TableCell>
                          <TableCell align="right">{row.description}</TableCell>
                          <TableCell align="right">
                          <Button
                            color="primary"
                            variant="contained"
                            onClick={() => {
                              viewDept(row);
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
    </div>
  );
};

export{DeptHome};
