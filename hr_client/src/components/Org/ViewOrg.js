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
  
  const ViewOrg = ({ org, editOrg, deleteOrg }) => {
    const [orgData, setOrgData] = useState();
  
    const [orgEdit, setOrgEdit] = useState({});
    useEffect(() => {
      async function getOrg() {
        let res = await getResource(org["@controls"]["self"]["href"]);
        setOrgData(res);
      }
      getOrg();
    }, [org]);
  
    useEffect(() => {
      let temp = {};
      if (orgData) {
        for (const [property, obj] of Object.entries(orgData)) {
          if (!property.startsWith("@")) {
            temp[property] = obj;
          }
  
          setOrgEdit(temp);
        }
      }
    }, [orgData]);
  
    let formContent = [];
    if (orgData) {
      for (const [property, obj] of Object.entries(
        orgData["@controls"]["edit"]["schema"]["properties"]
      )) {
        if (obj.enum) {
          formContent.push(
            <FormControl>
              <InputLabel htmlFor={property}>{property}</InputLabel>
              <Select
                label={property}
                value={orgEdit[property] || ""}
                onChange={(e) => {
                  let f = property;
                  setOrgEdit({
                    ...orgEdit,
                    [property]: e.target.value,
                  });
                }}
              >
                {obj.enum.map((item) => {
                  console.log(orgEdit[property] === item);
                  return (
                    <MenuItem selected={orgEdit[property] === item} value={item}>
                      {item}
                    </MenuItem>
                  );
                })}
              </Select>
              <FormHelperText>{obj.description}</FormHelperText>
            </FormControl>
          );
        } else if (obj.format === "date-time") {
          console.log(moment(orgEdit[property]).format("YYYY-DD-MM"));
          formContent.push(
            <TextField
              id={property}
              label={property}
              type="date"
              value={moment(orgEdit[property]).format("YYYY-MM-DD")}
              onChange={(e) => {
                setOrgEdit({
                  ...orgEdit,
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
                value={orgEdit[property]}
                onChange={(e) => {
                  setOrgEdit({
                    ...orgEdit,
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
  
    return (
      <div style={{ display: "flex" }}>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            let body = {};
            for (const [property, obj] of Object.entries(
              orgData["@controls"]["edit"]["schema"]["properties"]
            )) {
              if (obj.type === "number") {
                body[property] = parseInt(orgEdit[property]);
              } else if (obj.format === "date-time") {
                body[property] = moment(orgEdit[property]).toISOString(true);
              } else {
                body[property] = orgEdit[property];
              }
  
              if (
                orgData["@controls"]["edit"]["schema"]["required"].includes(
                  property
                ) &&
                !orgEdit[property]
              ) {
                return;
              }
            }
            editOrg(
              orgData["@controls"]["edit"]["href"],
              body,
              orgData["@controls"]["edit"]["method"]
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
        </form>
      </div>
    );
  };
  
  export { ViewOrg };
  