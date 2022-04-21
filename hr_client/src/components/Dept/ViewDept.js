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
  
  const ViewDept = ({ dept, editDept, deleteDept }) => {
    const [deptData, setDeptData] = useState();
  
    const [deptEdit, setDeptEdit] = useState({});
    useEffect(() => {
      async function getDept() {
        let res = await getResource(dept["@controls"]["self"]["href"]);
        setDeptData(res);
      }
      getDept();
    }, [dept]);
  
    useEffect(() => {
      let temp = {};
      if (deptData) {
        for (const [property, obj] of Object.entries(deptData)) {
          if (!property.startsWith("@")) {
            temp[property] = obj;
          }
  
          setDeptEdit(temp);
        }
      }
    }, [deptData]);
  
    let formContent = [];
    if (deptData) {
      for (const [property, obj] of Object.entries(
        deptData["@controls"]["edit"]["schema"]["properties"]
      )) {
        if (obj.enum) {
          formContent.push(
            <FormControl>
              <InputLabel htmlFor={property}>{property}</InputLabel>
              <Select
                label={property}
                value={deptEdit[property] || ""}
                onChange={(e) => {
                  setDeptEdit({
                    ...deptEdit,
                    [property]: e.target.value,
                  });
                }}
              >
                {obj.enum.map((item) => {
                  console.log(deptEdit[property] === item);
                  return (
                    <MenuItem selected={deptEdit[property] === item} value={item}>
                      {item}
                    </MenuItem>
                  );
                })}
              </Select>
              <FormHelperText>{obj.description}</FormHelperText>
            </FormControl>
          );
        } else if (obj.format === "date-time") {
          console.log(moment(deptEdit[property]).format("YYYY-DD-MM"));
          formContent.push(
            <TextField
              id={property}
              label={property}
              type="date"
              value={moment(deptEdit[property]).format("YYYY-MM-DD")}
              onChange={(e) => {
                setDeptEdit({
                  ...deptEdit,
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
                value={deptEdit[property]}
                onChange={(e) => {
                  setDeptEdit({
                    ...deptEdit,
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
      deleteDept(
        deptData["@controls"]["hrsys:delete-dept"]["href"],
        deptData["@controls"]["hrsys:delete-dept"]["method"]
      );
    }

    return (
      <div style={{ display: "flex" }}>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            let body = {};
            for (const [property, obj] of Object.entries(
              deptData["@controls"]["edit"]["schema"]["properties"]
            )) {
              if (obj.type === "number") {
                body[property] = parseInt(deptEdit[property]);
              } else if (obj.format === "date-time") {
                body[property] = moment(deptEdit[property]).toISOString(true);
              } else {
                body[property] = deptEdit[property];
              }
  
              if (
                deptData["@controls"]["edit"]["schema"]["required"].includes(
                  property
                ) &&
                !deptEdit[property]
              ) {
                return;
              }
            }
            editDept(
              deptData["@controls"]["edit"]["href"],
              body,
              deptData["@controls"]["edit"]["method"]
            );
            console.log("BODY", body);
          }}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "end",
            height: "90vh",
            flexWrap: "wrap",
            marginTop: "70px",
          }}
        >
          {formContent}
  
          <Button type="submit">SUBMIT</Button>
          <Button onClick={handleDelete}>DELETE</Button>
        </form>
      </div>
    );
  };
  
  export { ViewDept };
  