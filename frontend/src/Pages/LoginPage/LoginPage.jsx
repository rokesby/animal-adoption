import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Login from "../../Components/Login/Login";
import { getUsers, getUserById } from "../../services/users"
// import { useContext } from "react";
// import Context from "../../components/Context/Context";
import {Button, Card, CardContent, CardHeader, Box, TextField, CardActions, Typography } from "@mui/material";
import PetsIcon from '@mui/icons-material/Pets';


export const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("")
  const [userData, setUserData] = useState("")
  const navigate = useNavigate();

  const handleEmailChange = (event) => {
    // const token = localStorage.getItem("token");
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    // const token = localStorage.getItem("token");
    setPassword(event.target.value);
  };

  const handleSubmit = async (event) => {
    const token = localStorage.getItem("token"); //need to set up 
    event.preventDefault();
    if (token) {
      try {
        // await login(token, email, password); need to create the login service
        const data = await getUserById(email, password)
        setUserData(data);
        navigate("/listings");
        setEmail("");
        setPassword("");
        setError("")
      } catch (err) {
        setUserData(null)
        setError(err.message)
        setEmail("");
        setPassword("");
        navigate("/login");
      }
    }
  };

  return (
    <>
       <Card 
      sx={{
        width: "90vh",
        margin: "0 auto",
        padding: "0.1em",
        mt: 3,
      }}
    > 

      <CardContent
        component="form"
        id="post-form"
        onSubmit={handleSubmit}
      >
        <Typography variant="h2"  sx={{mb: 2}}>Login</Typography>
        {/* <PetsIcon sx={{mb: 2}}/> */}
        <TextField
          inputProps={{
            "data-testid": "username",
          }}
          sx={{mb: 2}}
          label="Email Address"
          fullWidth
          size="small"
          variant="outlined"
          id="username"
          type="text"
          name="message"
          value={email}
          onChange={handleEmailChange}

        />
        <TextField
          inputProps={{
            "data-testid": "password",
          }}
          label="Password"
          fullWidth
          size="small"
          variant="outlined"
          id="password"
          type="text"
          name="message"
          value={password}
          onChange={handlePasswordChange}
          helperText={error}

        />
      </CardContent>
      <CardActions sx={{ display:"flex" , justifyContent:"right", mr: 1.3}}>
        <Button
          data-testid="_submit-button"
          type="submit"
          form="post-form"
          variant="contained"
          endIcon={<PetsIcon />}
        >
          Login
        </Button>
      </CardActions>
    </Card>
    </>
  );
}
