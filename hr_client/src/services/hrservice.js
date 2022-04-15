const getResource = async (href) => {
  const res = await fetch(href);
  if (res.ok) {
    return res.json();
  }
  throw new Error("Error while getting resource");
};

export { getResource };
