import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";
import { useState, useEffect, createContext } from "react";
import "./App.css";
import { LoginPage } from "./Pages/LoginPage/LoginPage";
import Navbar from "./components/Navbar/Navbar";
import SignUpPage from "./Pages/SignUpPage/SignUpPage";
import CreateAdvertPage from "./Pages/CreateAdvertPage/CreateAdvertPage";
import AllAnimals from "./Pages/Animals/AllAnimals";
import AnimalAdvertPage from "./Pages/AnimalAdvertPage/AnimalAdvertPage";
import MessagesPage from "./Pages/Messages/MessagesPage"
import VerifyPage from "./Pages/Verify/VerifyPage"
import { AuthProvider } from "./components/Context/AuthProvider";
import '@mui/material/styles/styled'; // patching an issue with vite chunking https://github.com/vitejs/vite/issues/12423



// alternative to state for passing down to child components
// https://react.dev/reference/react/useContext#usecontext
// Create a context to pass down authStatus
// const Context = createContext();

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
        path: "/",
        element: <AllAnimals />,
      },
      {
        path: "login",
        element: <LoginPage />,
      },
      {
        path: "sign-up",
        element: <SignUpPage />,
      },
      {
        path: "verify",
        element: <VerifyPage />,
      },
      {
        path: "animals",
        element: <AllAnimals />,
      },
      {
        path: "animals/:id",
        element: <AnimalAdvertPage />,
      },

      {
        path: "create-advert",
        element: <CreateAdvertPage />,
      },
      {
        path: "messages",
        element: <MessagesPage />,
      },
    ],
  },
]);

const App = () => {

  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
};

export default App;
