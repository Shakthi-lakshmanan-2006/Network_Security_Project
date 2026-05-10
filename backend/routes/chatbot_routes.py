from flask import Blueprint, request, jsonify
from services.gemini_service import gemini_service
from utils.logger import logger

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint for the AI chatbot.
    Handles JSON messages or multipart/form-data with files.
    """
    try:
        user_message = ""
        files_data = []

        if request.content_type and 'multipart/form-data' in request.content_type:
            user_message = request.form.get('message', '')
            for key in request.files:
                file = request.files[key]
                files_data.append({
                    'name': file.filename,
                    'type': file.content_type,
                    'content': file.read()
                })
        else:
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({'error': 'Message is required'}), 400
            user_message = data['message']

        logger.info(f"Chatbot request: {user_message[:50]}... ({len(files_data)} files)")
        
        response = gemini_service.get_response(user_message, files=files_data)
        
        return jsonify({
            'status': 'success',
            'response': response
        }), 200

    except Exception as e:
        logger.error(f"Chatbot route error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error during chat processing'
        }), 500
