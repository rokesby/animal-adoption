import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import { useEffect, useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthProvider, useAuth } from "../Context/AuthProvider";

const Navbar = () => {
  const navigate = useNavigate();
  const [loggedIn, setLoggedIn] = useState(false);
  const { logout, isAuthenticated } = useAuth()
  const [anchorElNav, setAnchorElNav] = useState(null);
  const [anchorElUser, setAnchorElUser] = useState(null);

  useEffect(() => {
    setLoggedIn(isAuthenticated);
    console.log('isAuthenticated = ', isAuthenticated)
  }, [isAuthenticated]);

  const handleLogoutClick = async () => {
    await logout()
  };

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };


  return (
    <AppBar position="static" 
        sx={{ backgroundColor: '#003554' }}>
      <Container maxWidth="xl" >
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="a"
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "Roboto, Helvetica, Arial, sans-serif",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "#FFFACA", 
              textDecoration: "none",
            }}
          >
            🐾 Paws For Cause
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="menu"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              sx={{ color: "#FFFACA" }}
            >
            <MenuIcon />
            </IconButton>
            {/* LEFT HAND MENU */}
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{ display: { xs: "block", md: "none" } }}
            >
              <MenuItem component={Link} to="/animals" onClick={handleCloseNavMenu}>
                <Typography textAlign="center">Home</Typography>
              </MenuItem>
              <MenuItem component={Link} to="/animals" onClick={handleCloseNavMenu}>
                <Typography textAlign="center">Animals</Typography>
              </MenuItem>
              <MenuItem component={Link} to="/messages" onClick={handleCloseNavMenu}>
                <Typography textAlign="center">Messages</Typography>
              </MenuItem>
              </Menu>


              {/* USER MENU? */}
              {/* {!loggedIn && (
                <Menu>
                  <MenuItem component={Link} to="/sign-up" onClick={handleCloseNavMenu}>
                    <Typography textAlign="center">Signup</Typography>
                  </MenuItem>
                  <MenuItem component={Link} to="/login" onClick={handleCloseNavMenu}>
                    <Typography textAlign="center">Login</Typography>
                  </MenuItem>
                </Menu>
              )}
              {loggedIn && (
                <Menu>
                  <MenuItem component={Link} to="/create-advert" onClick={handleCloseNavMenu}>
                      <Typography textAlign="center">Create Advert</Typography>
                    </MenuItem> */}
                    {/* <MenuItem component={Link} to="/my-animals" onClick={handleCloseNavMenu}>
                      <Typography textAlign="center">My Animals</Typography>
                    </MenuItem> */}
                    {/* <MenuItem onClick={handleLogoutClick}>
                      <Typography textAlign="center">Logout</Typography>
                    </MenuItem>
                </Menu>

              )} */}
            
          </Box>

          <Typography
            variant="h5"
            noWrap
            component="a"
            sx={{
              mr: 2,
              display: { xs: "flex", md: "none" },
              flexGrow: 1,
              fontFamily: "Roboto, Helvetica, Arial, sans-serif",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "#FFFACA",
              textDecoration: "none",
            }}
          >
            🐾 Paws For Cause
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
            <Button
              component={Link}
              to="/animals"
              data-testid="_animals"
              sx={{
                fontFamily: 'Arial, sans-serif',
                color: '#FFFACA',             
                '&:hover': {
                  backgroundColor: '#557B71',
                },
              }}
            >
              Home
            </Button>
            <Button
              component={Link}
              to="/animals"
              data-testid="_animals"
              sx={{
                fontFamily: 'Arial, sans-serif',
                backgroundColor: '#003554', 
                color: '#FFFACA',             
                '&:hover': {
                  backgroundColor: '#557B71', 
                },
              }}
            >
              Animals
            </Button>
            <Button
              component={Link}
              to="/messages"
              data-testid="_messages"
              sx={{
                fontFamily: 'Arial, sans-serif',
                backgroundColor: '#003554', 
                color: '#FFFACA',             
                '&:hover': {
                  backgroundColor: '#557B71', 
                },
              }}
            >
              Messages
            </Button>
          </Box>

          {!loggedIn && (
            <Box sx={{ marginLeft: "auto" }}>
              <Button
                component={Link}
                to="/sign-up"
                data-testid="_signup"
                sx={{
                  fontFamily: 'Arial, sans-serif',  
                  color: '#FFFACA',             
                  '&:hover': {
                    backgroundColor: '#557B71',
                    gap: "1em", 
                  },
                }}
              >
                Signup
              </Button>
              <Button
                component={Link}
                to="/login"
                data-testid="_login"
                sx={{
                  fontFamily: 'Arial, sans-serif',  
                  color: '#FFFACA',             
                  '&:hover': {
                    backgroundColor: '#557B71',
                    gap: "1em",  
                  },
                }}
              >
                Login
              </Button>
            </Box>
          )}

          {loggedIn && (
            <Box sx={{ flexGrow: 0 }}>
              <Tooltip title="My Account">
                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                  <Avatar alt="" src="/public/avatar_cat.png" />
                </IconButton>
              </Tooltip>
              <Menu
                sx={{ mt: "45px" }}
                id="account-menu-appbar"
                anchorEl={anchorElUser}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right",
                }}
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}
              >
                <MenuItem
                  onClick={handleCloseUserMenu}
                  component={Link}
                  to="/create-advert"
                  data-testid="_create-advert"
                  sx={{ color: "#003554" }} 
                >
                  <Typography textAlign="center">Create Advert</Typography>
                </MenuItem>
                {/* <MenuItem
                  onClick={handleCloseUserMenu}
                  component={Link}
                  to="/my-animals"
                  data-testid="_my-animals"
                  sx={{ color: "#003554" }}  
                >
                  <Typography textAlign="center">My Animals</Typography>
                </MenuItem> */}
                <MenuItem
                  onClick={handleLogoutClick}
                  component={Link}
                  to="/login"
                  data-testid="_logout"
                  sx={{ color: "#003554" }}  
                >
                  <Typography textAlign="center">Logout</Typography>
                </MenuItem>
              </Menu>
            </Box>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;
