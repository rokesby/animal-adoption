import { useState, useEffect } from "react";
import Box from '@mui/material/Box';
import { Typography } from "@mui/material";
import ConversationList from "../../components/ConversationList/ConversationList";
import { useAuth } from "../../components/Context/AuthProvider";
import {getConversations, getConversationsMessages} from "../../services/messaging"
import ConversationView from "../../components/ConversationView/ConversationView";
import { formatConversationTime } from "../../utils/helper";


export const MessagesPage = () => {
const {authFetch} = useAuth();
const [conversationId, setConversationId] = useState(null)
const [conversationMessages, setConversationMessages] = useState({
    conversation: "",
    messages: []
})
const [conversations, setConversations] = useState([])
const [refreshKey, setRefreshKey] = useState(0)

const handleConversation = async (id) => {
    console.log("Conversation set as ", id)
    setConversationId(id)
    try {
        console.log('about to fetch')
        const messageData = await getConversationsMessages(authFetch, id)
        console.log(messageData)
        setConversationMessages(messageData)
    }
    catch (error){
        console.log(`couldn't fetch messages`, error)
    }
}

const handleConversationRefresh = (message) => {
    setConversationMessages(prevState => ({
        ...prevState,
        messages: [...prevState.messages, message]}))
}

useEffect(() => {
    const fetchConversationData = async () => {
    const conversationData = await getConversations(authFetch);
    setConversations(conversationData)
    formatConversationTime()
    }
    fetchConversationData();
    return () => {
    }
}, [refreshKey])

  return (
        <Box sx={{
            display: 'flex',
            height: '95vh',
            columnGap: 1,
            marginTop: 1,
            marginLeft: 1,
            marginRight: 1,
            flexDirection: {
                xs: 'column',
                sm: 'row'
            },
            justifyContent: {
                md: 'space-between'
                }
            }}
            
        >
            <Box 
            key={1} 
            sx={{ 
                flex: 3,
                minWidth: 360,
                maxWidth: 700
            }}
            >
                <ConversationList authFetch={authFetch} conversations={conversations} handleConversation={handleConversation} conversationId={conversationId}/>
            </Box>
            {conversationMessages.messages.length > 0 && (
                <Box 
                key={2} 
                sx={{
                    flexGrow: 2,
                    display: 'flex',
                    marginTop: {
                        xs: 2,
                        sm: 0
                    },
                    minWidth: 300,
                    maxWidth: 1000
                }}>
                    <ConversationView conversationMessages={conversationMessages} handleConversationRefresh={handleConversationRefresh} refreshKey={refreshKey} setRefreshKey={setRefreshKey}/>
                </Box>
            )}
            
        </Box>
  );
};

export default MessagesPage;