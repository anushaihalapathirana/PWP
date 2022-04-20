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

const RoleHome = ({ roleList }) => {
  return (
    <div>
      <div className='add-btn-div'>
        <Button className='btn-get-data'
            color="primary"
            variant="outlined"
            onClick={roleList.add}
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
                        <TableCell align="right">Edit</TableCell>
                        <TableCell align="right">Delete</TableCell>
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
                          <TableCell className='viewcell' align="right" onClick={() => roleList.edit(row['@controls']['self']['href'])}>{'Edit'}</TableCell>
                          <TableCell className='viewcell' align="right" 
                          onClick={() => roleList.delete(row['@controls']['self']['href'])}
                          >{'Delete'}</TableCell>
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
