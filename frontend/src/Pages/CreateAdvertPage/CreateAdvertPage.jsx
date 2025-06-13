import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardContent,
  CardActions,
  CardHeader,
  Box,
  Alert,
  IconButton,
} from "@mui/material";
import { createAnimal } from "../../services/animals";
import { Add, Remove } from "@mui/icons-material";
import { AuthProvider, useAuth } from "../../components/Context/AuthProvider";
import {InputFileUpload} from "../../components/MaterialComponents/InputFileUpload"


export const CreateAdvertPage = () => {
  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    species: "",
    age: 0, 
    breed: "",
    location: "",
    male: true,
    bio: "",
    neutered: false,
    livesWithChildren: false,
    images: 0,
  });
  const [files, setFiles] = useState(null);
  const {authFetch, isAuthenticated} = useAuth()
  const navigate = useNavigate();

  // Check for the token / navigate to 'login' if no token exists
  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated]);

  const handleUpdateFormData = (id, value) => {
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name || !formData.species || formData.age === "") {
      setMessage("Please fill in all required fields");
      return;
    }

    // try {
    //   const data = new FormData();
    //   for (const key in formData) {
      //     data.append(key, formData[key]);

    try {
      const animal = await createAnimal(authFetch,{
        name: formData.name,
        species: formData.species,
        age: formData.age,
        breed: formData.breed,
        location: formData.location,
        male: formData.male,
        bio: formData.bio,
        neutered: formData.neutered,
        lives_with_children: formData.livesWithChildren,
        images: formData.images
      });

      if (animal.status === 201) {
        const newAnimalId = animal.data.id;
        // Upload images to Bucket here
        console.log(files)
        navigate(`/animals/${newAnimalId}`);
      } else {
        throw new Error("Failed to create animal");
      }
    } catch (err) {
      console.error(err);
      setMessage("Error creating advert. Please try again.");
    }
  };

  const handleAgeChange = (amount) => {
    setFormData((prevData) => ({
      ...prevData,
      age: Math.max(0, prevData.age + amount), // Age is a positive num
    }));
  };

  const handleFileUploadData = (e) => {
    console.log(e.target.files)
    if(e.target.files) {
        setFiles(e.target.files)
    }
}

  return (
    <>
      {message && (
        <Box display="flex" justifyContent="center" alignItems="center">
          <Alert
            data-testid="_message"
            severity="error"
            sx={{ width: "50vw", mt: 2 }}
          >
            {message}
          </Alert>
        </Box>
      )}

      <Card
        sx={{
          width: "50vh",
          margin: "0 auto",
          padding: "0.1em",
          mb: 3,
          mt: 10,
        }}
      >
        <CardHeader
          title="Create Animal Advert"
          subheader="Please enter the animal's details"
          style={{ textAlign: "left" }}
        />

        <CardContent
          component="form"
          id="create-advert-form"
          onSubmit={handleSubmit}
        >
          <TextField
            label="Name"
            value={formData.name}
            onChange={(e) => handleUpdateFormData("name", e.target.value)}
            fullWidth
            size="small"
            variant="outlined"
            required
            sx={{ mb: 3 }}
          />

          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Species</InputLabel>
            <Select
              value={formData.species}
              onChange={(e) => handleUpdateFormData("species", e.target.value)}
              fullWidth
              size="small"
              variant="outlined"
              required
            >
              <MenuItem value="Dog">Dog</MenuItem>
              <MenuItem value="Cat">Cat</MenuItem>
              <MenuItem value="Rabbit">Rabbit</MenuItem>
              <MenuItem value="Other">Other</MenuItem>
            </Select>
          </FormControl>

          <Box display="flex" alignItems="center" sx={{ mb: 3 }}>
            <IconButton onClick={() => handleAgeChange(-1)}>
              <Remove />
            </IconButton>
            <TextField
              label="Age"
              value={formData.age}
              onChange={(e) => handleUpdateFormData("age", e.target.value)}
              type="number"
              InputProps={{ readOnly: true }}  // Makes the text field read-only
              size="small"
              variant="outlined"
              required
              sx={{ textAlign: "center" }}
            />
            <IconButton onClick={() => handleAgeChange(1)}>
              <Add />
            </IconButton>
          </Box>

          <TextField
            label="Breed"
            value={formData.breed}
            onChange={(e) => handleUpdateFormData("breed", e.target.value)}
            fullWidth
            size="small"
            variant="outlined"
            sx={{ mb: 3 }}
          />

          <TextField
            label="Location"
            value={formData.location}
            onChange={(e) => handleUpdateFormData("location", e.target.value)}
            fullWidth
            size="small"
            variant="outlined"
            required
            sx={{ mb: 3 }}
          />

          {/* <TextField
            label="Shelter_ID"
            value={formData.shelterId}
            onChange={(e) => handleUpdateFormData("shelterId", e.target.value)}
            fullWidth
            multiline
            size="small"
            variant="outlined"
            required
            sx={{ mb: 3 }}
          /> */}

          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Gender</InputLabel>
            <Select
              value={formData.male ? "true" : "false"}
              onChange={(e) =>
                handleUpdateFormData("male", e.target.value === "true")
              }
              fullWidth
              size="small"
              variant="outlined"
            >
              <MenuItem value="true">Male</MenuItem>
              <MenuItem value="false">Female</MenuItem>
            </Select>
          </FormControl>

          <TextField
            label="Bio"
            value={formData.bio}
            onChange={(e) => handleUpdateFormData("bio", e.target.value)}
            fullWidth
            multiline
            rows={4}
            size="small"
            variant="outlined"
            required
            sx={{ mb: 3 }}
          />

          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Neutered</InputLabel>
            <Select
              value={formData.neutered ? "true" : "false"}
              onChange={(e) =>
                handleUpdateFormData("neutered", e.target.value === "true")
              }
              fullWidth
              size="small"
              variant="outlined"
            >
              <MenuItem value="true">Yes</MenuItem>
              <MenuItem value="false">No</MenuItem>
            </Select>
          </FormControl>

          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Lives with Children</InputLabel>
            <Select
              value={formData.livesWithChildren ? "true" : "false"}
              onChange={(e) =>
                handleUpdateFormData(
                  "livesWithChildren",
                  e.target.value === "true"
                )
              }
              fullWidth
              size="small"
              variant="outlined"
            >
              <MenuItem value="true">Yes</MenuItem>
              <MenuItem value="false">No</MenuItem>
            </Select>
            <InputFileUpload handleFileUploadData={handleFileUploadData}/>
          </FormControl>
        </CardContent>

        <CardActions>
          <Button
            type="submit"
            form="create-advert-form"
            variant="contained"
            color="primary"
          >
            Submit
          </Button>
        </CardActions>
      </Card>
    </>
  );
};

export default CreateAdvertPage;