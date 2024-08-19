import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import { useState, useEffect, createContext } from "react";
import "./App.css";
import { LoginPage } from "./Pages/LoginPage/LoginPage";
import Navbar from "./components/Navbar/Navbar";
import SignUpPage from "./Pages/SignUpPage/SignUpPage";
import CreateAdvertPage from "./pages/CreateAdvertPage/CreateAdvertPage";
import AllAnimals from "./Pages/Animals/animals";
import AllAnimals from "./Pages/Animals/Animals";
import AnimalAdvertPage from "./Pages/AnimalAdvertPage/AnimalAdvertPage";

// alternative to state for passing down to child components
// https://react.dev/reference/react/useContext#usecontext
// Create a context to pass down authStatus
const Context = createContext();

// Wrapper component that includes the Navbar and renders the nested routes
const NavbarWrapper = () => (
  <>
    <Navbar />
    <Outlet />
  </>
);

// Define your routes
const router = createBrowserRouter([
  {
    path: "/", // Base path for the application
    element: <NavbarWrapper />, // Navbar on all pages
    children: [
      {
        path: "login", 
        element: <LoginPage />,
      },
      {
        path: "sign-up", 
        element: <SignUpPage />,
      },
      {
        path: "animals", 
        element: <AllAnimals />,
      },
      {
        path: "create-advert", // Path to the create advert page
        element: <CreateAdvertPage />,
      }
    ],
  },

]);

const App = () => {
  const [authStatus, setAuthStatus] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setAuthStatus(!!token);
  }, []);

  return (
    <Context.Provider value={{ authStatus, setAuthStatus }}>
      <RouterProvider router={router} />
    </Context.Provider>
  );
};

export default App;
