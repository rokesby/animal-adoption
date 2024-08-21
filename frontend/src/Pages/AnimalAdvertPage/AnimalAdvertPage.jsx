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
import { editAnimal, getSingleAnimal, updateAnimalActiveStatus } from "../../services/animals";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export const AnimalAdvertPage = () => {
  const [animalData, setAnimalData] = useState(null);
  const [error, setError] = useState(null);
  const [isActive, setisActive] = useState(true)
  const [isEditMode, setIsEditMode] = useState(false)
  const { id } = useParams();
  const navigate = useNavigate();

  // Get the JWT token from localStorage (or any other auth mechanism you're using)
  const token = localStorage.getItem("token");
  const shelter_id = Number(localStorage.getItem("shelter_id"));
  console.log(token)
  console.log(shelter_id)


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
  // MARYA - here I've defined the functions which allow input to be changed and saved

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSaveChanges = async () => {
    try {
      const updatedAnimalData = { ...formData };
      const response = await editAnimal(token, id, updatedAnimalData);
      setAnimalData(response.data);
      setIsEditMode(false);
    } catch (error) {
      console.error("Failed to update animal profile:", error);
      setError("Failed to update animal profile");
    }
  };

  
  // const handleEditClick = async () => {
  //   await editAnimal(token, animalData.id)
  // };

  const handleRemoveClick = async () => {
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
                      >
                        {animalData.shelter.email}
                      </a>
                    } 
                  />
                </ListItem>
              </List>
            </Box>
  
            {/* Conditionally rendering the "Edit" button if logged in AND if token.shelter_id == animal's shelter id */}
            {token && (shelter_id === animalData.shelter_id) && (
              <Box sx={{ mt: 4, textAlign: "center" }}>
                {/* <Button variant="contained" color="primary" onClick={handleEditClick}>
                  Edit {animalData.name}'s profile
                </Button> */}
                <Button variant="contained" color="primary" onClick={handleRemoveClick} sx={{ mt: 2 }}>
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
              <Button variant="outlined" color="secondary" onClick={() => setIsEditMode(false)}>
                Cancel
              </Button>
            </Box>
          </>
        )}
      </CardContent>
    </Card>
  );
};

//   return (
//     <Card
//       sx={{
//         width: "50vh",
//         margin: "0 auto",
//         padding: "2em",
//         mt: 10,
//       }}
//     >
//       <CardContent>
//       {!isEditMode ? (
//         <>
//         <Typography variant="h4" component="div">
//           {animalData.name}
//         </Typography>
//         <Typography variant="h6" color="textSecondary" sx={{ mb: 2 }}>
//           {animalData.breed} - {animalData.age} years old
//         </Typography>
//         <Typography variant="body1" sx={{ mb: 2 }}>
//           {animalData.bio}
//         </Typography>
//         <Box sx={{ mt: 4 }}>
//           <List>
//             <ListItem>
//               <ListItemText primary="Species" secondary={animalData.species} />
//             </ListItem>
//             <ListItem>
//               <ListItemText primary="Location" secondary={animalData.location} />
//             </ListItem>
//             <ListItem>
//               <ListItemText
//                 primary="Gender"
//                 secondary={animalData.male ? "Male" : "Female"}
//               />
//             </ListItem>
//             <ListItem>
//               <ListItemText
//                 primary="Neutered"
//                 secondary={animalData.neutered ? "Yes" : "No"}
//               />
//             </ListItem>
//             <ListItem>
//               <ListItemText
//                 primary="Lives with Children"
//                 secondary={animalData.livesWithChildren ? "Yes" : "No"}
//               />
//             </ListItem>
//             <ListItem>
//               <ListItemText 
//                 primary="Email" 
//                 secondary={
//                   <a 
//                     href={`mailto:${animalData.shelter.email}?subject=Inquiry%20about%20adopting%20${encodeURIComponent(animalData.name)}&body=Hi,%20I'm%20interested%20in%20adopting%20${encodeURIComponent(animalData.name)}.%20Could%20I%20get%20some%20more%20info?`}
//                   >
//                     {animalData.shelter.email}
//                   </a>
//                 } 
//               />
//             </ListItem>
//           </List>
//         </Box>

//         {/* Conditionally renderinf the "Edit" button if logged in AND if token.shelter_id == animals shelter id*/}
//         {token && (shelter_id == animalData.shelter_id) && (
//           <Box sx={{ mt: 4, textAlign: "center" }}>
//             <Button variant="contained" color="primary" onClick={handleEditClick}>
//               Edit {animalData.name}'s profile
//             </Button>
//             </>
//         ) : (
//           <>
//             <TextField
//               label="Name"
//               name="name"
//               value={formData.name || ''}
//               onChange={handleInputChange}
//               fullWidth
//               sx={{ mb: 2 }}
//             />
//             <TextField
//               label="Breed"
//               name="breed"
//               value={formData.breed || ''}
//               onChange={handleInputChange}
//               fullWidth
//               sx={{ mb: 2 }}
//             />
//             <TextField
//               label="Age"
//               name="age"
//               value={formData.age || ''}
//               onChange={handleInputChange}
//               fullWidth
//               sx={{ mb: 2 }}
//             />
//             <TextField
//               label="Bio"
//               name="bio"
//               value={formData.bio || ''}
//               onChange={handleInputChange}
//               fullWidth
//               multiline
//               sx={{ mb: 2 }}
//             />
//             <TextField
//               label="Species"
//               name="species"
//               value={formData.species || ''}
//               onChange={handleInputChange}
//               fullWidth
//               sx={{ mb: 2 }}
//             />
//             <TextField
//               label="Location"
//               name="location"
//               value={formData.location || ''}
//               onChange={handleInputChange}
//               fullWidth
//               sx={{ mb: 2 }}
//             />
//             {/* Add other fields as needed */}
//             <Button variant="contained" color="primary" onClick={handleSaveChanges} sx={{ mr: 2 }}>
//               Save
//             </Button>
//             <Button variant="outlined" color="secondary" onClick={() => setIsEditMode(false)}>
//               Cancel
//             </Button>
//           </>
//             <Button variant="contained" color="primary" onClick={handleRemoveClick}>
//               Remove {animalData.name}'s profile
//             </Button>
//           </Box>
//         )}
//       </CardContent>
//     </Card>
//   );
// };

export default AnimalAdvertPage;