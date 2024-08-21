import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  Box,
  List,
  ListItem,
  ListItemText,
  Button, 
} from "@mui/material";
import { getSingleAnimal } from "../../services/animals";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export const AnimalAdvertPage = () => {
  const [animalData, setAnimalData] = useState(null);
  const [error, setError] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();

  // Get the JWT token from localStorage (or any other auth mechanism you're using)
  const token = localStorage.getItem("token");
  const shelter_id = localStorage.getItem("shelter_id");


  console.log("AnimalAdvertPage received id:", id);

  useEffect(() => {
    const fetchAnimalData = async () => {
      try {
        const data = await getSingleAnimal(id);
        console.log("Fetched animal data:", data); // Debugging line
        setAnimalData(data);
      } catch (error) {
        console.error("Failed to fetch animal data:", error);
        setError("Failed to fetch animal data");
      }
    };

    fetchAnimalData();
  }, [id]);

   // Enhanced condition to check if data is not just falsy but also an empty object
  if (error) {
    return (
      <Typography
        sx={{ mt: 10, textAlign: "center" }}
        variant="h6"
        color="error"
      >
        {error}
      </Typography>
    );
  }

// Debugging line to check if data is undefined, null, or empty
console.log("Current animalData state:", animalData);
  
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

  // Handle the "Edit" button click
  const handleEditClick = () => {
    navigate(`/edit-animal/${id}`);
  };

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
            <ListItem>
              <ListItemText 
                primary="Email" 
                secondary={
                  <a 
                    href={`mailto:${animalData.shelter.email}?subject=Inquiry%20about%20adopting%20${encodeURIComponent(animalData.name)}&body=Hi,%20I'm%20interested%20in%20adopting%20${encodeURIComponent(animalData.name)}.%20Could%20I%20get%20some%20more%20info?`}
                  >
                    {animalData.shelter.email}
                  </a>
                } 
              />
            </ListItem>
          </List>
        </Box>

        {/* Conditionally renderinf the "Edit" button if logged in AND if token.shelter_id == animals shelter id*/}
        {token && (shelter_id == animalData.shelter_id) && (
          <Box sx={{ mt: 4, textAlign: "center" }}>
            <Button variant="contained" color="primary" onClick={handleEditClick}>
              Edit Animal
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default AnimalAdvertPage;