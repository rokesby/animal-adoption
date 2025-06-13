import {useContext, useEffect, useState} from "react";
import { useNavigate } from "react-router-dom";
import Box from '@mui/material/Box';
import { Button, Card, CardContent, CardHeader } from "@mui/material";
import { AuthContext, useAuth } from "../Context/AuthContext";



export const LoginLogout = () => {

  const navigate = useNavigate();
  const {token, setToken} = useAuth()
  const [buttonText, setButtonText] = useState()
  
  
  useEffect(() => {
    if (token) {
      setButtonText("Logout")
    } else {
      setButtonText("Login")
    }
  }, [token]);

  const handleClick = () => {
    if (token) {
      setToken(null)
    } else {
      navigate("/login")
    }
  }

    return (
        <>
        <Button variant="outlined" onClick={handleClick}>{buttonText}</Button>
        </>
      );
}

export default LoginLogout;