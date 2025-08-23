from datetime import datetime
import uuid

import pytest
from lib.models import Conversation, Shelter, Animal, Message, User

from lib.database_connection import db

def test_get_all_conversations(conversation_repo):
    """
    get all conversations should return all conversations
    """
    repo = conversation_repo
    test_conversations = []
    expected_animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    
    for n in range(4):
        test_conversations.append(Conversation(
            shelter_id=1,
            animal_id=expected_animal_id
        ))
    
    repo.db.session.add_all(test_conversations)
    # db.session.commit()
    
    result = repo.get_all_conversations()
    matching = [conv for conv in result if conv.animal_id == expected_animal_id]
    assert len(matching) == 5
    assert all(isinstance(conv, Conversation) for conv in result)
    

def test_get_conversation_by_id(conversation_repo):
    """
    get_conversation_by_id should return all conversations with given id
    """
    repo = conversation_repo
    matching_animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    conversation_id = uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28")
    
    result = repo.get_conversation_by_id(conversation_id)
    assert result.shelter_id == 1
    assert result.animal_id == matching_animal_id
    
def test_get_conversation_by_user_and_shelter(conversation_repo):
    """
    GIVEN an animal_id and user_id
    IF a conversation has the animal_id and user_id
    AND the user is not a shelter user
    A conversation id should be returned
    """
    repo = conversation_repo
    user_id = 2
    animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    animal_id_2 = uuid.UUID("93497185-f4be-491d-a478-b26e16ebeb4f")
    conversation_id = uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28")
    
    result = repo.get_conversation_by_animal_and_user(user_id, animal_id)
    assert result.id == conversation_id
    
def test_get_conversation_messages(conversation_repo):
    repo = conversation_repo
    conversation_id = uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28")
    
    test_message = Message(
            content=f"This is a test message reply",
            sender_id=2,
            conversation_id=conversation_id
            )

    db.session.add(test_message)
    
    result = repo.get_conversation_messages(conversation_id)
    
    assert len(result) == 2
    for message in result:
        assert message.conversation_id == conversation_id
        assert 'This is a test message' in  message.content


