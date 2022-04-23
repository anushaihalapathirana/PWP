import {
    Button,
    TableCell,
    TableHead, 
    TableRow, 
    Paper,
    TableBody,
    TableContainer,
    Table
  } from "@material-ui/core";
  import React, { useEffect, useState } from "react";
  import { getResource } from "../../services/hrservice";
  
  const ViewLeave = ({ employee, editLeave, deleteLeave }) => {
    const [leaveData, setLeaveData] = useState([]);
    useEffect(() => {
      async function getLeave() {
        console.log(employee["@controls"])
        let res = await getResource(employee["@controls"]["hrsys:leaves"]["href"]);
        setLeaveData(res["items"]);
      }
      getLeave();
    }, [employee]);
    
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
        }}>Leave Plans</h1>
        <div
          style={{
            position: "relative",
            display: "flex",
            flexDirection: "row",
            // alignItems: "center",
          }}
        >
        </div>
        <div style={{
          margin: "20px",
          width: "50%",
          display: "flex",
          justifyContent: "center"
          }}>
          <TableContainer
           style={{
            height:"500px",
            overflow: "scroll"
          }} 
           component={Paper}>
              <Table aria-label="simple table" stickyHeader>
                  <TableHead>
                    <TableRow>
                          <TableCell align="right">Leave date</TableCell>
                          <TableCell align="right">Leave type</TableCell>
                          <TableCell align="right">Reason</TableCell>
                          <TableCell align="right"></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                        {leaveData.map((row) => (
                          <TableRow key={row.id}>
                            <TableCell align="right">{row.leave_date}</TableCell>
                            <TableCell align="right">{row.leave_type}</TableCell>
                            <TableCell align="right">{row.reason}</TableCell>
                            <TableCell align="right">
                            <Button
                              color="primary"
                              variant="contained"
                              // onClick={() => {
                              //   viewRole(row);
                              // }} 
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
  
  export { ViewLeave };
  