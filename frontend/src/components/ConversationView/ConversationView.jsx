// import * from 'react';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import ConversationReply from '../ConversationReply/ConversationReply';
import { Stack, Typography } from '@mui/material';
import { useAuth } from "../Context/AuthProvider";
import { formatConversationTime } from '../../utils/helper';

export default function ConversationView({conversationMessages, handleConversationRefresh, setRefreshKey}) {
    const {conversation, messages} = conversationMessages
    console.log('conversation: ', conversation, 'messages: ', messages, 'length', messages.length)
    const {userData} = useAuth()

    const isCurrentUser = (message) => {
        return message.sender_id == userData.user_id
    }
    
    return (
    <Box
        sx={{
            width: '100%', 
            display: 'flex',
            flexDirection: 'column', 
            rowGap: 2,
            borderRadius: 7,
            
            }}
        >
        {/* Conversation messages */}
            <Stack 
            direction="column"
            spacing={2}
            sx={{
                justifyContent: "flex-start",
                alignItems: "centre",
                overflow: 'auto',
                flexGrow: 1,
                borderRadius: 'inherit',
                bgcolor: 'background.paper', 
                maxHeight: {
                    xs: '60vh'
                    },
            }}>
                {messages.map(
                    message => (
                        <Box key={message.id} id={message.id}
                        >
                        {/* date */}
                            <Typography variant='body2' color={'grey'}>
                                {formatConversationTime(message.created_at)}
                            </Typography>
                            {/* avatar, name, message details */}
                            <Box
                            sx={{
                            display: 'flex',
                            color: 'black',
                            justifyContent: 'flex-start',
                            alignItems: 'flex-start',
                            flexDirection: isCurrentUser(message) ? 'row-reverse' : 'row'
                            }} 
                            >
                            <Avatar alt={message.sender_name} src={
                                isCurrentUser(message) ? "/public/avatar_dog.png" : "/public/avatar_cat.png"} 
                                sx={{
                                padding: 2
                                }}/>
                            <Box sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                textAlign: isCurrentUser(message) ? 'right' : 'left',
                                width: '50%',
                                paddingTop: 1,
                                paddingBottom: 2
                                
                            }}>
                                <Typography 
                                    variant='subtitle1'
                                    sx={{fontWeight: 'bold',
                                    color: isCurrentUser(message) ? 'blueviolet' : 'orange',
            
                                    }}
                                >{message.sender_name}
                                </Typography>
                                <Typography variant='body1'
                                >{message.content}</Typography>
                            </Box>
                            </Box>
                        </Box>
                    )
                )}
            </Stack>
        {/* conversation reply box */}
        <Box sx={{
            flexShrink: 1,
            border: 'solid',
            borderWidth: 2,
            borderColor: 'lightsteelblue',
            alignContent: 'flex-start',
            padding: 2,
            bgcolor: 'background.paper',
            // backgroundColor: 'transparent',
            borderRadius: 'inherit',
            height: 'min-content'
            }}>
            <ConversationReply conversation={conversation} setRefreshKey={setRefreshKey} handleConversationRefresh={handleConversationRefresh}/> 
        </Box>
    </Box>
    
    )
}
