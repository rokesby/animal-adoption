// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const signup = async (formData) => {
  const payload = {
    first_name: formData.first_name,
    last_name: formData.last_name,
    email: formData.email,
    password: formData.password,
    shelter_id: formData.shelter_id,
  };

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  };

  let response = await fetch(`${BACKEND_URL}/sign-up`, requestOptions);
  if (response.status === 201) {
    const data = await response.json();
    return data;
  } else if (response.status === 409) {
    const data = await response.json();
    return data.message;
  } else {
    throw new Error(
      `Received status ${response.status} when signing up. Expected 201`
    );
  }
};

export const getUsers = async () => {
  const requestOptions = {
    method: "GET",
    headers: {
      // Authorization: `Bearer ${token}`,
    },
  };

  const response = await fetch(`${BACKEND_URL}/users`, requestOptions);
  console.log(response.status);
  if (response.status !== 200) {
    throw new Error("Unable to fetch users");
  }

  const data = await response.json();
  return data;
};

export const getUserById = async (email, password) => {
  const requestOptions = {
    method: "GET",
    headers: {
      // Authorization: `Bearer ${token}`,
      email: email,
      password: password
    },
  };

  const response = await fetch(`${BACKEND_URL}/login`, requestOptions);
  if (response.status !== 200) {
    if (response.status == 401)
        throw new Error("Username or Password is incorrect");
    else {
        throw new Error("Unable to fetch user");
    }
  }

  const data = await response.json();
  return data;
};
