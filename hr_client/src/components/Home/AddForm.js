import React, { Fragment } from "react";
import {Button, TextField} from "@material-ui/core";
import {useForm} from "react-hook-form";
import './commonTable.css'

const AddForm = props => {

  return (
    <div>
      <Fragment>
        <form className='add-form' onSubmit={(e) => props.onSubmit(e)} noValidate>
            <h2>{props.title}</h2>
            <TextField
            id="id"
            label={props.labelid}
            name={props.nameid}
            margin="normal"
            variant="outlined"
            />

            <TextField
            id="name"
            label={props.label}
            name={props.name}
            margin="normal"
            variant="outlined"
            />

            <TextField
            id="desc"
            label={props.labeldesc}
            name={props.namedesc}
            margin="normal"
            variant="outlined"
            />

            <Button className="add-btn" type="submit" color="primary" size="large" variant="contained">
            ADD
            </Button>
        </form>
        </Fragment>
    </div>
  );
};

export{AddForm};
