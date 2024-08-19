import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Link } from "react-router-dom";  

//import { useContext } from "react";
//import Context from "../Context/Context";

const Navbar = () => {
  //const { authStatus, setAuthStatus } = useContext(Context);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar
        data-testid="_nav"
        position="static"
        color="transparent"
        sx={{
          width: "100vw",
        }}
      >
        <Toolbar>
        <Typography component={Link} to="/" color="inherit" variant="h6">
  🐾 For a Cause
</Typography>

          <Box sx={{ marginLeft: "auto" }}>
            <Button
              component={Link}
              to="/animals"
              data-testid="_animals"
              color="inherit"
            >
              Home
            </Button>
            <Button
              component={Link}
              to="/login"
              data-testid="_login"
              color="inherit"
            >
              Login
            </Button>
            <Button
              component={Link}
              to="/sign-up"
              data-testid="_signup"
              color="inherit"
            >
              Signup
            </Button>
          </Box>

          {/* <Box sx={{ marginLeft: "auto" }}>
            <Button
              component={Link}
              to="/create-advert"
              data-testid="_create-advert"
              color="inherit"
            >
              Create Advert
            </Button>
          </Box> */}
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;