import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import mockData from "./mockData.json";

export const AnimalAdvertPage = () => {
  // const [animalData, setAnimalData] = useState(null);
  const [name, setName] = useState("");
  const [species, setSpecies] = useState(""); 
  const [age, setAge] = useState(""); 
  const [breed, setBreed] = useState(""); 
  const [location, setLocation] = useState("");      
  
  useEffect(() => {
// Temporary - mock data
    // setAnimalData(mockData);
    const fetchAnimalData = async () => {
      try {
        const data = await getSingleAnimal(animal_id);
        setName(data.name);
        setSpecies(data.species);
        setAge(data.age);
        setBreed(data.breed);
        setLocation(data.location);
      } catch (error) {
        console.error("Fail to fetch animal data");
      }
    }
  });

  if (!animalData) {
    return (
      <Typography
        sx={{ mt: 10, textAlign: "center" }}
        variant="h6"
        color="textSecondary"
      >
        Loading...
      </Typography>
    );
  }

  return (
    <Card
      sx={{
        width: "50vh",
        margin: "0 auto",
        padding: "2em",
        mt: 10,
      }}
    >
      <CardContent>
        <Typography variant="h4" component="div">
          {animalData.name}
        </Typography>
        <Typography variant="h6" color="textSecondary" sx={{ mb: 2 }}>
          {animalData.breed} - {animalData.age} years old
        </Typography>
        <Typography variant="body1" sx={{ mb: 2 }}>
          {animalData.bio}
        </Typography>
        <Box sx={{ mt: 4 }}>
          <List>
            <ListItem>
              <ListItemText primary="Species" secondary={animalData.species} />
            </ListItem>
            <ListItem>
              <ListItemText primary="Location" secondary={animalData.location} />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Gender"
                secondary={animalData.male ? "Male" : "Female"}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Neutered"
                secondary={animalData.neutered ? "Yes" : "No"}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Lives with Children"
                secondary={animalData.livesWithChildren ? "Yes" : "No"}
              />
            </ListItem>
          </List>
        </Box>
      </CardContent>
    </Card>
  );
};

export default AnimalAdvertPage;