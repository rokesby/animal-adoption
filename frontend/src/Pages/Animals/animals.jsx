import { useState, useEffect } from "react";
import { getAnimals } from "../../services/animals";
import AnimalCard from "../../components/AnimalCard/animalcard";
import LoginLogout from "../../components/LoginLogout/LoginLogout";

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
    <LoginLogout />
      <h2>Animals Who Need a Home</h2>
      {animalsState.length > 0 ? (
        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center" }}>
          {animalsState.map((animal) => {
            const { id, image, name, breed, age, location } = animal;
            console.log ("Image from DB: " + image);
            return (
              <AnimalCard
                key={id}
                image={image}
                name={name}
                age={age}
                breed={breed}
                location={location}
                button1Text={`Meet ${name}`}
                linkUrl={`/animals/${id}`}  // Assuming animal details are on /animals/:id
              />
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