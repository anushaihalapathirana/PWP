import {
  Button,
  FormControl,
  FormHelperText,
  Input,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@material-ui/core";
import React, { useState } from "react";
import moment from "moment";

const AddEmployee = ({ addEmployeeControl, addEmployee }) => {
  let schema = addEmployeeControl["schema"];

  let [error, setError] = useState(false);
  let [formSelectState, setFormSelectState] = useState({});

  let formContent = [];
  for (const [property, obj] of Object.entries(schema["properties"])) {
    if (obj.enum) {
      formContent.push(
        <FormControl>
          <InputLabel 
          style={{
            width: "150px",
            marginLeft: "0px",
          }}
          htmlFor={property}>{property}</InputLabel>
          <Select
            style={{
              width: "300px",
              margin: "20px",
            }}
            id={property}
            name={property}
            value={formSelectState[property] && obj.enum[0]}
            label={property}
            onChange={(e) => {
              setFormSelectState({
                ...formSelectState,
                f: e.target.value,
              });
            }}
          >
            {obj.enum.map((item) => {
              return <MenuItem value={item}>{item}</MenuItem>;
            })}

            {/* <MenuItem value={20}>Twenty</MenuItem>
          <MenuItem value={30}>Thirty</MenuItem> */}
          </Select>
          <FormHelperText 
          style={{
            width: "150px",
            marginLeft: "20px",
          }}>{obj.description}</FormHelperText>
        </FormControl>
      );
    } else if (obj.format === "date-time") {
      formContent.push(
        <TextField
          style={{
            width: "300px",
            margin: "20px",
          }}
          id={property}
          label={property}
          type="date"
          sx={{ width: 220 }}
          InputLabelProps={{
            shrink: true,
          }}
        />
      );
    } else {
      formContent.push(
        <FormControl
          style={{
            width: "300px",
            margin: "20px",
          }}
        >
          <InputLabel htmlFor={property}>{property}</InputLabel>
          <Input type={obj.type} id={property} />
          <FormHelperText>{obj.description}</FormHelperText>
        </FormControl>
      );
    }
  }
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        marginTop: "65px",
        marginLeft: "240px",
      }}
    >
      <div
      style={{
        justifyContent: "left",
        display: "flex",
        marginLeft: "20px",
      }}>
        <h1 style={{
        marginRight: "200px"
      }}>Add Employee</h1>
      
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();

          let body = {};
          for (const [property, obj] of Object.entries(schema["properties"])) {
            if (obj.type === "number") {
              body[property] = parseInt(e.target[property].value);
            } else if (obj.format === "date-time") {
              body[property] = moment(e.target[property].value).toISOString(
                true
              );
            } else {
              body[property] = e.target[property].value;
            }

            if (
              schema["required"].includes(property) &&
              !e.target[property].value
            ) {
              setError(true);
              return;
            }
          }
          addEmployee(addEmployeeControl["href"], body);
        }}
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "end",
          height: "85vh",
          flexWrap: "wrap",
          // marginTop: "70px",
        }}
      >
        {formContent}
        <TextField
        style={{
          marginTop: "20px",
          width: "300px",
          marginLeft: "20px",
        }}
          id="date"
          label="Birthday"
          type="date"
          defaultValue="2017-05-24"
          sx={{ width: 220 }}
          InputLabelProps={{
            shrink: true,
          }}
        />
        <Button
          style={{
            margin: "20px",
            width:"300px",
            marginLeft: "20px !important"
          }}
          variant="contained" color="primary" type="submit">SUBMIT</Button>
      </form>
    </div>
  );
};

export { AddEmployee };
