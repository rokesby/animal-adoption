// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
// import getUserById from "../services/users"

export const login = async (email, password) => {
    const payload = {
        email: email,
        password: password,
      }
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    };
    
    const response = await fetch(`${BACKEND_URL}/token`, requestOptions);
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

