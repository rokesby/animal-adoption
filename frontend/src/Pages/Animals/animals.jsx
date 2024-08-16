import { useState, useEffect } from "react";
import { getAnimals } from "../../services/animals";
import AnimalCard from "../../components/AnimalCard/animalcard";

// This component fetches all the animals from the database and displays them in a card format.
  const AllAnimals = () => {
  const [animalsState, setAnimalsState] = useState([]);

  const fetchAnimals = () => {
    getAnimals()
      .then((data) => {
        setAnimalsState(data.animals);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  useEffect(() => {
    fetchAnimals();
  }, []);

  return (
    <>
      <h2>Animals who need a home</h2>
      {animalsState.map((animal) => {
        const { id, image, name, breed, age, location } = animal;
        return (
          <>
            <div
              key={id}
              style={{
                margin: "1em",
                overflow: "hidden",
                display: "inline-block",
                flexDirection: "row",
              }}
            >
              <AnimalCard
                image={image}
                name={name}
                age={age}
                breed={breed}
                location={location}
                button1Text={`Meet ${name}`}
              />
            </div>
          </>
        );
      })}
    </>
  );
};

export default AllAnimals;
