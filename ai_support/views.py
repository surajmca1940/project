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
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            
            if not message:
                return JsonResponse({
                    'error': 'Please enter a message',
                    'status': 'error'
                })
            
            # Enhanced response logic based on keywords
            message_lower = message.lower()
            
            if any(word in message_lower for word in ['anxious', 'anxiety', 'worried', 'stress']):
                responses = [
                    "I hear that you're feeling anxious. Anxiety is very common among students. Try taking slow, deep breaths. Would you like some specific breathing exercises?",
                    "Stress and anxiety can be overwhelming. Have you tried any grounding techniques? One simple method is the 5-4-3-2-1 technique: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
                    "It sounds like you're dealing with anxiety. This is completely normal. Consider speaking with a counselor who can provide personalized strategies. Would you like me to help you schedule an appointment?"
                ]
            elif any(word in message_lower for word in ['sad', 'depressed', 'down', 'hopeless']):
                responses = [
                    "I'm sorry you're feeling this way. Depression can make everything feel difficult. You're taking a positive step by reaching out. Have you considered talking to a professional?",
                    "Feeling down is something many students experience. It's important to know that you're not alone and that help is available. Would you like information about counseling services?",
                    "Thank you for sharing how you're feeling. These feelings are valid, and there are ways to feel better. Sometimes talking to someone can make a big difference."
                ]
            elif any(word in message_lower for word in ['exam', 'test', 'study', 'academic']):
                responses = [
                    "Academic pressure can be really challenging. Try breaking your study into smaller, manageable chunks. What specific part of your studies is causing you the most stress?",
                    "Exam stress is very common! Some strategies that help: create a study schedule, take regular breaks, get enough sleep, and practice relaxation techniques. Would you like more specific study tips?",
                    "Academic challenges can feel overwhelming. Remember that it's okay to ask for help - from professors, tutors, or counselors. What subject or assignment is troubling you most?"
                ]
            elif any(word in message_lower for word in ['sleep', 'tired', 'insomnia', 'exhausted']):
                responses = [
                    "Sleep problems can really affect your mental health and academic performance. Try maintaining a regular sleep schedule and avoiding screens before bed. Are you having trouble falling asleep or staying asleep?",
                    "Good sleep is crucial for mental health. Some tips: keep your room cool and dark, avoid caffeine late in the day, and try relaxation exercises before bed. How long have you been having sleep issues?",
                    "Sleep difficulties are common among students. Consider creating a bedtime routine and avoiding studying in bed. If this continues, it might be worth speaking with a healthcare provider."
                ]
            elif any(word in message_lower for word in ['lonely', 'alone', 'isolated', 'friends']):
                responses = [
                    "Feeling lonely can be really hard, especially as a student. Have you considered joining clubs or study groups? Our peer support forum might also be a good place to connect with others.",
                    "Social connections are important for mental health. It can be challenging to make friends, but there are opportunities on campus. Would you like suggestions for meeting like-minded people?",
                    "You're not alone in feeling lonely. Many students struggle with this. Consider attending campus events or joining our peer support community where you can connect with others who understand."
                ]
            elif any(word in message_lower for word in ['help', 'support', 'counselor', 'therapy']):
                responses = [
                    "I'm glad you're seeking help - that takes courage. Our counseling center offers confidential support. Would you like me to provide information about booking an appointment?",
                    "Reaching out for support is a sign of strength. We have professional counselors available, as well as peer support options. What type of help would be most useful for you right now?",
                    "There are several support options available: individual counseling, group therapy, peer support forums, and crisis hotlines. What feels most comfortable for you to try first?"
                ]
            else:
                # General supportive responses
                responses = [
                    "Thank you for sharing with me. Can you tell me more about what's on your mind?",
                    "I'm here to listen. What's been troubling you lately?",
                    "It sounds like you have something important to share. I'm here to support you.",
                    "Everyone goes through difficult times. What would be most helpful for you right now?",
                    "I appreciate you reaching out. What's the main thing you'd like support with today?"
                ]
            
            import random
            bot_response = random.choice(responses)
            
            return JsonResponse({
                'response': bot_response,
                'status': 'success'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid message format',
                'status': 'error'
            })
        except Exception as e:
            return JsonResponse({
                'error': 'Something went wrong. Please try again.',
                'status': 'error'
            })
    
    return JsonResponse({'error': 'Invalid request method', 'status': 'error'})

def coping_strategies(request):
    """List of coping strategies"""
    return render(request, 'ai_support/coping_strategies.html')
