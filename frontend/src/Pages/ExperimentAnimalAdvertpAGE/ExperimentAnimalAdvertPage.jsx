import { useState, useEffect } from "react";
import { getAnimals } from "../../services/animals";
import AnimalCard from "../../components/AnimalCard/animalcard";

// This component fetches all the animals from the database and displays them in a card format.
const AllAnimals = () => {
  const [animalsState, setAnimalsState] = useState([]);
  const [speciesFilter, setSpeciesFilter] = useState("all"); 

  const fetchAnimals = () => {
    getAnimals()
      .then((data) => {
        console.log("I have data");

        if (data && Array.isArray(data)) {
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

  // Function to handle radio button change
  const handleSpeciesChange = (event) => {
    setSpeciesFilter(event.target.value);
  };

  const filteredAnimals = animalsState.filter((animal) =>
    speciesFilter === "all" || animal.species === speciesFilter
  );

  return (
    <>
      <h2>Animals Who Need a Home</h2>

      <div>
        <label>
          <input
            type="radio"
            value="all"
            checked={speciesFilter === "all"}
            onChange={handleSpeciesChange}
          />
          All
        </label>
        <label>
          <input
            type="radio"
            value="cat"
            checked={speciesFilter === "cat"}
            onChange={handleSpeciesChange}
          />
          Cats
        </label>
        <label>
          <input
            type="radio"
            value="dog"
            checked={speciesFilter === "dog"}
            onChange={handleSpeciesChange}
          />
          Dogs
        </label>
        <label>
          <input
            type="radio"
            value="rabbit"
            checked={speciesFilter === "rabbit"}
            onChange={handleSpeciesChange}
          />
          Rabbits
        </label>
      </div>

      {filteredAnimals.length > 0 ? (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "20px",
          }}
        >
          {filteredAnimals.map((animal) => {
            const { id, image, name, breed, age, location } = animal;
            console.log("Image from DB: " + image);
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
