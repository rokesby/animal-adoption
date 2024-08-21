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
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

function ResponsiveAppBar() {
  const [anchorElNav, setAnchorElNav] = useState(null);
  const [anchorElUser, setAnchorElUser] = useState(null);

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

  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [buttonText, setButtonText] = useState();

  useEffect(() => {
    if (token) {
      setButtonText("Logout");
    } else {
      setButtonText("Login");
    }
  }, [token]);

  const handleLogoutClick = () => {
    if (token) {
      localStorage.clear("token");
      setToken(null);
    } else {
      navigate("/login");
    }
  };

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "inherit",
              textDecoration: "none",
            }}
          >
            🐾 For a Cause
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
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
              sx={{
                display: { xs: "block", md: "none" },
              }}
            ></Menu>
          </Box>
          <Typography
            variant="h5"
            noWrap
            component="a"
            href="#app-bar-with-responsive-menu"
            sx={{
              mr: 2,
              display: { xs: "flex", md: "none" },
              flexGrow: 1,
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "inherit",
              textDecoration: "none",
            }}
          >
            🐾 For a Cause
          </Typography>
        <Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
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
              to="/animals"
              data-testid="_animals"
              color="inherit"
            >
              Animals
            </Button>
          </Box>
          
          
          <Box sx={{ marginLeft: "auto" }}>
            <Button
              component={Link}
              to="/sign-up"
              data-testid="_signup"
              color="inherit"
            >
              Signup
            </Button>
          </Box>
          <Box sx={{ marginLeft: "auto" }}>
            <Button
              component={Link}
              to="/login"
              data-testid="_login"
              color="inherit"
            >
              Login
            </Button>
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="My Account">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt="" src="/static/images/avatar/2.jpg" />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: "45px" }}
              id="menu-appbar"
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
              {" "}
              <MenuItem
                onClick={handleCloseUserMenu}
                component={Link}
                to="/my-profile"
                data-testid="_my-profile"
                color="inherit"
              >
                <Typography textAlign="center">My Profile</Typography>
              </MenuItem>
              <MenuItem
                onClick={handleCloseUserMenu}
                component={Link}
                to="/create-advert"
                data-testid="_create-advert"
                color="inherit"
              >
                <Typography textAlign="center">Create Advert</Typography>
              </MenuItem>
              <MenuItem
                onClick={handleCloseUserMenu}
                component={Link}
                to="/my-animals"
                data-testid="_my-animals"
                color="inherit"
              >
                <Typography textAlign="center">My Animals</Typography>
              </MenuItem>
              <MenuItem
                onClick={handleLogoutClick}
                component={Link}
                to="/login"
                data-testid="_logout"
                color="inherit"
              >
                <Typography textAlign="center">Logout</Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
export default ResponsiveAppBar;

// import AppBar from "@mui/material/AppBar";
// import Box from "@mui/material/Box";
// import Toolbar from "@mui/material/Toolbar";
// import Typography from "@mui/material/Typography";
// import Button from "@mui/material/Button";
// import { Link } from "react-router-dom";

// //import { useContext } from "react";
// //import Context from "../Context/Context";

// const Navbar = () => {
//   //const { authStatus, setAuthStatus } = useContext(Context);

//   return (
//     <Box sx={{ flexGrow: 1 }}>
//       <AppBar
//         data-testid="_nav"
//         position="static"
//         color="transparent"
//         sx={{
//           width: "100vw",
//         }}
//       >
//         <Toolbar>
//         <Typography component={Link} to="/" color="inherit" variant="h6">
//   🐾 For a Cause
// </Typography>

//           <Box sx={{ marginLeft: "auto" }}>
//             <Button
//               component={Link}
//               to="/animals"
//               data-testid="_animals"
//               color="inherit"
//             >
//               Home
//             </Button>
//
//             <Button
//               component={Link}
//               to="/sign-up"
//               data-testid="_signup"
//               color="inherit"
//             >
//               Signup
//             </Button>
//           </Box>

//           {/* <Box sx={{ marginLeft: "auto" }}>
//             <Button
//               component={Link}
//               to="/create-advert"
//               data-testid="_create-advert"
//               color="inherit"
//             >
//               Create Advert
//             </Button>
//           </Box> */}
//         </Toolbar>
//       </AppBar>
//     </Box>
//   );
// };

// export default Navbar;
