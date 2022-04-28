/**
 * 
 * This file contains the method to handle API requests 
 */
import { AUTH } from "../util/constants";

/**
 * 
 * @param {href} URL
 * This method will send GET API call to the backend 
 */
const getResource = async (href) => {
  const res = await fetch(href, {
    headers: {
      "Content-Type": "application/json",
      "HRSystem-Api-Key": AUTH
    },
  });
  if (res.ok) {
    return res.json();
  }  else if (!res.ok){
    return res.json()
  } else {
    throw new Error("Error while getting resource");
  }
};

/**
 * 
 * @param {href} URL
 * This method will send DELETE API call to the backend 
 */
const deleteResource = async (href, method) => {
  const res = await fetch(href, { 
    method: method,
    headers: {
      "Content-Type": "application/json",
      "HRSystem-Api-Key": AUTH
    },
  });
  if (res.ok) {
    return res.ok;
  } else if (!res.ok){
    return res.json()
  } else {
    throw new Error("Error while deleting resource");
  }
};

/**
 * 
 * @param {href} URL
 * This method will send POST API call to the backend 
 */
const addResource = async (href, body, method = "POST") => {
  const res = await fetch(href, {
    method: method,
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      "HRSystem-Api-Key": AUTH
    },
  });
  if (res.ok) {
    return res.ok;
  }  else if (!res.ok){
    return res.json()
  } else {
    throw new Error("Error while adding resource");
  }
};

export { getResource, deleteResource, addResource };
