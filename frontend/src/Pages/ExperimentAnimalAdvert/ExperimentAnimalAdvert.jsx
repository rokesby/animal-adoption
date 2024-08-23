import { useState, useEffect } from "react";
import { getAnimals } from "../../services/animals";
import AnimalCard from "../../components/AnimalCard/animalcard";

// This component fetches all the animals from the database and displays them in a card format.
const ExperimentalAllAnimals = () => {
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
            <h2>Can you give one of us a good home?</h2>

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
                        value="Cat"
                        checked={speciesFilter === "Cat"}
                        onChange={handleSpeciesChange}
                    />
                    Cats
                </label>
                <label>
                    <input
                        type="radio"
                        value="Dog"
                        checked={speciesFilter === "Dog"}
                        onChange={handleSpeciesChange}
                    />
                    Dogs
                </label>
                <label>
                    <input
                        type="radio"
                        value="Rabbit"
                        checked={speciesFilter === "Rabbit"}
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
                                    flex: "1 1 calc(33.333% - 20px)",
                                    maxWidth: "calc(33.333% - 20px)",
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

export default ExperimentalAllAnimals;