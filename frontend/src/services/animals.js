const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const getAnimals = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        // Authorization: `Bearer ${token}`,
      },
    };
  
    try {
      const response = await fetch(`${BACKEND_URL}/listings`, requestOptions);
      if (response.status !== 200) {
        throw new Error("Unable to fetch animals");
      }
      const data = await response.json();
      return data || []; 
    } catch (error) {
      console.error('Error:', error);
      return [];
    }
};
