
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

const OrgHome = ({ orgList, viewOrg, orgControl }) => {

  return (
    <div>
      <div className='add-btn-div'>
      <Button
            className="btn-get-data"
            color="primary"
            variant="contained"
            onClick={() => {
              if (orgControl["hrsys:add-organization"]) {
                orgList.add();
              }
            }}
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
                        <TableCell align="right"></TableCell>
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
                          <Button
                            color="primary"
                            variant="contained"
                            onClick={() => {
                              viewOrg(row);
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

export{OrgHome};

