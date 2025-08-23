import React, { useState, useEffect } from 'react'
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import ListSubheader from '@mui/material/ListSubheader';
import { Button, ListItemButton, ListItemSecondaryAction } from '@mui/material';
import { formatConversationTime } from '../../utils/helper';


export default function ConversationList({authFetch, conversations, conversationId, handleConversation}) {
    
    return (
        <Box sx={{
            borderRadius: 7,
            width: '100%',
            bgcolor: 'white',
            }}>
        <ListSubheader
            sx={{
                borderRadius: 'inherit'
            }}
        
        >{`All Messages`}</ListSubheader>
        {conversations.length > 0 ? (
            <List>
            {conversations.map((conversationAndMessage) => {
                const {conversation, latest_message} = conversationAndMessage;
                const contentLength = latest_message.content.length
                const messageContent = contentLength >= 100 ? `${latest_message.content.substring(0,100)}...` : latest_message.content
                return (
                    <ListItem key={conversation.id} 
                        alignItems="flex-start" 
                        disablePadding
                        >
                        <ListItemButton
                        id={conversation.id}
                        onClick={(e) => handleConversation(e.currentTarget.id)}
                        selected={conversationId == conversation.id}
                        sx={{
                            '&.Mui-selected': {
                                borderRadius: 7,
                                marginBottom: -1,
                                '&:hover': {
                                backgroundColor: 'rgba(71, 145, 220, 0.18)',
                            }
                            },
                            // '&.Mui-focusVisible': {
                            //     backgroundColor: 'rgba(71, 145, 220, 0.18)',
                            //     color: 'green',
                            //     borderRadius: 7
                            // }
                        }}
                        >
                        <ListItemAvatar>
                            <Avatar alt={latest_message.sender_name} src="public/avatar_cat.png" />
                        </ListItemAvatar>
                        <ListItemText
                        primary={latest_message.sender_name}
                        primaryTypographyProps={{
                            sx: { fontWeight: 'bold',  color: 'midnightblue', }
                        }}
                        secondary={
                            <>
                            <Typography
                                component='body'
                                variant="body2"
                                sx={{ color: 'black',
                                }}
                            >
                                {messageContent}
                            </Typography>
                            <Typography
                                component="span"
                                variant="body2"
                                sx={{ color: 'GrayText', display: 'inline' }}
                            >
                                {formatConversationTime(conversation.updated_at)}
                            </Typography>
                            </>
                        }
                        
                        />

                        </ListItemButton>
                        {/* <ListItemSecondaryAction>
                            <Button>Delete</Button>
                        </ListItemSecondaryAction> */}
                    </ListItem>
                    
                )
            })}
            </List>
        ) : (
            <Typography> No Messages</Typography>
        )}
        </Box>
    )
}
