import uuid

from sqlalchemy import select
from lib.database_connection import db
from lib.models import Message, Conversation


def test_get_message_by_id(message_repo):
    repo = message_repo
    message_id = uuid.UUID('33ba2e0b-481e-4c4d-8ceb-3027379177c1')
    test_user_id = 2
    conversation_id = uuid.UUID('0b598972-693f-4825-b34d-83d73afd89ce')
    
    result: Message = repo.get_message_by_id(message_id)
    
    assert "This is a test message" in result.content
    assert result.sender_id == test_user_id
    assert result.conversation_id == conversation_id
    

def test_create_new_message_with_conversation(message_repo):
    """
    IF a new message is sent
    AND a conversation doesn't exist
    A new conversation should be created
    """
    repo = message_repo
    test_animal_id = uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    user_id = 2
    data = {
        "content": "This is a test to create a new message"
    }
    
    result = repo.create_new_message_with_conversation(data, user_id, test_animal_id)
    
    new_conversation = repo.db.session.get(Conversation, result.conversation_id)
    
    assert "This is a test to create a new message" in result.content
    assert result.conversation_id is not None
    assert result.sender_id is 2
    assert new_conversation.shelter_id == 1
    assert new_conversation.animal_id == uuid.UUID("6ebc0357-849a-47ac-84c1-45cb40fa15a1")
    assert any(participant.id == user_id for participant in new_conversation.participants)
    
def test_reply_to_message(message_repo):
    """
    IF a user replies to a message
    A new message should be created
    with the same conversation_id
    """
    repo = message_repo
    test_animal_id = uuid.UUID("93497185-f4be-491d-a478-b26e16ebeb4f")
    test_message_id = uuid.UUID('33ba2e0b-481e-4c4d-8ceb-3027379177c1')
    test_conversation_id = uuid.UUID('0b598972-693f-4825-b34d-83d73afd89ce')
    test_shelter_user_id = 1
    data = {
        "content": "This is a test reply",
        "conversation_id": test_conversation_id
    }
    
    result = repo.reply_to_conversation(data,test_shelter_user_id, test_conversation_id)
    
    conversation = db.session.scalars(select(Message).filter_by(conversation_id=test_conversation_id)).all()
    assert result.conversation_id is not None
    assert result.sender_id is 1
    assert len(conversation) == 2
    
def test_reply_to_message_adds_user_to_conversation_participants(message_repo):
    """
    IF a user replies to a message
    AND a new message is created
    the user should be added to conversation participants
    """
    repo = message_repo
    test_animal_id = uuid.UUID("93497185-f4be-491d-a478-b26e16ebeb4f")
    test_message_id = uuid.UUID('33ba2e0b-481e-4c4d-8ceb-3027379177c1')
    test_conversation_id = uuid.UUID('0b598972-693f-4825-b34d-83d73afd89ce')
    test_shelter_user_id = 1
    data = {
        "content": "This is a test reply",
    }
    
    result = repo.reply_to_conversation(data, test_shelter_user_id, test_conversation_id)
    
    conversation = db.session.scalar(select(Conversation).filter_by(id=test_conversation_id))
    
    assert any(participant.id == test_shelter_user_id for participant in conversation.participants)

def test_message_reply_user_isnt_duplicated_in_participants(message_repo):
    """
    IF a user replies to a message
    AND a new message is created
    the user should be added to conversation participants
    """
    repo = message_repo
    test_animal_id = uuid.UUID("93497185-f4be-491d-a478-b26e16ebeb4f")
    test_message_id = uuid.UUID('33ba2e0b-481e-4c4d-8ceb-3027379177c1')
    test_conversation_id = uuid.UUID('0b598972-693f-4825-b34d-83d73afd89ce')
    test_shelter_user_id = 1
    user_id = 2
    data = {
        "user_id": test_shelter_user_id,
        "content": "This is a test reply",
        "conversation_id": test_conversation_id
    }
    data_2 = {
        "user_id": user_id,
        "content": "This is another a test reply",
        "conversation_id": test_conversation_id
    }
    conversation = db.session.scalar(select(Conversation).filter_by(id=test_conversation_id))
    
    for message in conversation.messages:
        print(message.content)
    for participant in  conversation.participants:
        print(participant.id)
    
    repo.reply_to_conversation(data, test_shelter_user_id, test_conversation_id)
    repo.reply_to_conversation(data_2, user_id, test_conversation_id)
    
    print(f'conversation AFTER reply:')
    for message in conversation.messages:
        print(message.content)
    print(f'conversation participants AFTER reply:')
    for participant in  conversation.participants:
        print(participant.id)
    
    assert any(participant.id == test_shelter_user_id for participant in conversation.participants)
    assert len(conversation.messages) == 3
    assert len(conversation.participants) == 2

def test_delete_message(message_repo):
    """
    WHEN a message is deleted
    AND the user_id == sender_id
    It SHOULD be removed from the database
    """
    repo = message_repo
    message_id = uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e')
    test_user_id = 1
    conversation_id = uuid.UUID('05800ada-a00b-4d32-9aea-6eae201acc58')
    conversation_messages = repo.db.session.scalars(select(Message).filter_by(conversation_id=conversation_id)).all()
    assert len(conversation_messages) == 2

    message = repo.db.session.scalar(select(Message).filter_by(id=message_id))
    assert message is not None
    
    repo.delete_message_id(message_id)

    conversation_messages = repo.db.session.scalars(select(Message).filter_by(conversation_id=conversation_id)).all()
    message = repo.db.session.scalar(select(Message).filter_by(id=message_id))
    
    assert len(conversation_messages) == 1
    assert message is None
    
    for message in conversation_messages:
        assert "This is a test message reply" not in message.content
    