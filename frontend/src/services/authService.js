// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const loginService = async (email, password) => {
  const payload = {
    email: email,
    password: password,
  };
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    credentials: "include",
  };

  const response = await fetch(`/api/token`, requestOptions);
  if (response.status !== 200) {
    if (response.status == 401)
      throw new Error("Username or Password is incorrect");
    else {
      throw new Error("Login failed");
    }
  }

  const data = await response.json();
  return data;
};

export const signupService = async (formData) => {
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
    credentials: "include",
  };

  const response = await fetch(`/api/sign-up`, requestOptions);
  // if (response.status === 201) {
  //   const data = await response.json();
  //   return data;
  // }
  if (response.status !== 201) {
    if (response.status === 409) {
      throw new Error("Signup Failed");
      // const data = await response.json();
      // alert(data.error || 'An error occurred during sign up. Use a registered shelter email');
      // return data.message;
    } else {
      throw new Error(
        `Received status ${response.status} when signing up. Expected 201`
      );
    }
  }
  const data = await response.json();
  return data;
};

export const logoutService = async () => {
  const requestOptions = {
    method: "POST",
    credentials: "include",
  };

  const response = await fetch(`/api/logout`, requestOptions);
  return response;
};

export const refreshToken = async () => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  };

  const response = await fetch(`/api/refresh-token`, requestOptions);
  if (response.status !== 200) {
    if (response.status == 401) {
      throw new Error("Unauthorised")
    }
    else {
      throw new Error(response.status, ": refresh failed");
    }
  }

  const data = await response.json();
  return data;
};

