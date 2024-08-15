// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const getUsers = async () => {
    const requestOptions = {
      method: "GET",
    //   headers: {
    //     Authorization: `Bearer ${token}`,
    //   },
    };
  
    const response = await fetch(`${BACKEND_URL}/users`);
  
    console.log(response.status);
  
    if (response.status !== 200) {
      throw new Error("Unable to fetch users");
    }
  
    const data = await response.json();
    return data;
  };