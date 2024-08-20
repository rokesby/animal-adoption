//animals pages page  

import { useState, useEffect } from "react";
import { getAnimals } from "../../services/animals";
import AnimalCard from "../../components/AnimalCard/animalcard";

// This component fetches all the animals from the database and displays them in a card format.
const AllAnimals = () => {
  const [animalsState, setAnimalsState] = useState([]);

  const fetchAnimals = () => {
    getAnimals()
      .then((data) => {
        console.log("I have data");
        if (data && Array.isArray(data  )) {
          setAnimalsState(data);
        } else {
          console.error("Unexpected data format:", data);
        }
      })
      .catch((err) => {
        console.error("Error fetching animals:", err);
      });
  };

  useEffect(() => {
    fetchAnimals();
  }, []);

  return (
    <>
      <h2>Animals Who Need a Home</h2>
      {animalsState.length > 0 ? (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "20px", 
          }}
        >
          {animalsState.map((animal) => {
            const { id, image, name, breed, age, location } = animal;
            return (
              <div
                key={id} 
                style={{
                  flex: "1 1 calc(33.333% - 20px)", // Allows 3 cards per row
                  maxWidth: "calc(33.333% - 20px)", // Ensures cards are contained within the row
                  boxSizing: "border-box", 
                }}
              >
                <AnimalCard
                  image={image}
                  name={name}
                  age={age}
                  breed={breed}
                  location={location}
                  button1Text={`Meet ${name}`}
                  linkUrl={`/animals/${id}`} 
                />
              </div>
            );
          })}
        </div>
      ) : (
        <p>No animals available at the moment.</p>
      )}
    </>
  );
};

export default AllAnimals;