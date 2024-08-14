import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Login from "../../Components/Login/Login";
// import { useContext } from "react";
// import Context from "../../components/Context/Context";
import {Button, Card, CardContent, CardHeader, Box, TextField, CardActions } from "@mui/material";


export const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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
        // I have taken setPost to handlePostChange - add validation for an empty post.
        // await login(token, email, password); need to create the login service
        console.log(email)
        console.log(password)
        navigate("/login");
        // props.fetchPosts();
        setEmail("");
        setPassword("");
      } catch (err) {
        console.error(err);
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

        <TextField
          inputProps={{
            "data-testid": "username",
          }}
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

        />
      </CardContent>
      <CardActions sx={{ display:"flex" , justifyContent:"right", mr: 1.3}}>
        <Button
          data-testid="_submit-button"
          type="submit"
          form="post-form"
          variant="contained"
        >
          Login
        </Button>
      </CardActions>
    </Card>
    </>
  );
}