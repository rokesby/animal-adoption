//animals pages page  

import { useState, useEffect } from "react";
import { getAnimals } from "../../services/animals";
import AnimalCard from "../../components/AnimalCard/animalcard";
import { Box, Container } from "@mui/material";

// This component fetches all the animals from the database and displays them in a card format.
const AllAnimals = () => {
  const [animalsState, setAnimalsState] = useState([]);
  

  const fetchAnimals = () => {
    getAnimals()
      .then((data) => {
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

  return (
    <>
      <h2>Animals available for adoption</h2>
      <Container sx={{
        height:"100vh",
        overflow: 'auto'
      }}>
      {animalsState.length > 0 ? (
        <Box
          sx={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: {
              xs: 1,
              md: 4
            } 
          }}
        >
          {animalsState.map((animal) => {
            const { id, name, breed, age, profileImageId, location, shelter_id } = animal;
            return (
              <Box
                key={id} 
                sx={{
                  minWidth:"360px",
                  width: {
                    xs: '100%',
                    md: '30%'
                  },
                }}
              >
                <AnimalCard
                  id={id}
                  profileImageId={profileImageId}
                  name={name}
                  age={age}
                  breed={breed}
                  location={location}
                  button1Text={`Meet ${name}`}
                  linkUrl={`/animals/${id}`} 
                  shelter_id={shelter_id}
                />
              </Box>
            );
          })}
        </Box>
      ) : (
        <h2>No animals available at the moment.</h2>
      )}
      

      </Container>
    </>
  );
};

export default AllAnimals;