import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import CardHeader from "@mui/material/CardHeader";
import { AuthProvider, useAuth } from "../../components/Context/AuthProvider"

export const SignUpPage = () => {
  const {token, signup} = useAuth()
  const [errorMessage, setErrorMessage] = useState("");
  const [message, setMessage] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [success, setSuccess] = useState(false)

  const navigate = useNavigate();

  const handleUpdateFormData = (id, value) => {
    setFormData({ ...formData, [id]: value });
    if (id === "password") {
      validatePassword(value);
    }
  };

  const validatePassword = (password) => {
    const errors = [];

    if (password.length < 8) {
      errors.push("Password must be at least 8 characters long.");
    }
    if (!/[A-Z]/.test(password)) {
      errors.push("Password must contain at least one uppercase letter.");
    }
    if (!/[a-z]/.test(password)) {
      errors.push("Password must contain at least one lowercase letter.");
    }
    if (!/\d/.test(password)) {
      errors.push("Password must contain at least one digit.");
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push("Password must contain at least one special character.");
    }

    setPasswordError(errors.join(" "));
    return errors.length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage("")
    if (passwordError) {
      setMessage("Please fix the password errors");
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      setMessage("Passwords don't match");
      return;
    }

    try {
      const success = await signup(formData);
      if (success) {
        console.log('successful signup')
        // navigate("/create-advert")
        setSuccess(true)
        setFormData({
          first_name: "",
          last_name: "",
          email: "",
          password: "",
          confirmPassword: "",
        })
      }
     
    } catch (err) {
      console.error(err);
      setErrorMessage("Error signing up. Please try again.");
    }
  };

  return (
    <>
      {message && (
        <Box display="flex" justifyContent="center" alignItems="center">
          <Alert severity="error" sx={{ width: "50vw", mt: 2 }}>
            {message}
          </Alert>
        </Box>
      )}

      <Card sx={{ width: "50vh", margin: "0 auto", padding: "0.1em", mb: 3, mt: 10, color: '#003554' }}>
        <CardHeader title="Sign Up" subheader="Please enter your details" style={{ textAlign: "left" }} />

        <CardContent component="form" id="signup-form" onSubmit={handleSubmit}>
          {passwordError && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {passwordError}
            </Alert>
          )}

          <TextField
            inputProps={{
              "data-testid": "none",
            }}
            label="First Name"
            placeholder="e.g. Steve"
            fullWidth
            size="small"
            variant="outlined"
            id="first_name"
            type="text"
            value={formData.first_name}
            onChange={(e) => handleUpdateFormData("first_name", e.target.value)}
            sx={{ mb: 3 }}
          />

          <TextField
          inputProps={{
            "data-testid": "none",
          }}
            label="Last Name"
            placeholder="e.g. Alex"
            fullWidth
            size="small"
            variant="outlined"
            id="last_name"
            type="text"
            value={formData.last_name}
            onChange={(e) => handleUpdateFormData("last_name", e.target.value)}
            sx={{ mb: 3 }}
          />

          <TextField
            inputProps={{
              "data-testid": "none",
            }}
            InputLabelProps={{ shrink: true }}
            label="Email"
            placeholder="steve@example.com"
            fullWidth
            size="small"
            variant="outlined"
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => handleUpdateFormData("email", e.target.value)}
            sx={{ mb: 3 }}
          />

          <TextField
            inputProps={{
              "data-testid": "none",
            }}
            label="Password"
            placeholder="Choose a strong one"
            fullWidth
            size="small"
            variant="outlined"
            id="password"
            type="password"
            value={formData.password}
            onChange={(e) => handleUpdateFormData("password", e.target.value)}
            sx={{ mb: 3 }}
          />

          <TextField
            inputProps={{
              "data-testid": "none",
            }}
            label="Confirm Password"
            placeholder="Confirm Password"
            fullWidth
            size="small"
            variant="outlined"
            id="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={(e) => handleUpdateFormData("confirmPassword", e.target.value)}
            sx={{ mb: 3 }}
          />

          <CardActions>
            <Button data-testid="submit-button" type="submit" form="signup-form" variant="contained"
            sx={{
              fontFamily: 'Arial, sans-serif',
              backgroundColor: '#003554',
              color: '#FFFACA',
              '&:hover': {
                backgroundColor: '#557B71',
              },
            }}>
              Submit
            </Button>
          </CardActions>
        </CardContent>
        {success && (
          <Alert severity="success">Sign up successful. Please check your email to verify your account</Alert>
        )}
        {errorMessage && (
          <Alert severity="error">{errorMessage}</Alert>
        )}
        
      </Card>
      
    </>
  );
};

export default SignUpPage;