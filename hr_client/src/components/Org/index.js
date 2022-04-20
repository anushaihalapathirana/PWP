
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

const OrgHome = ({ orgList }) => {

  return (
    <div>
      <div className='add-btn-div'>
        <Button className='btn-get-data'
            color="primary"
            variant="outlined"
            onClick={orgList.add}
            >
              Add Organization
        </Button>
      </div>
      <div>
        <TableContainer component={Paper}>
            <Table aria-label="simple table" stickyHeader>
                <TableHead>
                  <TableRow>
                        <TableCell align="right">ID</TableCell>
                        <TableCell align="right">Name</TableCell>
                        <TableCell align="right">Location</TableCell>
                        <TableCell align="right">Edit</TableCell>
                        <TableCell align="right">Delete</TableCell>

                  </TableRow>
                </TableHead>
                <TableBody>
                      {orgList.items.map((row) => (
                        <TableRow key={row.organization_id}>
                          <TableCell component="th" scope="row">
                            {row.organization_id}
                          </TableCell>
                          <TableCell align="right">{row.name}</TableCell>
                          <TableCell align="right">{row.location}</TableCell>
                          <TableCell className='viewcell' align="right" onClick={() => orgList.get(row['@controls']['self']['href'])}>{'Edit'}</TableCell>
                          <TableCell className='viewcell' align="right" 
                          onClick={() => orgList.delete(row['@controls']['self']['href'])}
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

export{OrgHome};

