import uuid
import pytest
from lib.models import Conversation, Message
from routes.conversation_routes import conversation_repo, message_repo

def test_post_new_message(client, mocker, auth_non_shelter_user):
    """
    GIVEN a user is valid, 
    AND a conversation WITH user AND animal doesn't exist
    POST /messages,
    SHOULD create a new message
    AND conversation
    """
    
    auth_non_shelter_user(user_id=1)
    animal_id=1
    
    mock_user = mocker.Mock()
    mock_user.id = 1
    
    mock_conversation_id = uuid.uuid4()
    
    mock_data = {
        "animal_id": animal_id,
        "content": 'This is a test message'
    }
    
    mock_new_message = mocker.Mock(spec=Message)
    mock_new_message.conversation_id = mock_conversation_id
    mock_new_message.content = 'This is a test message'
    mock_new_message.to_dict.return_value = {
        "conversation_id": mock_conversation_id,
        "content": mock_new_message.content
    }
    
    mock_get_conversation_by_animal_and_user = mocker.patch.object(
        conversation_repo, 'get_conversation_by_animal_and_user',
        return_value=None
    )
    
    mock_create_new_message_with_conversation = mocker.patch.object(
        message_repo, 'create_new_message_with_conversation',
        return_value=mock_new_message
    )
  
    response = client.post('/messages', json=mock_data, headers={'Authorization': f'Bearer valid-token'})
    
    mock_get_conversation_by_animal_and_user.assert_called_once_with(mock_user.id, animal_id)
    mock_create_new_message_with_conversation.assert_called_once_with(mock_data, mock_user.id, animal_id)

    assert response.status_code == 201
    
def test_reply_to_conversation_called_for_existing_conversation(auth_non_shelter_user, mocker, client):
    """
    GIVEN a user is valid, 
    AND a conversation WITH user AND animal already exists
    POST /messages,
    SHOULD create a new message in the existing conversation
    """
    
    auth_non_shelter_user(user_id=1)
    animal_id=1
    
    mock_user = mocker.Mock()
    mock_user.id = 1
    mock_user_2 = mocker.Mock()
    mock_user_2.id = 2
    
    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.id = str(uuid.uuid4())
    mock_conversation.participants = [mock_user, mock_user_2]
    mock_conversation.animal_id = 1
    
    mock_data = {
        "animal_id": animal_id,
        "content": 'This should be a reply',
    }
    
    mock_new_message = mocker.Mock(spec=Message)
    mock_new_message.conversation_id = mock_conversation.id
    mock_new_message.content = 'This is a test message'
    mock_new_message.to_dict.return_value = {
        "conversation_id": mock_conversation.id,
        "content": mock_new_message.content,
    }
    
    mock_get_conversation_by_animal_and_user = mocker.patch.object(
        conversation_repo, 'get_conversation_by_animal_and_user',
        return_value=mock_conversation
    )
    
    mock_reply_to_conversation = mocker.patch.object(
        message_repo, 'reply_to_conversation',
        return_value=mock_new_message
    )
    
    response = client.post('/messages', json=mock_data, headers={'Authorization': f'Bearer valid-token'})
    
    print(response)
    
    assert response.status_code == 201
    mock_get_conversation_by_animal_and_user.assert_called_once_with(mock_user.id, animal_id)
    mock_reply_to_conversation.assert_called_once_with(mock_data, mock_user.id, mock_conversation.id)
    
def test_shelter_user_reply_uses_correct_conversation(client, mocker, auth_user):
    
    auth_user(user_id=1, shelter_id=1)
    
    mock_user_1 = mocker.Mock()
    mock_user_1.id = 1
    mock_user_2 = mocker.Mock()
    mock_user_2.id = 2
    mock_user_3 = mocker.Mock()
    mock_user_3.id = 3
    
    # mock_conversation_id = '02e4f62d-12da-41c6-8738-33b68998479a'
    mock_conversation = mocker.Mock(spec=Conversation)
    mock_conversation.id = '02e4f62d-12da-41c6-8738-33b68998479a'
    mock_conversation.shelter_id = 1
    mock_conversation.animal_id = 1
    mock_conversation.participants = [mock_user_1, mock_user_2]
    mock_conversation.to_dict.return_value = {
        "id": mock_conversation.id,
        "shelter_id": 1,
        "animal_id": "5235c2d2-266a-4851-a48a-777ce595065e",
        "created_at": "2025-07-28T14:33:39",
        "updated_at": "2025-07-28T14:33:39"
        }
    
    mock_conversation_2_id = uuid.uuid4()
    mock_conversation_2 = mocker.Mock(spec=Conversation)
    mock_conversation_2.id = mock_conversation_2_id
    mock_conversation_2.shelter_id = 1
    mock_conversation_2.animal_id = 1
    mock_conversation_2.participants = [mock_user_1, mock_user_3]
    mock_conversation_2.to_dict.return_value = {
        "id": mock_conversation_2_id,
        "shelter_id": 1,
        "animal_id": "5235c2d2-266a-4851-a48a-777ce595065e",
        "created_at": "2025-07-28T14:33:39",
        "updated_at": "2025-07-28T14:33:39"
        }
    
    mock_data = {
        "animal_id": 1,
        "shelter_id":1,
        "content": "Test message from a shelter user",
        "conversation_id": mock_conversation.id
    }
    
    mock_message = mocker.Mock(spec=Message)
    mock_message.to_dict.return_value = {
        "conversation_id": mock_conversation.id,
        "content": mock_data['content'],
    }
    
    mock_reply_to_conversation = mocker.patch.object(
        message_repo, 'reply_to_conversation',
        return_value=mock_message
    )
    
    mock_get_conversation_by_animal_and_user = mocker.patch.object(
        conversation_repo, 'get_conversation_by_animal_and_user',
        return_value=mock_conversation_2_id
    )
    
    response = client.post('/messages', json=mock_data, headers={'Authorization': f'Bearer valid-token'})
    
    json_response = response.get_json()
    
    assert response.status_code == 201
    assert json_response['conversation_id'] == mock_conversation.id
    mock_get_conversation_by_animal_and_user.assert_not_called()
    mock_reply_to_conversation.assert_called_once_with(mock_data, mock_user_1.id, mock_conversation.id)
    


    """As a user, 
    I should be able to distinguish my opened messages from my unopened messages"""
