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

const ViewEmployee = ({
  employee,
  editEmployee,
  deleteEmployee,
  viewLeaves,
}) => {
  const [employeeData, setEmployeeData] = useState();

  const [empEdit, setEmpEdit] = useState({});
  useEffect(() => {
    async function getEmployee() {
      let res = await getResource(employee["@controls"]["self"]["href"]);
      setEmployeeData(res);
    }
    getEmployee();
  }, [employee]);

  useEffect(() => {
    let temp = {};
    if (employeeData) {
      for (const [property, obj] of Object.entries(employeeData)) {
        if (!property.startsWith("@")) {
          temp[property] = obj;
        }

        setEmpEdit(temp);
      }
    }
  }, [employeeData]);

  let formContent = [];
  if (employeeData) {
    for (const [property, obj] of Object.entries(
      employeeData["@controls"]["edit"]["schema"]["properties"]
    )) {
      if (obj.enum) {
        console.log("DDDDDDD", empEdit[property]);
        formContent.push(
          <FormControl
            style={{
              width: "300px",
              margin: "20px",
            }}
          >
            <InputLabel htmlFor={property}>{property}</InputLabel>
            <Select
              //   id={property}
              //   name={property}
              label={property}
              value={empEdit[property] || ""}
              //   defaultValue={empEdit[property]}
              onChange={(e) => {
                let f = property;
                // setFormSelectState({
                //   ...formSelectState,
                //   f: e.target.value,
                // });
                setEmpEdit({
                  ...empEdit,
                  [property]: e.target.value,
                });
              }}
            >
              {obj.enum.map((item) => {
                console.log(empEdit[property] === item);
                return (
                  <MenuItem selected={empEdit[property] === item} value={item}>
                    {item}
                  </MenuItem>
                );
              })}

              {/* <MenuItem value={20}>Twenty</MenuItem>
                <MenuItem value={30}>Thirty</MenuItem> */}
            </Select>
            <FormHelperText>{obj.description}</FormHelperText>
          </FormControl>
        );
      } else if (obj.format === "date-time") {
        console.log(moment(empEdit[property]).format("YYYY-DD-MM"));
        formContent.push(
          <TextField
            style={{
              width: "300px",
              margin: "20px",
            }}
            id={property}
            label={property}
            type="date"
            value={moment(empEdit[property]).format("YYYY-MM-DD")}
            onChange={(e) => {
              setEmpEdit({
                ...empEdit,
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
          <FormControl
            style={{
              width: "300px",
              margin: "20px",
            }}
          >
            <InputLabel htmlFor={property}>{property}</InputLabel>
            <Input
              type={obj.type}
              id={property}
              value={empEdit[property]}
              onChange={(e) => {
                setEmpEdit({
                  ...empEdit,
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
    deleteEmployee(
      employeeData["@controls"]["hrsys:delete-employee"]["href"],
      employeeData["@controls"]["hrsys:delete-employee"]["method"]
    );
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        marginTop: "65px",
        marginLeft: "240px",
      }}
    >
      <div>
        <Button onClick={viewLeaves}>View Leaves</Button>
        <Button>Add Leave</Button>
        {/* <Button>Employees in Same Organization</Button> */}
      </div>
      <div>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            let body = {};
            for (const [property, obj] of Object.entries(
              employeeData["@controls"]["edit"]["schema"]["properties"]
            )) {
              if (obj.type === "number") {
                body[property] = parseInt(empEdit[property]);
              } else if (obj.format === "date-time") {
                body[property] = moment(empEdit[property]).toISOString(true);
              } else {
                body[property] = empEdit[property];
              }

              if (
                employeeData["@controls"]["edit"]["schema"][
                  "required"
                ].includes(property) &&
                !empEdit[property]
              ) {
                //   setError(true);
                return;
              }
            }
            //   addEmployee(addEmployeeControl["href"], body);
            editEmployee(
              employeeData["@controls"]["edit"]["href"],
              body,
              employeeData["@controls"]["edit"]["method"]
            );
            console.log("BODY", body);
          }}
          style={{
            display: "flex",
            flexDirection: "column",
            // alignItems: "end",
            height: "70vh",
            flexWrap: "wrap",
            marginTop: "70px",
          }}
        >
          {formContent}
          <Button variant="contained" color="primary" type="submit">
            Update
          </Button>
          <Button onClick={handleDelete}>DELETE</Button>
        </form>
      </div>
    </div>
  );
};

export { ViewEmployee };
