from datetime import datetime
import uuid
import pytest
from sqlalchemy import UUID

from lib.models import Conversation, Message
from routes.conversation_routes import conversation_repo, message_repo

def test_get_shelter_conversations(client, mocker, auth_user):
    """
    GIVEN a valid shelter user
    GET /shelter/conversations 
    SHOULD return all conversations
    for the given users shelter id
    """
    
    auth_user()
    shelter_id = 1
    conversation_id = uuid.uuid4()
    
    mock_conversations = []
    
    for i in range(3):
        mock_conversation = mocker.Mock(spec=Conversation)
        mock_conversation.shelter_id = shelter_id
        mock_conversation.to_dict.return_value = {
        "id": conversation_id,
        "shelter_id": 1,
        "animal_id": "5235c2d2-266a-4851-a48a-777ce595065e",
        "created_at": "2025-07-28T14:33:39",
        "updated_at": "2025-07-28T14:33:39"
        }
        mock_conversations.append(mock_conversation)
    
    mock_get_conversations = mocker.patch.object(
    conversation_repo, 'get_shelter_conversations', 
    return_value=mock_conversations
    )
    
    response = client.get('/shelter/conversations',  headers={'Authorization': f'Bearer valid-token'})
    response_data = response.get_json()
    
   
    assert response.status_code == 200
    assert len(response_data) == len(mock_conversations)
    assert isinstance(response_data, list)
    mock_get_conversations.assert_called_once_with(1)
    
def test_invalid_users_cant_get_shelter_conversations(client, mocker, auth_non_shelter_user):
    """
    GIVEN an invalid user
    GET /shelter/conversations 
    SHOULD return a 403 error
    """
    
    auth_non_shelter_user()
    shelter_id = 1
    conversation_id = uuid.uuid4()
    
    mock_conversations = []
    
    for i in range(3):
        mock_conversation = mocker.Mock(spec=Conversation)
        mock_conversation.shelter_id = shelter_id
        mock_conversation.to_dict.return_value = {
        "id": conversation_id,
        "shelter_id": 2,
        "animal_id": "5235c2d2-266a-4851-a48a-777ce595065e",
        "created_at": "2025-07-28T14:33:39",
        "updated_at": "2025-07-28T14:33:39"
        }
        mock_conversations.append(mock_conversation)
    
    mock_get_conversations = mocker.patch.object(
    conversation_repo, 'get_shelter_conversations', 
    return_value=mock_conversations
    )
    
    response = client.get('/shelter/conversations',  headers={'Authorization': f'Bearer valid-token'})
    response_data = response.get_json()
    
   
    assert response.status_code == 403
    assert 'Access denied' in response_data['error']
    mock_get_conversations.assert_not_called()

def test_get_conversation_messages_by_id(client, mocker, auth_user):
    """
    GIVEN a valid user
    AND a valid conversation id
    GET /conversations/<id>/messages
    SHOULD return messages with the matching conversation id
    """
    
    auth_user()
    conversation_id = "ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28"
    message_id = str(uuid.uuid4())
    
    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.id = conversation_id
    mock_conversation.shelter_id = 1
    mock_conversation.to_dict.return_value = {
        "id": mock_conversation.id
    }
    
    mock_messages = []
    
    for i in range(2):
        mock_message =  mocker.Mock(spec=Message)
        mock_message.id = message_id
        mock_message.content = f'this is a test message {i}'
        mock_message.conversation_id = conversation_id
        mock_message.to_dict.return_value = {
            "id": message_id,
            "content": mock_message.content,
            "conversation_id": conversation_id
        }
        mock_messages.append(mock_message)
    
    mock_get_conversation_by_id = mocker.patch.object(
        conversation_repo, 'get_conversation_by_id', 
        return_value=mock_conversation
    )
    
    mock_get_conversation_messages = mocker.patch.object(
    conversation_repo, 'get_conversation_messages', 
    return_value=mock_messages
    )
    
    response = client.get(f'/conversations/{conversation_id}/messages', headers={'Authorization': f'Bearer valid-token'})
    
    print(f'response: {response}')
    # response_data = response.get_json()
    
    assert response.status_code == 200
    # assert len(response) == len(mock_messages)
    mock_get_conversation_messages.assert_called_once_with(conversation_id)


