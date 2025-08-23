import uuid
from flask import Blueprint, g, jsonify, request
from sqlalchemy import UUID
from lib.database_connection import db
from lib.models.conversation_repository import ConversationRepository
from lib.models.message_repository import MessageRepository
from lib.services.auth import token_checker


conversation_repo = ConversationRepository(db)
message_repo = MessageRepository(db)
conversation_bp = Blueprint('conversation', __name__)

@conversation_bp.route('/shelter/conversations', methods=['GET'])
@token_checker
def get_shelter_conversations():
    shelter_id = getattr(g, "shelter_id", None)
    
    if shelter_id is None:
        return jsonify({"error":"Access denied"}), 403
    
    conversations = conversation_repo.get_shelter_conversations(shelter_id)
    response_json = jsonify([conversation.to_dict() for conversation in conversations])
    return response_json, 200

# @conversation_bp.route('/conversations', methods=['GET'])
# @token_checker
# def get_user_conversations():
#     user_id = getattr(g, "user_id")
#     response = conversation_repo.get_user_conversations(user_id)
#     response_json = jsonify([conversation.to_dict() for conversation in response])
#     return response_json, 200

@conversation_bp.route('/conversations', methods=['GET'])
@token_checker
def get_conversations_with_message():
    user_id = getattr(g, "user_id", None)
    shelter_id = getattr(g, "shelter_id", None)
    
    if shelter_id is None:
        response = conversation_repo.get_user_conversations(user_id)
        response_json = jsonify([conversation.to_dict() for conversation in response])
        return response_json, 200
    
    results = conversation_repo.get_shelter_conversations_with_message(shelter_id)
    
    response_json = []
    
    for conversation, message in results:
        response_json.append({
            "conversation": conversation.to_dict(),
            "latest_message": message.to_dict() 
        })
    return response_json, 200


@conversation_bp.route('/conversations/<id>/messages', methods=['GET'])
@token_checker
def get_conversation_messages(id):
    user_id = getattr(g, "user_id")
    conversation = conversation_repo.get_conversation_by_id(id)
    shelter_id = getattr(g, "shelter_id", None)
    if shelter_id:
        if conversation.shelter_id != g.shelter_id:
            return jsonify({"error": "Access denied"}), 403
    else:
        print("get_conversations: not shelter user")
        if not any(participant.id == user_id for participant in conversation.participants):
            return jsonify({"error": "Access denied"}), 403
    
    messages = conversation_repo.get_conversation_messages(id)
    
    
    messages_json = [message.to_dict() for message in messages]
    
    response_json = {
        "conversation": conversation.to_dict(),
        "messages": messages_json
    }
    return response_json, 200

@conversation_bp.route('/conversations/<id>/messages', methods=['POST'])
@token_checker
def reply_to_conversation_messages(id):
    data = request.get_json()
    user_id = getattr(g, "user_id")
    shelter_id = getattr(g, "shelter_id", None)
   
    conversation = conversation_repo.get_conversation_by_id(id)
    if conversation is None:
        return jsonify({"error": "conversation not found"}), 404
        
    if shelter_id:
        if conversation.shelter_id != g.shelter_id:
            return jsonify({"error": "Access denied"}), 403
    else:
        if not any(participant.id == user_id for participant in conversation.participants):
            return jsonify({"error": "Access denied"}), 403
    
    reply = message_repo.reply_to_conversation(data, user_id, conversation.id)
    response = jsonify(reply.to_dict())
    return response, 201

@conversation_bp.route('/messages', methods=['POST'])
@token_checker
def create_message():
    data = request.get_json()
    animal_id = data['animal_id']
    user_id = getattr(g, "user_id")
    
    conversation_id = data.get('conversation_id') 
    
    if conversation_id:
        response = message_repo.reply_to_conversation(data, user_id, conversation_id)
        return jsonify(response.to_dict()), 201
    
    existing_conversation = conversation_repo.get_conversation_by_animal_and_user(user_id, animal_id)
    if existing_conversation:
        response = message_repo.reply_to_conversation(data, user_id, existing_conversation.id)
        return jsonify(response.to_dict()), 201
    
    else:
        response = message_repo.create_new_message_with_conversation(data, user_id, animal_id)
        return jsonify(response.to_dict()), 201
    


