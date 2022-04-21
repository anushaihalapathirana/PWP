import React, { Fragment } from "react";
import {Button, TextField} from "@material-ui/core";
import {useForm} from "react-hook-form";
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
    <div>
      <div className='add-btn-div'>
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
      <div>
        <TableContainer component={Paper}>
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
                          <Button
                            color="primary"
                            variant="contained"
                            onClick={() => {
                              viewDept(row);
                            }} 
                          >
                            View
                          </Button>
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
