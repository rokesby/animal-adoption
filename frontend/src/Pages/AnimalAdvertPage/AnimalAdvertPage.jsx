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
  CardMedia,
} from "@mui/material";
import {
  editAnimal,
  getSingleAnimal,
  updateAnimalActiveStatus,
} from "../../services/animals";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuth, AuthProvider } from "../../components/Context/AuthProvider";
import { buildImageUrl } from "../../utils/gcpUtils";

export const AnimalAdvertPage = () => {
  const [animalData, setAnimalData] = useState(null);
  const [formData, setFormData] = useState({});
  const [profileImage, setProfileImage] = useState("/profile_placeholder.png");
  const [error, setError] = useState(null);
  const [isActive, setisActive] = useState(true);
  const [isEditMode, setisEditMode] = useState(false);
  const { id } = useParams();
  const { authFetch, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAnimalData = async () => {
      try {
        const data = await getSingleAnimal(id);
        setAnimalData(data);
        setFormData(data);
        if (data.images != 0) {
          const profileImageUrl = buildImageUrl(data.id, data.profileImageId);
          setProfileImage(profileImageUrl);
          // console.log(profileImageUrl)
        }
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
      const response = await editAnimal(authFetch, id, updatedAnimalData);
      setAnimalData(response.data);
      setisEditMode(false);
    } catch (error) {
      console.error("Failed to update animal profile at this time", error);
      setError("Failed to update animal profile");
    }
  };

  const handleRemoveClick = async () => {
    console.log("We are attempting to change the isActive state to false");
    await updateAnimalActiveStatus(authFetch, animalData.id, false);
    setisActive(false);
    alert("This animal profile has now been hidden from all animal listings");
    navigate("/animals");
  };

  return (
    <Card
      square={true}
      sx={{
        display: "flex",
        flexDirection: "column",
        width: {
          xs: "100%",
          md: "80%",
        },
        margin: "auto",
        height: "90vh",
        minHeight: 'min-content',
        // border: '2px solid blue',
      }}
    >
      <CardMedia
        component="img"
        sx={{
          maxHeight: '5rem',
          maxHeight: {
            xs: "30rem",
            // sm: "30rem",
          },
          objectFit: {
            xs: "cover",
          },
        }}
        image={profileImage}
        alt={`${animalData.name}'s image`}
      />
      <CardContent
        sx={{
          minHeight: 'min-content',
          // border: "2px solid green",
        }}
      >
        {!isEditMode ? (
          <>
            <Box sx={{
              flexDirection: "column",
              
            }}>
              <Typography variant="h4">{animalData.name}</Typography>
              <Typography variant="h6" color="textSecondary" sx={{ mb: "1em" }}>
                {animalData.breed} - {animalData.age} years old
              </Typography>
              <Typography variant="body1" sx={{ mb: "1em" }}>
                {animalData.bio}
              </Typography>
            </Box>
            <List
              sx={{
                display: "flex",
                // border: "2px solid pink",
                flexDirection: 'row',
                minHeight:'min-content',
                flexWrap: 'wrap',
                "& > *": {
                  display: 'flex',
                  flex: {
                    xs: "1 1 100%",
                    md: "1 1 50%",
                    // lg: "1 1 25%",
                  },

                  // border: '2px solid purple',
                },
              }}
            >
              <ListItem>
                <ListItemText
                  primary="Species"
                  secondary={animalData.species}
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Location"
                  secondary={animalData.location}
                />
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
              {/* This should be a button */}
              {/* <ListItem>
                <ListItemText primary="Email" 
                  secondary="Log in to email"
                />
              </ListItem> */}
            </List>

            {/* Conditionally renderinf the "Edit" button if logged in AND if token.shelter_id == animals shelter id*/}
            {isAuthenticated && animalData.shelter_id == 1 && (
              <Box
                sx={{
                  mt: 4,
                  textAlign: "center",
                  display: "flex",
                  justifyContent: "center",
                  gap: 2,
                }}
              >
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleEditClick}
                >
                  Edit {animalData.name}'s profile
                </Button>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleRemoveClick}
                >
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
              value={formData.name || ""}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Breed"
              name="breed"
              value={formData.breed || ""}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Age"
              name="age"
              value={formData.age || ""}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Bio"
              name="bio"
              value={formData.bio || ""}
              onChange={handleInputChange}
              fullWidth
              multiline
              sx={{ mb: 2 }}
            />
            <TextField
              label="Species"
              name="species"
              value={formData.species || ""}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <TextField
              label="Location"
              name="location"
              value={formData.location || ""}
              onChange={handleInputChange}
              fullWidth
              sx={{ mb: 2 }}
            />
            <Box sx={{ mt: 2, textAlign: "center" }}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSaveChanges}
                sx={{ mr: 2 }}
              >
                Save
              </Button>
              <Button
                variant="outlined"
                color="secondary"
                onClick={() => setisEditMode(false)}
              >
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
