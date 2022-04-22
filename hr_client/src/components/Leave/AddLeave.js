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
  import React, { useState, useEffect } from "react";
  import moment from "moment";
  import { getResource } from "../../services/hrservice";
  
  const AddLeave = ({ employee, addLeave }) => {
    let [schema, setSchema] = useState()
    let [addLeaveControl, setAddLeaveControl] = useState()

    let [error, setError] = useState(false);
    let [formSelectState, setFormSelectState] = useState({});
  
    useEffect(() => {
        async function getLeave() {
          console.log(employee["@controls"])
          let res = await getResource(employee["@controls"]["hrsys:leaves"]["href"]);
          setSchema(res["@controls"]["hrsys:add-leave"]["schema"]);
          setAddLeaveControl(res["@controls"]["hrsys:add-leave"])
        }
        getLeave();
      }, [employee]);
    
      
    let formContent = [];
    if(schema) {
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
                // InputProps={{ inputProps: { min: new Date().toISOString().slice(0, 16),} }}
                inputProps={{
                    min: new Date().toISOString().slice(0, 10),
                    // max: "2022-08-20"
                  }}
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
    }
    return (
      <div>
        <h1 style={{
          justifyContent: "center",
          display: "flex",
          marginLeft: "20px",
          marginTop: "80px"
        }}>Add Leave</h1>
      
      <div 
      style={{
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
            addLeave(addLeaveControl["href"], body);
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
  
  export { AddLeave };
  