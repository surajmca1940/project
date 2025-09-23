from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ChatSession, ChatMessage
from .gemini_service import GeminiMentalHealthAssistant
import json
import uuid
import logging

logger = logging.getLogger(__name__)

def chat_home(request):
    """AI Chat interface"""
    return render(request, 'ai_support/chat.html')

@csrf_exempt
def send_message(request):
    """Handle chat messages using Gemini AI (API endpoint)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            session_id = data.get('session_id', str(uuid.uuid4()))
            
            if not message:
                return JsonResponse({
                    'error': 'Please enter a message',
                    'status': 'error'
                })
            
            # Initialize Gemini AI assistant
            gemini_assistant = GeminiMentalHealthAssistant()
            
            # Get or create chat session
            chat_session = None
            conversation_history = []
            
            try:
                if request.user.is_authenticated:
                    chat_session, created = ChatSession.objects.get_or_create(
                        session_id=session_id,
                        defaults={'user': request.user}
                    )
                else:
                    chat_session, created = ChatSession.objects.get_or_create(
                        session_id=session_id
                    )
                
                # Get conversation history
                recent_messages = chat_session.messages.all().order_by('-timestamp')[:12]
                conversation_history = [
                    {
                        'type': 'user' if msg.message_type == 'user' else 'bot',
                        'content': msg.content
                    }
                    for msg in reversed(recent_messages)
                ]
                
            except Exception as e:
                logger.error(f"Error managing chat session: {e}")
                # Continue without session tracking
            
            # Generate response using Gemini AI
            ai_response_data = gemini_assistant.generate_response(
                user_message=message,
                conversation_history=conversation_history
            )
            
            # Save messages to database if session exists
            if chat_session:
                try:
                    # Save user message
                    ChatMessage.objects.create(
                        session=chat_session,
                        message_type='user',
                        content=message
                    )
                    
                    # Save bot response
                    ChatMessage.objects.create(
                        session=chat_session,
                        message_type='bot',
                        content=ai_response_data['response']
                    )
                    
                except Exception as e:
                    logger.error(f"Error saving chat messages: {e}")
            
            # Prepare response with additional context
            response_data = {
                'response': ai_response_data['response'],
                'status': ai_response_data['status'],
                'session_id': session_id
            }
            
            # Add warning indicators if needed
            if ai_response_data.get('crisis_indicators'):
                response_data['crisis_warning'] = True
                response_data['crisis_message'] = "If you're having thoughts of self-harm, please reach out immediately: National Crisis Lifeline 988"
            
            if ai_response_data.get('needs_professional_help'):
                response_data['professional_help_suggested'] = True
                response_data['help_message'] = "Consider speaking with a professional counselor for personalized support"
            
            # Add AI attribution
            if not ai_response_data.get('fallback'):
                response_data['powered_by'] = ai_response_data.get('powered_by', 'AI Assistant')
            
            return JsonResponse(response_data)
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid message format',
                'status': 'error'
            })
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            return JsonResponse({
                'error': 'Something went wrong. Please try again.',
                'status': 'error'
            })
    
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'})

@csrf_exempt
def get_coping_strategies(request):
    """Get AI-powered coping strategies for specific categories"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = data.get('category', 'general').lower()
            
            # Initialize Gemini AI assistant
            gemini_assistant = GeminiMentalHealthAssistant()
            
            # Get AI-generated coping strategies
            strategies = gemini_assistant.get_coping_strategies(category)
            
            return JsonResponse({
                'strategies': strategies,
                'category': category,
                'status': 'success',
                'powered_by': 'Google Gemini AI' if gemini_assistant.is_configured else 'Built-in strategies'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid request format',
                'status': 'error'
            })
        except Exception as e:
            logger.error(f"Error getting coping strategies: {e}")
            return JsonResponse({
                'error': 'Unable to get coping strategies. Please try again.',
                'status': 'error'
            })
    
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'})

def coping_strategies(request):
    """List of coping strategies"""
    # Get categories for the template
    categories = ['anxiety', 'depression', 'stress', 'academic']
    return render(request, 'ai_support/coping_strategies.html', {
        'categories': categories
    })
