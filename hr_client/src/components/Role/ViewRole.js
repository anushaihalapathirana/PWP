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
  
  const ViewRole = ({ role, editRole, deleteRole }) => {
    const [roleData, setRoleData] = useState();
  
    const [roleEdit, setRoleEdit] = useState({});
    useEffect(() => {
      async function getRole() {
        let res = await getResource(role["@controls"]["self"]["href"]);
        setRoleData(res);
      }
      getRole();
    }, [role]);
  
    useEffect(() => {
      let temp = {};
      if (roleData) {
        for (const [property, obj] of Object.entries(roleData)) {
          if (!property.startsWith("@")) {
            temp[property] = obj;
          }
  
          setRoleEdit(temp);
        }
      }
    }, [roleData]);
  
    let formContent = [];
    if (roleData) {
      for (const [property, obj] of Object.entries(
        roleData["@controls"]["edit"]["schema"]["properties"]
      )) {
        if (obj.enum) {
          formContent.push(
            <FormControl>
              <InputLabel htmlFor={property}>{property}</InputLabel>
              <Select
                label={property}
                value={roleEdit[property] || ""}
                onChange={(e) => {
                  setRoleEdit({
                    ...roleEdit,
                    [property]: e.target.value,
                  });
                }}
              >
                {obj.enum.map((item) => {
                  console.log(roleEdit[property] === item);
                  return (
                    <MenuItem selected={roleEdit[property] === item} value={item}>
                      {item}
                    </MenuItem>
                  );
                })}
              </Select>
              <FormHelperText>{obj.description}</FormHelperText>
            </FormControl>
          );
        } else if (obj.format === "date-time") {
          console.log(moment(roleEdit[property]).format("YYYY-DD-MM"));
          formContent.push(
            <TextField
              id={property}
              label={property}
              type="date"
              value={moment(roleEdit[property]).format("YYYY-MM-DD")}
              onChange={(e) => {
                setRoleEdit({
                  ...roleEdit,
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
                value={roleEdit[property]}
                onChange={(e) => {
                  setRoleEdit({
                    ...roleEdit,
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
      deleteRole(
        roleData["@controls"]["hrsys:delete-role"]["href"],
        roleData["@controls"]["hrsys:delete-role"]["method"]
      );
    }
  
    return (
      <div>
        <h1 style={{
          justifyContent: "center",
          display: "flex",
          marginLeft: "20px",
          marginTop: "80px"
        }}>Role Details</h1>
      
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
              roleData["@controls"]["edit"]["schema"]["properties"]
            )) {
              if (obj.type === "number") {
                body[property] = parseInt(roleEdit[property]);
              } else if (obj.format === "date-time") {
                body[property] = moment(roleEdit[property]).toISOString(true);
              } else {
                body[property] = roleEdit[property];
              }
  
              if (
                roleData["@controls"]["edit"]["schema"]["required"].includes(
                  property
                ) &&
                !roleEdit[property]
              ) {
                return;
              }
            }
            editRole(
              roleData["@controls"]["edit"]["href"],
              body,
              roleData["@controls"]["edit"]["method"]
            );
            console.log("BODY", body);
          }}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "end",
            // height: "90vh",
            flexWrap: "wrap",
            marginTop: "20px",
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
      </div>
    );
  };
  
  export { ViewRole };
  