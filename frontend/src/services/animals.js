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
// export const getsingleAnimal = async () => {
//   const requestOptions = {
//     method: "GET",
//     headers: {
//       // Authorization: `Bearer ${token}`,
//     },
//   };
//   try {
//     const response = await fetch(`${BACKEND_URL}/listings/<int:id>`, requestOptions);
//     if (response.status !== 200) {
//       throw new Error("Unable to fetch animals");
//     }
//     const data = await response.json();
//     return data || [];
//   } catch (error) {
//     console.error('Error:', error);
//     return [];
//   }
// };
// The animal object is what is created on CreateAdvertPage
// We pass it in through the services function here

// I've updated createAnimal to accept a token
export const createAnimal = async (token, animal) => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, // I've uncommented this to pass the token in the header.
    },
    body: JSON.stringify(animal),
  };
  try {
    console.log(`Making request to: ${BACKEND_URL}/listings`);
    const response = await fetch(`${BACKEND_URL}/listings`, requestOptions);
    if (!response.ok) {
      throw new Error("Error creating post");
    }
    const data = await response.json();
    return {
      status: response.status,
      message: 'Successfully created animal profile',
      data:data,
    };
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getSingleAnimal = async (id) => {
  const requestOptions = {
    method: "GET",
    headers: {
      // Authorization: `Bearer ${token}`,
    },
  };
  try {
    const response = await fetch(`${BACKEND_URL}/listings/${id}`, requestOptions);
    if (response.status !== 200) {
      throw new Error("Unable to fetch this animal");
    }
    const data = await response.json();
    return data; 

  } catch (error) {
    console.error('Error:', error);
  }
};







