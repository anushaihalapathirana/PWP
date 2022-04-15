import React, { Fragment } from "react";
import {Button, TextField} from "@material-ui/core";
import {useForm} from "react-hook-form";

const EmployeeForm = props => {
  const { register, handleSubmit, errors } = useForm();
  const onSubmit = (data, e) => {
    e.preventDefault();
    console.log(data);
    props.history.push("/");
  };

  return (
    <Fragment>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <TextField
          id="emp_id"
          label="Employee ID"
          name="empid"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="fname"
          label="First Name"
          name="fname"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="lname"
          label="Last Name"
          name="lname"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="address"
          label="Address"
          name="address"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="gender"
          label="Gender"
          name="gender"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="date_of_birth"
          label="Date of birth"
          name="date_of_birth"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="appointment_date"
          label="Date of Appointment"
          name="appointment_date"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="active_emp"
          label="active_emp"
          name="active_emp"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="prefix_title"
          label="prefix_title"
          name="prefix_title"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="marritial_status"
          label="marritial_status"
          name="marritial_status"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="mobile_no"
          label="Mobile number"
          name="mobile_no"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="basic_salary"
          label="Basic salary"
          name="basic_salary"
          margin="normal"
          variant="outlined"
        />

        <TextField
          id="account_number"
          label="Account number"
          name="account_number"
          margin="normal"
          variant="outlined"
        />

        <Button type="submit" size="large" variant="contained">
          Next
        </Button>
      </form>
    </Fragment>
  );
};

export{EmployeeForm};
