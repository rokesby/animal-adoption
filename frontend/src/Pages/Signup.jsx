import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useContext } from "react";
import Context from "../../components/Context/Context";

import "./signUpPage.css";

import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Alert from "@mui/material/Alert";
import ContentPasteIcon from "@mui/icons-material/ContentPaste";
import Box from "@mui/material/Box";
import CardHeader from "@mui/material/CardHeader";

import { signup } from "../../services/authentication";
import { InputAdornment } from "@mui/material";

export const SignupPage = () => {
  const { authStatus, setAuthStatus } = useContext(Context);
  const [message, setMessage] = useState("");

  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleUpdateFormData = (id, value) => {
    setFormData({ ...formData, [id]: value 

    });

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (formData.password === formData.confirmPassword) {
      try {
        const data = await signup(formData);
        if (data === "User with email provided already exists") {
          setMessage(data);
        } else {
          navigate("/", { state: [0, data.message] });
        }
      } catch (err) {
        console.error(err);
        navigate("/signup");
      }
    }
  };

  return (
    <>
      {!authStatus && (
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
              title="Sign Up"
              subheader="Please enter your details"
              style={{ textAlign: "left" }}
            />

            <CardContent
              data-testid="user-card"
              component="form"
              id="signup-form"
              onSubmit={handleSubmit}
            >
              {formData.password !== formData.confirmPassword && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  Passwords don't match
                </Alert>
              )}

              <Typography gutterBottom variant="p" component="div">
                {/* <label htmlFor="firstName">First Name</label> */}
              </Typography>
              <TextField
                inputProps={{
                  "data-testid": "none",
                }}
                InputLabelProps={{ shrink: true }}
                label="First Name"
                placeholder="e.g. John"
                fullWidth
                size="small"
                variant="outlined"
                id="firstName"
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={(e) =>
                  handleUpdateFormData("firstName", e.target.value)
                }
                sx={{ mb: 3 }}
              />
              <Typography gutterBottom variant="p" component="div">
                {/* <label htmlFor="lastName">Last Name</label> */}
              </Typography>
              <TextField
                inputProps={{
                  "data-testid": "none",
                }}
                InputLabelProps={{ shrink: true }}
                label="Last Name"
                placeholder="e.g. Smith"
                fullWidth
                size="small"
                variant="outlined"
                id="lastName"
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={(e) =>
                  handleUpdateFormData("lastName", e.target.value)
                }
                sx={{ mb: 3 }}
              />

              <Typography gutterBottom variant="p" component="div">
                {/* <label htmlFor="email">Email</label> */}
              </Typography>
              <TextField
                inputProps={{
                  "data-testid": "none",
                }}
                InputLabelProps={{ shrink: true }}
                label="Email"
                placeholder="john@example.com"
                fullWidth
                size="small"
                variant="outlined"
                id="email"
                type="email"
                name="email"
                value={formData.email}
                onChange={(e) => handleUpdateFormData("email", e.target.value)}
                sx={{ mb: 3 }}
              />

              <Typography gutterBottom variant="p" component="div">
                {/* <label htmlFor="password">Password</label> */}
              </Typography>
              <TextField
                inputProps={{
                  "data-testid": "none",
                }}
                InputLabelProps={{ shrink: true }}
                label="Password"
                placeholder="Choose a strong one"
                fullWidth
                size="small"
                variant="outlined"
                id="password"
                type="password"
                name="password"
                value={formData.password}
                onChange={(e) =>
                  handleUpdateFormData("password", e.target.value)
                }
                sx={{ mb: 3 }}
              />

              <Typography gutterBottom variant="p" component="div">
                {/* <label htmlFor="confirmPassword">Confirm Password</label> */}
              </Typography>
              <TextField
                inputProps={{
                  "data-testid": "none",
                }}
                InputLabelProps={{ shrink: true }}
                label="Confirm Password"
                placeholder="Confirm it"
                fullWidth
                size="small"
                variant="outlined"
                id="confirmPassword"
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={(e) =>
                  handleUpdateFormData("confirmPassword", e.target.value)
                }
                sx={{ mb: 3 }}
              />

              <Typography gutterBottom variant="p" component="div">
                {/* <label htmlFor="image">Profile Photo URL</label> */}
              </Typography>
              <TextField
                InputProps={{
                  "data-testid": "none",
                  endAdornment: (
                    <InputAdornment position="end">
                      {/* <IconButton edge="end" color="primary"> */}
                      <ContentPasteIcon onClick={(e) => handlePaste(e)} />
                      {/* <button onClick={(e) => handlePaste(e)}>Paste</button> */}
                      {/* </IconButton> */}
                    </InputAdornment>
                  ),
                }}
                InputLabelProps={{ shrink: true }}
                label="Profile Photo URL"
                placeholder="accepted formats: PNG, JPG, BMP"
                fullWidth
                size="small"
                variant="outlined"
                id="image"
                type="text"
                name="image"
                value={formData.image}
                onChange={(e) => handleUpdateFormData("image", e.target.value)}
                sx={{ mb: 3 }}
              />

              <Typography variant="body1" color="text.secondary">
                {/* {email} */}
              </Typography>
            </CardContent>

            <CardActions>
              <Button
                data-testid="_submit-button"
                type="submit"
                form="signup-form"
                variant="contained"
              >
                Submit
              </Button>
            </CardActions>
          </Card>
        </>
      )}
    </>
  );
};

export default SignupPage;