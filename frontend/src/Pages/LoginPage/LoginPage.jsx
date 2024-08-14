import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Login from "../../Components/Login/Login";
// import { useContext } from "react";
// import Context from "../../components/Context/Context";
import {Button, Card, CardContent, CardHeader, Box, TextField, CardActions } from "@mui/material";


export const LoginPage = () => {
  const [loginForm, setLoginForm] = useState({});

  const handleEmailChange = (event) => {
    // const token = localStorage.getItem("token");
    setEmail({
      ...loginForm,
      email: event.target.value,
      password: event.target.value,
    });
  };

  const handleSubmit = () => {
    console.log("Submit")
  }

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

        <TextField
          inputProps={{
            "data-testid": "tusername",
          }}
          label="Email Address"
          fullWidth
          size="small"
          variant="outlined"
          id="login"
          type="text"
          name="message"
          value={loginForm.email}
          onChange={handleEmailChange}
          multiline
          rows={1}

        />
      </CardContent>
      <CardActions sx={{ display:"flex" , justifyContent:"right", mr: 1.3}}>
        <Button
          data-testid="_submit-button"
          type="submit"
          form="post-form"
          variant="contained"
        >
          Email
        </Button>
      </CardActions>
    </Card>
    </>
  );
}