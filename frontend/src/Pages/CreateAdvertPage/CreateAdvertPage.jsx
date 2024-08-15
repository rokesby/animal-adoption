import { useState } from "react";
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
} from "@mui/material";

export const CreateAdvertPage = () => {
  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    species: "",
    age: "",
    breed: "",
    location: "",
    male: true,
    bio: "",
    neutered: false,
    livesWithChildren: false,
    image: null,
    shelterId: "",
  });

  const navigate = useNavigate();

  const handleUpdateFormData = (id, value) => {
    setFormData({ ...formData, [id]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.name || !formData.species || !formData.age) {
      setMessage("Please fill in all required fields");
      return;
    }

    try {
      const data = new FormData();
      for (const key in formData) {
        data.append(key, formData[key]);
      }

    } catch (err) {
      console.error(err);
      setMessage("Error creating advert. Please try again.");
    }
  };

  return (
    <>
      {message && (
        <Box display="flex" justifyContent="center" alignItems="center">
          <Alert
            data-testid="_message"
            severity="error"
            sx={{
              width: "50vw",
              mt: 2,
            }}
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

          <TextField
            label="Species"
            value={formData.species}
            onChange={(e) => handleUpdateFormData("species", e.target.value)}
            fullWidth
            size="small"
            variant="outlined"
            required
            sx={{ mb: 3 }}
          />

          <TextField
            label="Age"
            value={formData.age}
            onChange={(e) => handleUpdateFormData("age", e.target.value)}
            fullWidth
            size="small"
            variant="outlined"
            required
            sx={{ mb: 3 }}
          />
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

          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Gender</InputLabel>
            <Select
              value={formData.male}
              onChange={(e) =>
                handleUpdateFormData("male", e.target.value === "true")
              }
              fullWidth
              size="small"
              variant="outlined"
            >
              <MenuItem value={true}>Male</MenuItem>
              <MenuItem value={false}>Female</MenuItem>
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
              value={formData.neutered}
              onChange={(e) =>
                handleUpdateFormData("neutered", e.target.value === "true")
              }
              fullWidth
              size="small"
              variant="outlined"
            >
              <MenuItem value={true}>Yes</MenuItem>
              <MenuItem value={false}>No</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>Lives with Children</InputLabel>
            <Select
              value={formData.livesWithChildren}
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
              <MenuItem value={true}>Yes</MenuItem>
              <MenuItem value={false}>No</MenuItem>
            </Select>
          </FormControl>

          <Button variant="contained" component="label" sx={{ mb: 3 }}>
            Upload Image
            <input
              type="file"
              hidden
              onChange={(e) => handleUpdateFormData("image", e.target.files[0])}
            />
          </Button>
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
