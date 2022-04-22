const getResource = async (href) => {
  const res = await fetch(href);
  if (res.ok) {
    return res.json();
  } else {
    return res.json()
  }
  throw new Error("Error while getting resource");
};

const deleteResource = async (href, method) => {
  const res = await fetch(href, { method: method });
  if (res.ok) {
    return res.ok;
  } else {
    return res.json()
  }
  throw new Error("Error while deleting resource");
};

const addResource = async (href, body, method = "POST") => {
  const res = await fetch(href, {
    method: method,
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    return res.ok;
  } else {
    return res.json()
  }
  throw new Error("Error while adding new employee");
};

export { getResource, deleteResource, addResource };
