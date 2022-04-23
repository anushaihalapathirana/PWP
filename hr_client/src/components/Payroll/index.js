import React from "react";
import {Button} from "@material-ui/core";
import './index.css'
import { CSVLink } from "react-csv";
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';

const PayrollHome = ({ getPayloadFile, data, isSuccess, headers }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        marginTop: "65px",
        marginLeft: "240px",
      }}
    >
      {
          isSuccess ? 
          <Alert severity="success">
            <AlertTitle style={{justifyContent:"left", display: "flex"}}>Success</AlertTitle>
              Payroll data generated successfully - <strong> You can download now</strong>
          </Alert> : <div></div>
        }
      <h1 style={{
        justifyContent: "left",
        display: "flex",
        marginLeft: "20px",
      }}>Payrolls</h1>
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
            onClick={() => {getPayloadFile()}}
          >
            Generate Payroll File
          </Button>
          {
            isSuccess ? 
          <CSVLink data={data} >
            Download File
          </CSVLink> : <div></div>
          }
          
          </div>
      </div>
    </div>
  );
};

export { PayrollHome };
