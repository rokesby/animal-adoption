// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const signup = async (formData) => {
    const payload = {
      first_name: formData.first_name,
      last_name: formData.last_name,
      email: formData.email,
      password: formData.password,
      // confirmPassword: formData.confirmPassword,
      shelter_id: formData.shelter_id,
    //   image: formData.image,
    };
  
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    };
  
    let response = await fetch(`${BACKEND_URL}/signup`, requestOptions);
  
    // docs: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201
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
  