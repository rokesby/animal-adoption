import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {Button, Card, CardContent, CardHeader, Box, TextField, CardActions, Typography } from "@mui/material";
import PetsIcon from '@mui/icons-material/Pets';
import { AuthProvider, useAuth } from "../../components/Context/AuthProvider"
import Alert from "@mui/material/Alert";
import SendIcon from '@mui/icons-material/Send';
import { reVerification } from "../../services/authService"

export const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("")
  const [errorMessage, setErrorMessage] = useState("")
  const [verifySuccess, setVerifySuccess] = useState("")
  const [userData, setUserData] = useState("");
  const {isAuthenticated, login} = useAuth()
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
    // const eventId = event.nativeEvent.submitter.id
    setVerifySuccess("")
    setErrorMessage("")
      try {
        const response = await login(email, password)
        if (response == true) {
          navigate('/animals')
          console.log('success!!!', response)
        } else {
          setErrorMessage(response.message)
          setUserData(null)
          setPassword("")
          console.log(response.message)
        }
  
      } catch (err) {
        console.log(' in trycatch:', err)
        setUserData(null)
        setErrorMessage(err.message)
        console.log(err.message)
    }
  };

  const handleReverification = async () => {

    try {
      const verification = await reVerification(email)
      console.log('success', verification)
      setErrorMessage("")
      setVerifySuccess(verification.message)
      
    } catch (error) {
      setErrorMessage(error.message)
    }
    

  }

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
        id="login-form"
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
          
          helperText={errorMessage}

        />
      </CardContent>
      <CardActions sx={{ display:"flex" , justifyContent:"right", mr: 1.3}}>
      <Button
            data-testid="_submit-button"
            id="submit-button"
            type="submit"
            form="login-form"
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
      {errorMessage && (
                <Alert 
                severity="error"
                action={
                <Button 
                type="button"
                // form="login-form"
                data-testid="_error-button"
                id="error-button"
                color="error" 
                size="small"
                variant="outlined"
                disableElevation
                onClick={handleReverification}
                endIcon={<SendIcon />}
                >
               {errorMessage == "Email or password is incorrect" ? "Reset Password" : "Resend"}
                </Button>}
                sx={{
                    marginTop: "1em",
                }}
                >
                    {errorMessage}
                </Alert>
            )}
      {verifySuccess && (
                <Alert 
                severity="success"
                sx={{
                    marginTop: "1em",
                }}
                >
                    {verifySuccess}
                </Alert>
            )}
    </Card>
    </Box>
    </>
  );
}
