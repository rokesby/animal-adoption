import {useState} from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { replyToConversationMessages } from '../../services/messaging';
import { useAuth } from "../Context/AuthProvider";



export default function ConversationReply({conversation, setRefreshKey, handleConversationRefresh}) {
    const {animal_id, id} = conversation;
    const [submitting, setSubmitting] = useState(false);
    const emptyFormData = {
        content: "",
        animal_id: animal_id,
    }

    const [formData, setFormData] = useState(emptyFormData);
    const maxMessageLength = 300;
    const {authFetch} = useAuth();

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


    const handleFormSubmit = async (e) => {
        e.preventDefault();
        if (submitting == false) {
            setSubmitting(true);
            console.log('submitting')
            // validate
            try {
                validateForm();
                const messageData = formData;
                const response = await replyToConversationMessages(authFetch, messageData, id)
                console.log('response', response)
                setRefreshKey(prev => prev + 1)
                handleConversationRefresh(response)
                return response
            } catch (error) {
                console.log(error)
            } finally {
                console.log('setting submitting false')
                setSubmitting(false);
                setFormData(emptyFormData);
            }
        } else {
            console.log('already submitting')
            return null
        }
        
    };

  return (
    <Box
      component="form"
      id='message-form'
    //   sx={{ bgcolor: 'background.paper'}}
    //   noValidate
      autoComplete="off"
      onSubmit={handleFormSubmit}
      sx={{
        // justifyContent: 'flex-start'
        height: 'min-content',
        
        }}
    >
        <TextField
        sx={{
            width: '100%', 
            // justifySelf: 'centre'
        }}
        id="reply-text-field"
        label="Reply"
        placeholder="Reply to user"
        multiline
        maxRows={4}
        name="reply"
        value={formData.content}
        onChange={(e) => handleFormData("content", e.target.value)}
        error={formData.content.length > maxMessageLength ? true : false}
            helperText={
                formData.content.length > maxMessageLength
                ? `The message must be less than ${maxMessageLength} characters`
                : false
            }
        />
        <Button
        type='submit'
        form='message-form'
        id='submit'
        label='submit'
        >
        Send
        </Button>
    </Box>
  )
}
