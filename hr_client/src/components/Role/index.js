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

const RoleHome = ({ roleList, viewRole, roleControl }) => {
  return (
    <div>
      <div className='add-btn-div'>
      <Button
            className="btn-get-data"
            color="primary"
            variant="contained"
            onClick={() => {
              if (roleControl["hrsys:add-role"]) {
                roleList.add();
              }
            }}
          >
            Add Role
          </Button>
      </div>
      <div>
        <TableContainer component={Paper}>
            <Table aria-label="simple table" stickyHeader>
                <TableHead>
                  <TableRow>
                        <TableCell align="right">Code</TableCell>
                        <TableCell align="right">Name</TableCell>
                        <TableCell align="right">Description</TableCell>
                        <TableCell align="right"></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                      {roleList.items.map((row) => (
                        <TableRow key={row.code}>
                          <TableCell component="th" scope="row">
                            {row.code}
                          </TableCell>
                          <TableCell align="right">{row.name}</TableCell>
                          <TableCell align="right">{row.description}</TableCell>
                          <Button
                            color="primary"
                            variant="contained"
                            onClick={() => {
                              viewRole(row);
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

export { RoleHome };
