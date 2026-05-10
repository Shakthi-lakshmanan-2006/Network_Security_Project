import os
import google.generativeai as genai
from config import Config
from utils.logger import logger
import PIL.Image
import io

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.warning("[WARN] GEMINI_API_KEY not found in environment variables. Chatbot will not function correctly.")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
            self.chat_sessions = {}

    def get_response(self, user_message, files=None, session_id='default'):
        """
        Sends a message to Gemini and returns the response.
        Supports multi-modal input (files).
        """
        if not self.api_key:
            return "I'm sorry, the Gemini API key is not configured. Please add your GEMINI_API_KEY to the backend/.env file to enable the AI assistant. [SUGGESTIONS] How to get an API key?, What is Gemini?, System help"

        try:
            # System prompt to define the Jarvis persona
            system_prompt = (
                "You are 'NetSec Guard AI', an advanced security intelligence system. "
                "Provide high-level network security analysis and threat detection. "
                "Be sophisticated, precise, and professional. "
                "FORMATTING RULES: "
                "1. DO NOT use raw markdown headers like '###'. Use plain bold text for titles. "
                "2. Use bullet points for lists. "
                "3. Keep descriptions concise and easy to read. "
                "4. Always provide 3 short follow-up questions after the tag [SUGGESTIONS]."
            )

            content_parts = [system_prompt, f"User: {user_message}"]
            
            if files:
                for file_data in files:
                    # If it's an image, convert to PIL
                    if file_data['type'].startswith('image/'):
                        img = PIL.Image.open(io.BytesIO(file_data['content']))
                        content_parts.append(img)
                    else:
                        # For other files (PDF etc), we pass them as raw bytes if supported or just mention them
                        # Note: 1.5 Flash supports PDF/Doc but requires specific handling or upload
                        # For simplicity in this step, we'll focus on images
                        content_parts.append(f"[File Attachment: {file_data['name']} ({file_data['type']})]")

            response = self.model.generate_content(content_parts)
            
            if response and response.text:
                return response.text
            else:
                return "Analysis complete. I couldn't generate a verbal response, but the data has been processed. [SUGGESTIONS] What is phishing?, How to block an IP?, Show me active threats"

        except Exception as e:
            logger.error(f"Error in GeminiService: {e}")
            return f"An error occurred in my processing core: {str(e)} [SUGGESTIONS] Check logs, Restart server, Contact admin"

# Singleton instance
gemini_service = GeminiService()
