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
  
  const AddDept = ({ addDeptControl, addDept }) => {
    let schema = addDeptControl["schema"];
  
    let [error, setError] = useState(false);
    let [formSelectState, setFormSelectState] = useState({});
  
    let formContent = [];
    for (const [property, obj] of Object.entries(schema["properties"])) {
      if (obj.enum) {
        formContent.push(
          <FormControl>
            <InputLabel htmlFor={property}>{property}</InputLabel>
            <Select
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
            </Select>
            <FormHelperText>{obj.description}</FormHelperText>
          </FormControl>
        );
      } else if (obj.format === "date-time") {
        formContent.push(
          <TextField
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
          <FormControl>
            <InputLabel htmlFor={property}>{property}</InputLabel>
            <Input type={obj.type} id={property} />
            <FormHelperText>{obj.description}</FormHelperText>
          </FormControl>
        );
      }
    }
    return (
      <div>
        <h1 style={{
          justifyContent: "center",
          display: "flex",
          marginLeft: "20px",
          marginTop: "80px"
        }}>Add Department</h1>
      
      <div style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
        }}>
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
            addDept(addDeptControl["href"], body);
          }}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "end",
            height: "90vh",
            flexWrap: "wrap",
            marginTop: "0px",
          }}
        >
          {formContent}
          
          <Button 
          style={{
            marginTop: "30px"
          }}
          variant="contained" color="primary" type="submit">SUBMIT</Button>
        </form>
      </div>
      </div>
    );
  };
  
  export { AddDept };
  