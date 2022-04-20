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

export { getResource, deleteResource };
