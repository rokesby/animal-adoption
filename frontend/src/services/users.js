// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const getUsers = async () => {
  const requestOptions = {
    method: "GET",
    headers: {
      // Authorization: `Bearer ${token}`,
    },
  };

  const response = await fetch(`/api/users`, requestOptions);
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
      password: password,
    },
  };

  const response = await fetch(`/api/login`, requestOptions);
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

export const postNewMessage = async (authFetch, formData) => {
  try {
    console.log("Posting a new message")
    const response = await authFetch(`/api/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    

    if (!response.ok) {
      throw new Error("Error sending message")
    }

    const data = await response.json();
    console.log('data', data);
    return {
      status: response.status,
      message: "Received message",
      data: data,
    };
  } catch (error) {
    throw error;
  }
}