def test_get_conversation_errors_if_shelter_user_isnt_valid(auth_user, client, mocker):
    """
    IF a shelter user attempts to get another shelters conversations
    There should be an unauthorised response
    """
    
    auth_user(user_id=3, shelter_id=4)
    conversation_id = "ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28"
    
    mock_user = mocker.Mock()
    mock_user.id = 1

    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.shelter_id = 1
    mock_conversation.participants = [mock_user]
    mock_conversation.to_dict.return_value = {
        "id": conversation_id,
        "shelter_id": 1,
        "animal_id": "5235c2d2-266a-4851-a48a-777ce595065e",
        "created_at": "2025-07-28T14:33:39",
        "updated_at": "2025-07-28T14:33:39"
    }
    mock_message_1 = mocker.Mock(spec=Message)
    mock_message_1.content = 'This is a test message from public user 2 to shelter id 1 for test_animal_1'
    mock_message_1.conversation_id = conversation_id 
    
    mock_message_2 = mocker.Mock(spec=Message)
    mock_message_2.content = 'This is a test message reply'
    mock_message_2.conversation_id = conversation_id
    
    mock_messages =[mock_message_1, mock_message_2]
    
    mock_get_conversation_by_id = mocker.patch.object(
        conversation_repo, 'get_conversation_by_id', 
        return_value=mock_conversation
    )
    mock_get_conversation_messages = mocker.patch.object(
        conversation_repo, 'get_conversation_messages', 
        return_value=mock_messages
    )
    
    response = client.get(f'/conversations/{conversation_id}/messages', headers={'Authorization': f'Bearer valid-token'})
    
   
    mock_get_conversation_by_id.assert_called_once_with(conversation_id)
    assert response.status_code == 403
    assert response.get_json()['error'] == 'Access denied'
    mock_get_conversation_messages.assert_not_called()
    
def test_get_conversation_errors_if_user_isnt_valid(auth_non_shelter_user, client, mocker):
    """
    IF a user attempts to get another users conversations
    There should be an unauthorised response
    """
    
    auth_non_shelter_user(user_id=3)
    conversation_id = "ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28"
    
    mock_user = mocker.Mock()
    mock_user.id = 1

    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.shelter_id = 1
    mock_conversation.participants = [mock_user]
    mock_conversation.to_dict.return_value = {
    "id": conversation_id,
    "shelter_id": 1,
    "animal_id": "5235c2d2-266a-4851-a48a-777ce595065e",
    "created_at": "2025-07-28T14:33:39",
    "updated_at": "2025-07-28T14:33:39"
}
    mock_message_1 = mocker.Mock(spec=Message)
    mock_message_1.content = 'This is a test message from public user 2 to shelter id 1 for test_animal_1'
    mock_message_1.conversation_id = conversation_id 
    
    mock_message_2 = mocker.Mock(spec=Message)
    mock_message_2.content = 'This is a test message reply'
    mock_message_2.conversation_id = conversation_id
    
    mock_messages =[mock_message_1, mock_message_2]
    
    mock_get_conversation_by_id = mocker.patch.object(
        conversation_repo, 'get_conversation_by_id', 
        return_value=mock_conversation
    )
    mock_get_conversation_messages = mocker.patch.object(
        conversation_repo, 'get_conversation_messages', 
        return_value=mock_messages
    )
    
    response = client.get(f'/conversations/{conversation_id}/messages', headers={'Authorization': f'Bearer valid-token'})
    
   
    mock_get_conversation_by_id.assert_called_once_with(conversation_id)
    assert response.status_code == 403
    assert response.get_json()['error'] == 'Access denied'
    mock_get_conversation_messages.assert_not_called()

def test_get_conversations(auth_non_shelter_user, client, mocker):
    """
    GIVEN the user is valid
    GET /conversations
    SHOULD return all conversations
    WHERE the user is a participant
    """
    auth_non_shelter_user(user_id=3)
    
    conversation_id = str(uuid.uuid4())
    
    mock_user = mocker.Mock()
    mock_user.id = 3
    mock_user_2 = mocker.Mock()
    mock_user_2.id = 4
    mock_user_3 = mocker.Mock()
    mock_user_3.id = 5

    mock_conversations = []
    
    for i in range(5):
        mock_conversation = mocker.Mock(spec=Conversation)
        mock_conversation.participants = [mock_user, mock_user_2, mock_user_3]
        mock_conversation.to_dict.return_value = {
        "id": conversation_id,
        "shelter_id": 1,
        "animal_id": "5235c2d2-266a-4851-a48a-777ce595065e",
        "created_at": "2025-07-28T14:33:39",
        "updated_at": "2025-07-28T14:33:39"
        }
        mock_conversations.append(mock_conversation)
        
    mock_get_user_conversations = mocker.patch.object(
        conversation_repo, 'get_user_conversations',
        return_value = mock_conversations
    )
        
    response = client.get('/conversations', headers={'Authorization': f'Bearer valid-token'})
    response_json = response.get_json()

    
    assert response.status_code == 200
    assert len(response_json) == 5
    mock_get_user_conversations.assert_called_once_with(mock_user.id)
    
def test_post_conversation_reply(client, auth_non_shelter_user, mocker):
    """
    GIVEN a valid user
    AND a valid conversation id
    POST /conversations/<id>/messages
    SHOULD create a new message in the given conversation id
    """
    
    auth_non_shelter_user(user_id=1)
    mock_user_1 = mocker.Mock()
    mock_user_1.id = 1
    animal_id = 1
    shelter_id = 1
    
    mock_conversation_id = "ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28"
    
    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.id = mock_conversation_id
    mock_conversation.participants = [mock_user_1]
    
    mock_data = {
        "content": "Test message reply to /conversations/<id>/messages"
    }
    
    mock_message = mocker.Mock(spec=Message)
    mock_message.to_dict.return_value = {
        "conversation_id": mock_conversation_id,
        "content": mock_data['content'],
    }
    
    mock_get_conversation_by_id = mocker.patch.object(
        conversation_repo, 'get_conversation_by_id',
        return_value = mock_conversation
    )
    
    mock_reply_to_conversation = mocker.patch.object(
        message_repo, 'reply_to_conversation',
        return_value = mock_message
    )
    
    response = client.post(f'/conversations/{mock_conversation_id}/messages',json=mock_data, headers={'Authorization': f'Bearer valid-token'})
    
    mock_get_conversation_by_id.assert_called_once_with(mock_conversation_id)
    mock_reply_to_conversation.assert_called_once_with(mock_data, mock_user_1.id, mock_conversation_id)
    assert response.status_code == 201
    