def test_get_user_conversations(conversation_repo):
    """
    get_user_conversations should return all conversations belonging to the user id
    """
    repo = conversation_repo
    test_user = repo.db.session.get(User, 2)
    test_user_2 = User(email="user_2@example444.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="public", last_name="user_2")
    animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    shelter_id = 1
    conversation_1 = Conversation(
            shelter_id=shelter_id,
            animal_id=animal_id,
            participants=[test_user]
        )
    conversation_2 = Conversation(
            shelter_id=shelter_id,
            animal_id=animal_id,
            participants=[test_user_2]
        )
    conversation_2 = Conversation(
            shelter_id=shelter_id,
            animal_id=animal_id,
            participants=[test_user_2, test_user]
        )
    
    repo.db.session.add(conversation_1)
    repo.db.session.add(conversation_2)
    
    user_conversations = repo.get_user_conversations(2)
    user_2_conversations = repo.get_user_conversations(test_user_2.id)
    assert len(user_conversations) == 3
    assert len(user_2_conversations) == 2
    
def test_get_shelter_conversations(conversation_repo):
    """
    get_shelter_conversations should return all conversations belonging to the shelter
    """
    repo = conversation_repo
    test_shelter_2 = Shelter(id=2, name="Example Shelter", location="South London", 
                          email="info@example2.com", domain="example2.com", phone_number="07123123123")
    test_animal_2 = Animal(id=uuid.UUID("93497185-f4be-491d-a478-b26e16ebeb4f"),name="Test Two", species="dog", age=2, breed="test breed",
                          location="London", male=True, bio="This is a test dog.",
                          neutered=False, lives_with_children=False, images=1,
                          isActive=True, shelter=test_shelter_2)
    animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    shelter_id_1 = 1
    conversation_1 = Conversation(
            shelter_id=shelter_id_1,
            animal_id=animal_id
        )
    conversation_2 = Conversation(
            shelter_id=shelter_id_1,
            animal_id=animal_id
        )
    conversation_3 = Conversation(
            shelter_id=shelter_id_1,
            animal_id=animal_id
        )
    conversation_4 = Conversation(
            shelter=test_shelter_2,
            animal=test_animal_2
        )
    conversation_5 = Conversation(
            shelter=test_shelter_2,
            animal=test_animal_2
        )
    
    db.session.add_all([conversation_1, conversation_2, conversation_3, conversation_4, conversation_5])
   
    result = repo.get_shelter_conversations(1)
    assert len(result) == 4
    
def test_get_shelter_conversations_with_message(conversation_repo):
    """
    get_shelter_conversations_with_message should return 
    all conversations belonging to the shelter
    AND most recent message in conversation
    """
    repo = conversation_repo
    test_user = repo.db.session.get(User, 2)
    conversation_id = uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28")
    test_shelter_user = User(id=3, email="user3@example.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="shelter", last_name="user", shelter_id=1)
    test_shelter_2 = Shelter(id=2, name="Example Shelter", location="South London", 
                          email="info@example2.com", domain="example2.com", phone_number="07123123123")
    test_animal_2 = Animal(id=uuid.UUID("93497185-f4be-491d-a478-b26e16ebeb4f"),name="Test Two", species="dog", age=2, breed="test breed",
                          location="London", male=True, bio="This is a test dog.",
                          neutered=False, lives_with_children=False, images=1,
                          isActive=True, shelter=test_shelter_2)
    animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    shelter_id_1 = 1
    conversation_1 = Conversation(
            shelter_id=shelter_id_1,
            animal_id=animal_id,
            participants=[test_user, test_shelter_user]
        )
    message_1 = Message(
        content="This should not be visible",
        sender_id=2,
        conversation=conversation_1,
        created_at=datetime.fromisoformat('2025-08-03T16:23:20.295083+01:00')
    )
    message_2 = Message(
        content="conversation_1 latest message",
        sender=test_shelter_user,
        conversation=conversation_1,
        created_at=datetime.fromisoformat('2025-08-04T16:23:20.295083+01:00')
    )
    message_3 = Message(
            content=f"This should not be visible",
            sender=test_user,
            conversation_id=conversation_id,
            created_at=datetime.fromisoformat('2025-01-01T16:26:26.841685+01:00')
            )
    
    repo.db.session.add_all([message_1, message_2, message_3 ])
   
    results = repo.get_shelter_conversations_with_message(1)
    
    messages = [message for _, message in results]
    assert len(messages) == 2
    assert any("This should not be visible" != message.content for message in messages)
    assert any(message_2.content == message.content for message in messages)
    assert any("This is a test message from public user 2 to shelter id 1 for test_animal_1" == message.content for message in messages)
    
    

def test_create_conversation(conversation_repo):
    """
    WHEN a new conversation is created
    it SHOULD include the shelter_id, animal_id and participants"""
    repo = conversation_repo
    test_animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    test_user_id = 2
    test_shelter_id = 1
    conversation_data = {'shelter_id': test_shelter_id, 'animal_id': test_animal_id, 'user_id': test_user_id}
    
    result = repo.create_conversation(conversation_data)
    test_user = repo.db.session.get(User, test_user_id)
    
    assert result.shelter_id == test_shelter_id
    assert result.animal_id == test_animal_id
    assert test_user in result.participants
    assert result.created_at is not None
    assert result.updated_at is not None
    assert result.owner is None
    
def test_add_participant(conversation_repo):
    """
    add participant SHOULD append the given user to conversation.participants
    """
    repo = conversation_repo
    
    conversation_id = uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28")
    new_user = User(id=3, email="user_2@example.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="public", last_name="user", shelter_id=1)
    
    repo.db.session.add(new_user)

    
    data = {"user_id": new_user.id, "conversation_id": conversation_id}
    
    result = repo.add_participant(data)
    
    assert new_user in result.participants
    assert len(result.participants) == 2

def test_add_participant_to_invalid_conversation_errors(conversation_repo):
    repo = conversation_repo
    new_user = User(id=3,email="user_2@example.com", 
                    password="$2b$12$ktcmG68CCpPTv6QgRiqGOOhvjuSmEXjJyJmurK3RhvKTYihVJXM8W",
                    first_name="public", last_name="user", shelter_id=1)
    
    conversation_id = uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e')
    repo.db.session.add(new_user)
    
    
    data = {"user_id": new_user.id, "conversation_id": conversation_id}
    
    with pytest.raises(ValueError) as err:
        repo.add_participant(data)
    error_message = str(err.value)
    print(error_message)
    assert error_message == "Conversation not found"
    
def test_add_invalid_user_to_participant_errors(conversation_repo):
    repo = conversation_repo
    
    conversation_id = uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28")
    
    data = {"user_id": 3, "conversation_id": conversation_id}
    
    with pytest.raises(ValueError) as err:
        repo.add_participant(data)
    error_message = str(err.value)
    print(error_message)
    assert error_message == "User not found"
    
def test_cannot_add_duplicate_participants(conversation_repo):
    repo = conversation_repo
    
    conversation_id = uuid.UUID("ce8ea8a3-3680-41c5-83d1-7bf59cdc5a28")
    
    conversation = repo.db.session.get(Conversation, conversation_id)
    assert len(conversation.participants) == 1
    
    data = {"user_id": 2, "conversation_id": conversation_id}
    
    result = repo.add_participant(data)
    
    assert len(result.participants) == 1