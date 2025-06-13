import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {Button, Card, CardContent, CardHeader, Box, TextField, CardActions, Typography } from "@mui/material";
import PetsIcon from '@mui/icons-material/Pets';
import { AuthProvider, useAuth } from "../../components/Context/AuthProvider"

export const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("")
  const [userData, setUserData] = useState("");
  const {token, setToken, isAuthenticated, setIsAuthenticated, login} = useAuth()
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/animals")
    } 
  }, [isAuthenticated]);


  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
      try {
        const success = await login(email, password)
        if (success) {
          navigate('/login')
        }
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
        <Typography variant="h2" sx={{ mb: 2, color: '#003554' }}>Login</Typography>
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
          type="email"
          name="email"
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
          type="password"
          name="password"
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
            sx={{
              fontFamily: 'Arial, sans-serif',
              backgroundColor: '#003554',
              color: '#FFFACA',
              '&:hover': {
                backgroundColor: '#557B71',
              },
            }}
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
