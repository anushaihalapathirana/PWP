import React, { useEffect, useState } from "react";
import { getResource } from "../../services/hrservice";
import { UI_LOADING_STATES } from "../../util/constants";

const Home = () => {
  const [roleState, setRoleState] = useState(UI_LOADING_STATES.INIT);
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    setRoleState(UI_LOADING_STATES.LOADING);
    async function callResource() {
      try {
        let roleBody = await getResource("/api/roles/");
        setRoles(roleBody["items"]);
        console.log(roles);
      } catch (error) {
        setRoleState(UI_LOADING_STATES.ERROR);
      }
    }

    callResource();
  }, []);
  let items = roles.map((item) => <h6>{item.name}</h6>);
  return items;
};

export { Home };
