import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../services/authentication"
// import { useContext } from "react";
// import Context from "../../components/Context/Context";
import {Button, Card, CardContent, CardHeader, Box, TextField, CardActions, Typography } from "@mui/material";
import PetsIcon from '@mui/icons-material/Pets';


export const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("")
  const [userData, setUserData] = useState("");
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  
  // get token from local storage
  
  useEffect(() => {
    if (token) {
     navigate("/animals")
    }
  }, [token]);


  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
      try {
        const data = await login(email, password)
        localStorage.setItem("token", data.token)
        localStorage.setItem("user_id", data.user_id)
        localStorage.setItem("shelter_id", data.shelter_id)
        navigate("/create-advert");
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
  };

  return (
    <>
    <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh'
        }}>
    <Card 
      sx={{
        width: "400px",
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
    </Box>
    </>
  );
}
