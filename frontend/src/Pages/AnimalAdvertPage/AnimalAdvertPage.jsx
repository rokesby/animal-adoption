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
  TextField,
  CardMedia
} from "@mui/material";
import { editAnimal, getSingleAnimal, updateAnimalActiveStatus } from "../../services/animals";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export const AnimalAdvertPage = () => {
  const [animalData, setAnimalData] = useState(null);
  const [formData, setFormData] = useState({});
  const [error, setError] = useState(null);
  const [isActive, setisActive] = useState(true);
  const [isEditMode, setisEditMode] = useState(false);
  const { id } = useParams();
  const navigate = useNavigate();

  // Get the JWT token from localStorage (or any other auth mechanism you're using)
  const token = localStorage.getItem("token");
  const shelter_id = localStorage.getItem("shelter_id");

  const specificSubstring = "unique_id";

  // HERE I AM EXPERIMENTING WITH GETTING AN IMAGE TO LOAD
  const realImage = animalData?.image && !animalData.image.includes(specificSubstring) // The '?' is added in bc animalData is set to null on line 19. Code was failing w/out it
  ? `${import.meta.env.VITE_BACKEND_URL}`+ "/upload/" + `${animalData.image}`
  : "https://placecats.com/265/265";

  console.log("AnimalAdvertPage received id:", id);

  useEffect(() => {
    const fetchAnimalData = async () => {
      try {
        const data = await getSingleAnimal(id);
        console.log("Fetched animal data:", data); 
        setAnimalData(data);
        setFormData(data)
      } catch (error) {
        console.error("Failed to fetch animal data:", error);
        setError("Failed to fetch animal data");
      }
    };

    fetchAnimalData();
  }, [id]);

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

  // THIS SECTION IS WHERE ALL THE EVENT HANDLERS ARE - MS

  const handleEditClick = () => {
    setisEditMode(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSaveChanges = async () => {
    try {
      const updatedAnimalData = { ...formData };
      const response = await editAnimal(token, id, updatedAnimalData);
      setAnimalData(response.data);
      setisEditMode(false);
    } catch (error) {
      console.error('Failed to update animal profile at this time', error);
      setError('Failed to update animal profile');
    }
  };

  const handleRemoveClick = async () => {
    console.log('We are attempting to change the isActive state to false')
    await updateAnimalActiveStatus(token, animalData.id, false)
    setisActive(false)
    alert('This animal profile has now been hidden from all animal listings')
    navigate('/animals')
  };
  console.log("Current isActive state:", isActive);

  return (
    <Card
      sx={{
        width: "50vh",
        margin: "0 auto",
        padding: "2em",
        mt: 10,
      }}
    >
      <CardMedia
        component="img"
        height="265"
        image={realImage}
        alt={`${animalData.name}'s image`}
      />
      <CardContent>
        {!isEditMode ? (
          <>
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
                    style={{ color: 'navy', fontWeight: 'bold' }} 
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
              Edit {animalData.name}'s profile
            </Button>
            <Button variant="contained" color="primary" onClick={handleRemoveClick}>
              Remove {animalData.name}'s profile
            </Button>
          </Box>
        )}
        </>
        ) : (
          <>
          <TextField
              label="Name"
              name="name"
              value={formData.name || ''}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Breed"
              name="breed"
              value={formData.breed || ''}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Age"
              name="age"
              value={formData.age || ''}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Bio"
              name="bio"
              value={formData.bio || ''}
              onChange={handleInputChange}
              fullWidth
              multiline
              sx={{ mb: 2 }}
            />
            <TextField
              label="Species"
              name="species"
              value={formData.species || ''}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Location"
              name="location"
              value={formData.location || ''}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <Box sx={{ mt: 2, textAlign: "center" }}>
              <Button variant="contained" color="primary" onClick={handleSaveChanges} sx={{ mr: 2 }}>
                Save
              </Button>
              <Button variant="outlined" color="secondary" onClick={() => setisEditMode(false)}>
                Cancel
              </Button>
            </Box>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default AnimalAdvertPage;