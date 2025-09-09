from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def chat_home(request):
    """AI Chat interface"""
    return render(request, 'ai_support/chat.html')

@csrf_exempt
def send_message(request):
    """Handle chat messages (API endpoint)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        
        # Simple response logic - replace with actual AI integration
        responses = [
            "I understand you're going through a difficult time. Can you tell me more?",
            "Thank you for sharing. Have you considered speaking with a counselor?",
            "It's normal to feel overwhelmed. Here are some coping strategies...",
            "Would you like me to help you schedule an appointment?",
            "Remember that seeking help is a sign of strength."
        ]
        
        import random
        bot_response = random.choice(responses)
        
        return JsonResponse({
            'response': bot_response,
            'status': 'success'
        })
    
    return JsonResponse({'error': 'Invalid request method'})

def coping_strategies(request):
    """List of coping strategies"""
    return render(request, 'ai_support/coping_strategies.html')