def test_reply_to_conv_errors_if_conv_not_found(client, auth_non_shelter_user, mocker):
    """
    GIVEN a valid user
    AND an invalid conversation id
    POST /conversations/<id>/messages
    SHOULD return a 404 error
    """
    
    auth_non_shelter_user(user_id=1)
    mock_user_1 = mocker.Mock()
    mock_user_1.id = 1
    
    mock_conversation_id = "ce8ea8a3-3680-41c5-83d1-7bf59cdc5a29"
    
    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.id = mock_conversation_id
    mock_conversation.participants = [mock_user_1]
    
    mock_data = {
        "animal_id": 1,
        "shelter_id":1,
        "content": "Test mesage reply to /conversations/<id>/messages"
    }
    mock_data_updated = {
        "animal_id": 1,
        "shelter_id":1,
        "content": "Test mesage reply to /conversations/<id>/messages",
        "conversation_id": mock_conversation_id
    }
    
    mock_message = mocker.Mock(spec=Message)
    mock_message.to_dict.return_value = {
        "conversation_id": mock_conversation_id,
        "content": mock_data['content'],
    }
    
    mock_reply_to_conversation = mocker.patch.object(
        message_repo, 'reply_to_conversation',
        return_value = mock_message
    )
    
    mock_get_conversation_by_id = mocker.patch.object(
        conversation_repo, 'get_conversation_by_id',
        return_value = None
    )
    
    response = client.post(f'/conversations/{mock_conversation_id}/messages',json=mock_data, headers={'Authorization': f'Bearer valid-token'})
    
    response_json = response.get_json()
    print(response_json)
    mock_get_conversation_by_id.assert_called_once_with(mock_conversation_id)
    assert 'conversation not found' in response_json['error']
   

def test_unauthorised_user_cannot_reply_to_conversation(client, auth_non_shelter_user, mocker):
    """
    GIVEN the user is not part of the shelter
    AND is not a participant
    POST /conversations/<id>/messages
    SHOULD return a 403 error 
    """
    
    auth_non_shelter_user(user_id=2)
    
    mock_conversation_id = "ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28"
    
    mock_user_1 = mocker.Mock()
    mock_user_1.id = 1
    
    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.id = mock_conversation_id
    mock_conversation.participants = [mock_user_1]
    
    mock_data = {
        "animal_id": 1,
        "shelter_id":1,
        "content": "Test message reply to /conversations/<id>/messages for invalid user"
    }
    
    mock_message = mocker.Mock(spec=Message)
    mock_message.to_dict.return_value = {
        "conversation_id": mock_conversation_id,
        "content": mock_data['content'],
    }
    
    mock_get_conversation_by_id = mocker.patch.object(
        conversation_repo, 'get_conversation_by_id',
        return_value = mock_conversation
    )
    
    mock_reply_to_conversation = mocker.patch.object(
        message_repo, 'reply_to_conversation',
        return_value = mock_message
    )
    
    response = client.post(f'/conversations/{mock_conversation_id}/messages',json=mock_data, headers={'Authorization': f'Bearer valid-token'})
    
    response_json = response.get_json()
    assert response.status_code == 403
    mock_reply_to_conversation.assert_not_called()
    
@pytest.mark.skip("first implement remove participant in conversation repo")
def test_remove_conversation_participant(client, auth_non_shelter_user,mocker):
    """
    GIVEN a user
    PUT /conversations/<id>/participants/remove  
    SHOULD remove the user
    IF the user exists in the participants
    """
    auth_non_shelter_user(user_id=1)
    
    mock_user_1 = mocker.Mock()
    mock_user_1.id = 1
    mock_user_2 = mocker.Mock()
    mock_user_2.id = 2
    mock_user_3 = mocker.Mock()
    mock_user_3.id = 3
    
    mock_conversation_id = "ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28"
    
    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.id = mock_conversation_id
    mock_conversation.participants = [mock_user_1, mock_user_2, mock_user_3]
    mock_conversation.to_dict.return_value = {
        "id": mock_conversation_id,
    }
    
    mock_remove_participant = mocker.patch.object(
        conversation_repo, 'remove_participant',
        return_value = mock_conversation
    )
    
    response = client.post(f'/conversations/{mock_conversation_id}/participants/remove', headers={'Authorization': f'Bearer valid-token'})
    
    assert response.status_code == 202
    mock_remove_participant.assert_called_once_with(mock_user_1.id)
    assert mock_user_1 not in mock_conversation.participants
