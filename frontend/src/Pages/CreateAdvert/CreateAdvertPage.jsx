import React, { useState } from 'react';
import { TextField, Button, Grid, Typography, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import { useNavigate } from "react-router-dom";

const CreateAdvertPage = () => {
    const [name, setName] = useState('');
    const [species, setSpecies] = useState('');
    const [age, setAge] = useState('');
    const [breed, setBreed] = useState('');
    const [location, setLocation] = useState('');
    const [male, setMale] = useState(true); 
    const [bio, setBio] = useState('');
    const [neutered, setNeutered] = useState(false);
    const [livesWithChildren, setLivesWithChildren] = useState(false);
    const [image, setImage] = useState(null);
    const [shelterId, setShelterId] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('name', name);
        formData.append('species', species);
        formData.append('age', age);
        formData.append('breed', breed);
        formData.append('location', location);
        formData.append('male', male);
        formData.append('bio', bio);
        formData.append('neutered', neutered);
        formData.append('lives_with_children', livesWithChildren);
        formData.append('image', image);
        formData.append('shelter_id', shelterId);


    };

    return (
        <Grid container spacing={3} direction="column" alignItems="center" justifyContent="center">
            <Grid item xs={12}>
                <Typography variant="h4">Create an Animal Advert</Typography>
            </Grid>
            <Grid item xs={12}>
                <form onSubmit={handleSubmit}>
                    <Grid container spacing={3}>
                        <Grid item xs={12}>
                            <TextField
                                label="Name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                fullWidth
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                label="Species"
                                value={species}
                                onChange={(e) => setSpecies(e.target.value)}
                                fullWidth
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                label="Age"
                                value={age}
                                onChange={(e) => setAge(e.target.value)}
                                fullWidth
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                label="Breed"
                                value={breed}
                                onChange={(e) => setBreed(e.target.value)}
                                fullWidth
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                label="Location"
                                value={location}
                                onChange={(e) => setLocation(e.target.value)}
                                fullWidth
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControl fullWidth>
                                <InputLabel>Gender</InputLabel>
                                <Select
                                    value={male}
                                    onChange={(e) => setMale(e.target.value === "true")}
                                    fullWidth
                                >
                                    <MenuItem value={true}>Male</MenuItem>
                                    <MenuItem value={false}>Female</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                label="Bio"
                                value={bio}
                                onChange={(e) => setBio(e.target.value)}
                                fullWidth
                                multiline
                                rows={4}
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControl fullWidth>
                                <InputLabel>Neutered</InputLabel>
                                <Select
                                    value={neutered}
                                    onChange={(e) => setNeutered(e.target.value === "true")}
                                    fullWidth
                                >
                                    <MenuItem value={true}>Yes</MenuItem>
                                    <MenuItem value={false}>No</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12}>
                            <FormControl fullWidth>
                                <InputLabel>Lives with Children</InputLabel>
                                <Select
                                    value={livesWithChildren}
                                    onChange={(e) => setLivesWithChildren(e.target.value === "true")}
                                    fullWidth
                                >
                                    <MenuItem value={true}>Yes</MenuItem>
                                    <MenuItem value={false}>No</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12}>
                            <Button
                                variant="contained"
                                component="label"
                            >
                                Upload Image
                                <input
                                    type="file"
                                    hidden
                                    onChange={(e) => setImage(e.target.files[0])}
                                />
                            </Button>
                        </Grid>
                        <Grid item xs={12}>
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                            >
                                Submit
                            </Button>
                        </Grid>
                    </Grid>
                </form>
            </Grid>
        </Grid>
    );
};

export default CreateAdvertPage;