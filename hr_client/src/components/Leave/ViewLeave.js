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
  import moment from "moment";
  import React, { useEffect, useState } from "react";
  import { getResource } from "../../services/hrservice";
  
  const ViewLeave = ({ employee, employeeControl, editLeave, deleteLeave }) => {
    const [leaveData, setLeaveData] = useState();
  
    const [leaveEdit, setLeaveEdit] = useState({});
    useEffect(() => {
      async function getLeave() {
        console.log(employee)
        console.log(employeeControl)
        let res = await getResource(employeeControl["@controls"]["self"]["href"]);
        setLeaveData(res);
      }
      getLeave();
    }, [employee]);
  
    useEffect(() => {
      let temp = {};
      if (leaveData) {
        for (const [property, obj] of Object.entries(leaveData)) {
          if (!property.startsWith("@")) {
            temp[property] = obj;
          }
  
          setLeaveEdit(temp);
        }
      }
    }, [leaveData]);
  
    let formContent = [];
    if (leaveData) {
      for (const [property, obj] of Object.entries(
        leaveData["@controls"]["edit"]["schema"]["properties"]
      )) {
        if (obj.enum) {
          formContent.push(
            <FormControl>
              <InputLabel htmlFor={property}>{property}</InputLabel>
              <Select
                label={property}
                value={leaveEdit[property] || ""}
                onChange={(e) => {
                  setLeaveEdit({
                    ...leaveEdit,
                    [property]: e.target.value,
                  });
                }}
              >
                {obj.enum.map((item) => {
                  console.log(leaveEdit[property] === item);
                  return (
                    <MenuItem selected={leaveEdit[property] === item} value={item}>
                      {item}
                    </MenuItem>
                  );
                })}
              </Select>
              <FormHelperText>{obj.description}</FormHelperText>
            </FormControl>
          );
        } else if (obj.format === "date-time") {
          console.log(moment(leaveEdit[property]).format("YYYY-DD-MM"));
          formContent.push(
            <TextField
              id={property}
              label={property}
              type="date"
              value={moment(leaveEdit[property]).format("YYYY-MM-DD")}
              onChange={(e) => {
                setLeaveEdit({
                  ...leaveEdit,
                  [property]: e.target.value,
                });
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
              <Input
                type={obj.type}
                id={property}
                value={leaveEdit[property]}
                onChange={(e) => {
                  setLeaveEdit({
                    ...leaveEdit,
                    [property]: e.target.value,
                  });
                }}
              />
              <FormHelperText>{obj.description}</FormHelperText>
            </FormControl>
          );
        }
      }
    }

    const handleDelete = () => {
      deleteLeave(
        leaveData["@controls"]["hrsys:delete-leave"]["href"],
        leaveData["@controls"]["hrsys:delete-leave"]["method"]
      );
    }
  
    return (
      <div style={{
         display: "flex",
         justifyContent: "center",
         alignItems: "center"
         }}>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            let body = {};
            for (const [property, obj] of Object.entries(
              leaveData["@controls"]["edit"]["schema"]["properties"]
            )) {
              if (obj.type === "number") {
                body[property] = parseInt(leaveEdit[property]);
              } else if (obj.format === "date-time") {
                body[property] = moment(leaveEdit[property]).toISOString(true);
              } else {
                body[property] = leaveEdit[property];
              }
  
              if (
                leaveData["@controls"]["edit"]["schema"]["required"].includes(
                  property
                ) &&
                !leaveEdit[property]
              ) {
                return;
              }
            }
            editLeave(
              leaveData["@controls"]["edit"]["href"],
              body,
              leaveData["@controls"]["edit"]["method"]
            );
            console.log("BODY", body);
          }}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "end",
            // height: "90vh",
            flexWrap: "wrap",
            marginTop: "112px",
          }}
        >
          {formContent}

          <Button
          style={{
            marginTop: "10px"
          }}
           variant="contained" color="primary" type="submit">
            Update
          </Button>
          <Button
          style={{
            marginTop: "10px",
            marginLeft: "10px"
          }}
           variant="contained"
           color="secondary" 
           onClick={handleDelete}>DELETE</Button>
        </form>
      </div>
    );
  };
  
  export { ViewLeave };
  