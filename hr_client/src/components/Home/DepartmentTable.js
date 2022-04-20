import React, { Fragment } from "react";
import {Button, TextField} from "@material-ui/core";
import {useForm} from "react-hook-form";
import './commonTable.css'
import { 
    TableHead, 
    TableRow, 
    Paper,
    TableCell,
    TableBody,
    TableContainer,
    Table
} from '@material-ui/core';

const DepartmentTable = props => {

  const handleCellClick = (data) => {
    console.log(data)
  }

  return (
    <div>
        <TableContainer component={Paper}>
            <Table aria-label="simple table" stickyHeader>
                <TableHead>
                  <TableRow>
                        <TableCell align="right">ID</TableCell>
                        <TableCell align="right">Name</TableCell>
                        <TableCell align="right">Description</TableCell>
                        <TableCell align="right">Edit</TableCell>
                        <TableCell align="right">Delete</TableCell>

                  </TableRow>
                </TableHead>
                <TableBody>
                      {props.data.map((row) => (
                        <TableRow key={row.department_id}>
                          <TableCell component="th" scope="row">
                            {row.department_id}
                          </TableCell>
                          <TableCell align="right">{row.name}</TableCell>
                          <TableCell align="right">{row.description}</TableCell>
                          <TableCell className='viewcell' align="right" onClick={() => handleCellClick(row['@controls']['self']['href'])}>{'Edit'}</TableCell>
                          <TableCell className='viewcell' align="right" 
                          onClick={() => props.onClickDelete(row['@controls']['self']['href'])}
                          >{'Delete'}</TableCell>
                        </TableRow>
                      ))}
                </TableBody>
            </Table>
        </TableContainer> 
    </div>
  );
};

export{DepartmentTable};
