
# Mocking potential routes used for creating an animal 
from flask import request, jsonify

@app.route('/register-pet', methods=['GET'])

def pet_signup():
    data= request.get_json()
    try:
        pet = create_pet(data)
        return jsonify({'message': 'Pet successfully registered'}), 201
    except Exception as e:
        return jsonify({"message": "Pet could not be registered", "error": str(e)}), 400