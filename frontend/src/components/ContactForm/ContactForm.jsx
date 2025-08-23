import { Box, Button, Stack, TextField } from "@mui/material";
import { useState } from "react";
import { useAuth } from "../Context/AuthProvider";
import { postNewMessage } from "../../services/users";

function ContactForm({ data }) {
    const { id } = data;
    const {authFetch} = useAuth();
    const emptyForm = { content: "" };
    const [errorMsg, setErrorMsg] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    const [formData, setFormData] = useState(emptyForm);
    const maxMessageLength = 300;

    const validateForm = () => {
        if (!formData.content.trim()) {
        throw new Error("Message is required");
        }
        if (formData.content.length > maxMessageLength) {
            throw new Error("Message too long");
        }
        return null;
    };

    const handleFormData = (field, value) => {
        setFormData({ ...formData, [field]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (submitting == false) {
            setSubmitting(true);
            console.log('submitting')
            // validate
            try {
                
                validateForm();
                const contactFormData = formData;
                contactFormData['animal_id'] = id
                // make backend request
                response = await postNewMessage(authFetch, contactFormData)
            } catch (error) {
                console.log(error)
            } finally {
                console.log('setting submitting false')
                setSubmitting(false);
                setFormData(emptyForm)
            }
        } else {
            console.log('already submitting')
            return null
        }
        
    
    };

    return (
        <Box
        // component="form"
        // autoComplete='on'
        // onSubmit={handleSubmit}
        >
        <Stack
            component="form"
            id="contact-form"
            autoComplete="on"
            onSubmit={handleSubmit}
            spacing={2}
            sx={{
            justifyContent: "start",
            alignItems: {
                xs: "start",
                md: "center",
            },
            }}
        >
            <TextField
            required
            multiline
            rows={5}
            id="content"
            label="Message"
            error={formData.content.length > maxMessageLength ? true : false}
            helperText={
                formData.content.length > maxMessageLength
                ? `The message must be less than ${maxMessageLength} characters`
                : false
            }
            fullWidth
            placeholder="Ask us a question"
            onChange={(e) => handleFormData("content", e.target.value)}
            type="text"
            value={formData.content}
            />
            <Button
            data-testid="submit-button"
            type="submit"
            variant="contained"
            id="submit"
            label="submit"
            form="contact-form"
            >
            Submit
            </Button>
        </Stack>
        </Box>
    );
    }

    export default ContactForm;
