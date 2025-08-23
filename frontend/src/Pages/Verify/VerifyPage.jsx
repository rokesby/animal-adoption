import { useState, useContext } from "react";
import Box from '@mui/material/Box';
import Alert from "@mui/material/Alert";
import AlertTitle from '@mui/material/AlertTitle';
import TextField from '@mui/material/TextField';
import { Button, Grid, Typography } from "@mui/material";
import Paper from '@mui/material/Paper';
import { redirect, useNavigate, useSearchParams } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import { verifyService } from "../../services/authService"

export const VerifyPage = () => {
    const [searchParams] = useSearchParams();
    const [submitting, setSubmitting] = useState(false)
    const [errorMessage, setErrorMessage] = useState("")
    const [success, setSuccess] = useState(false)
    const [invalidPin, setInvalidPin] = useState(false)
    const verificationToken = searchParams.get('token');

    const [pinEntryForm, setPinEntryForm] = useState({
        0: "",
        1: "",
        2: "",
        3: "",
        4: "",
        5: ""
    })

    const allowedDigits = ['0','1','2','3','4','5','6','7','8','9']
    
    const navigate = useNavigate();

    const handlePinEntry = (field, value) => {
        setErrorMessage("")
        setPinEntryForm({...pinEntryForm, [field]: value})
    }


    const joinDigits = () => {
        let digits = ""
        for( let digit in pinEntryForm) {
            digits += pinEntryForm[digit]
        }
        return digits
    }

    pinEntryForm.key

    const handlePinSubmit = async (e) => {
        e.preventDefault()
        console.log("submitting")
        console.log(pinEntryForm)
        setSubmitting(true)
        const enteredPin = joinDigits()
        
        const formData = {
            pin: enteredPin,
            token: verificationToken
        }

        try {
            const response = await verifyService(formData)
            
            console.log('successful pin', response)
            setInvalidPin(false)
            console.log(response)
            setSuccess(true)
        } catch (error) {
            setInvalidPin(true)
            setErrorMessage(error.message)
            console.log('error:', error.message)

        }
        setSubmitting(false)
    }

    const pinLength = 6
    return (
        <Grid container columns={6} sx={{
            height: '100vh',
            alignItems: "center",
            border: 'solid',
            borderColor: 'green',
            borderWidth: 2,
            justifyContent: "center"
        }}>
        <Grid
        size={2}
        sx={{ 
        height: '400px'
        }}
        >
        
        <Paper
        component="form"
        inputMode="numeric"
        id="pin-form"
        
        autoComplete="false"
        onSubmit={handlePinSubmit}
        sx={{
        padding: 2,
        height: '100%'
        }}>
        <Typography
        fontWeight={"bold"}
        color={'primary.main'}
        paddingTop={1}
        paddingBottom={1}
        variant="h6"
        >
        Enter verification code:
        </Typography>
        <Grid 
        key={"pin-input-grid"}
        container 
        columns={6} 
        sx={{
            justifyContent: 'space-evenly',
        }} >
            {Array.from({length: pinLength}, (_, index) => 
            <Grid>
            <TextField
            key={index}
            required
            id={`pin-input-${index}`}
            placeholder={`${index + 1}`}
            value={pinEntryForm[index]}
            inputProps={{
                    style: {textAlign: 'center'},
                    maxLength: 1,
            }}
            sx={{
                maxWidth: '50px',
            padding: '5px',
            textAlign: 'center',
            '& .MuiOutlinedInput-root': {
            '& fieldset': {
                borderColor: pinEntryForm[index] ? '#339c33ff' : '#608cb3f7',
                // borderWidth: pinEntryForm[index] ? 3 : 2
                borderWidth: 2
                
            },
            '&:hover fieldset': {
                borderColor: pinEntryForm[index] ? 'rgba(95, 135, 95, 0.93)' : 'rgba(65, 97, 157, 0.95)', // Darker on hover
            },
            '&.Mui-focused fieldset': {
                borderColor: 'primary.main', // Keep normal focus color
            },
        }
            }}
            onChange={(e) => handlePinEntry(index, e.target.value)}
            
            />
            </Grid>
        )}
        </Grid>
        <Button
        type="submit"
        form="pin-form"
        id="submit-pin-button"
        variant="contained"
        size="large"
        sx={{
            marginTop: 2
        }}
        >
            Submit
        </Button>
        {errorMessage && (
            <Alert 
            severity="error"
            sx={{
                marginTop: "1em"
            }}
            >
                {errorMessage}
            </Alert>
        )}
        {success && (
            <Alert 
            severity="success"
            action={
            <Button 
            color="inherit" 
            size="small"
            onClick={() => navigate('/login')}
            >
            Login
            </Button>
        }
            sx={{
                marginTop: "1em"
            }}
            >
                Successfully validated. Please log in
            </Alert>
        )}
        
        </Paper>
        </Grid>
        </Grid>
       
    )
}

export default VerifyPage