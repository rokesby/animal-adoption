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
export const createAnimal = async (animal) => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // Authorization: `Bearer ${token}`,
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
    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const getAnimals = async () => {
<<<<<<< HEAD
  const requestOptions = {
    method: "GET",
    headers: {
    "Content-Type": "application/json"
    },
  };

  const response = await fetch(`${BACKEND_URL}/animals`, requestOptions);

  console.log(response.status);

  if (response.status !== 200) {
    throw new Error("Unable to fetch animals");
  }

  const data = await response.json();
  return data;
};

export const getAnimal = async (id) => {
  const requestOptions = {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
  };

  const response = await fetch(`${BACKEND_URL}/animals/${id}`, requestOptions);
  if (response.status !== 200) {
    throw new Error("No animal found in backend");
  }

  const data = await response.json();
  return data;
};
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

export const createAnimal = async (animal) => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // Authorization: `Bearer ${token}`,
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
    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

