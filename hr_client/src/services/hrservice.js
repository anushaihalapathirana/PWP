const getResource = async (href) => {
  const res = await fetch(href);
  if (res.ok) {
    return res.json();
  }
  throw new Error("Error while getting resource");
};

const deleteResource = async (href) => {
  const res = await fetch(href, {method: 'DELETE'});
  if (res.ok) {
    return res.ok
  }
  throw new Error("Error while deleting resource");
};

const addResource = async (href, data) => {
  const res = await fetch(href, 
    {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
      },
    }
    ).then(response => {
      return response
    })
    .catch((error) => {
      throw new Error("Error while adding resource");
    });
};



export { getResource, deleteResource, addResource };
