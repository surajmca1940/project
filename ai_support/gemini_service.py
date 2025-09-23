import google.generativeai as genai
from django.conf import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GeminiMentalHealthAssistant:
    """
    Google Gemini AI-powered mental health assistant specifically designed 
    for college students and educational institutions.
    """
    
    def __init__(self):
        """Initialize the Gemini AI assistant with API key and configuration."""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.is_configured = True
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            self.is_configured = False
    
    def get_system_prompt(self) -> str:
        """
        Define the system prompt that establishes the AI's role and guidelines
        for mental health support in educational settings.
        """
        return """You are a compassionate, professional mental health support assistant specifically designed for college students and educational institutions. Your primary role is to provide:

1. EMOTIONAL SUPPORT & VALIDATION
- Listen empathetically to students' concerns
- Validate their feelings without judgment
- Provide reassurance and hope

2. PRACTICAL COPING STRATEGIES
- Suggest evidence-based techniques for anxiety, depression, stress
- Recommend breathing exercises, mindfulness, grounding techniques
- Provide study and time management tips

3. RESOURCE GUIDANCE
- Encourage seeking professional help when appropriate
- Suggest campus counseling services, peer support groups
- Provide crisis hotline information if needed

4. EDUCATIONAL CONTEXT
- Understand academic pressures, exam stress, social challenges
- Address common college student issues: homesickness, relationships, career anxiety
- Be culturally sensitive to diverse backgrounds

IMPORTANT GUIDELINES:
- Always be supportive, non-judgmental, and encouraging
- Never diagnose mental health conditions
- Always recommend professional help for serious concerns
- Maintain appropriate boundaries
- Keep responses concise but thorough (2-4 sentences)
- Use warm, accessible language
- Recognize crisis situations and provide immediate resources

If someone expresses thoughts of self-harm or suicide, immediately provide crisis resources and strongly encourage seeking immediate professional help.

Remember: You're a supportive companion, not a replacement for professional mental health care."""

    def generate_response(self, user_message: str, conversation_history: Optional[list] = None) -> dict:
        """
        Generate a mental health support response using Gemini AI.
        
        Args:
            user_message (str): The user's message
            conversation_history (list, optional): Previous conversation context
            
        Returns:
            dict: Response with message, status, and additional information
        """
        if not self.is_configured:
            return {
                'response': "I'm currently unable to connect to the AI service. Please try again later or contact our support team.",
                'status': 'error',
                'fallback': True
            }
        
        try:
            # Construct the conversation context
            prompt_parts = [self.get_system_prompt()]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 6 messages for context
                    if msg['type'] == 'user':
                        prompt_parts.append(f"Student: {msg['content']}")
                    else:
                        prompt_parts.append(f"Assistant: {msg['content']}")
            
            # Add current user message
            prompt_parts.append(f"Student: {user_message}")
            prompt_parts.append("Assistant:")
            
            full_prompt = "\n\n".join(prompt_parts)
            
            # Generate response from Gemini
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=300,  # Keep responses concise
                    temperature=0.7,  # Balanced creativity and consistency
                )
            )
            
            if response.text:
                ai_response = response.text.strip()
                
                # Check if response suggests professional help or crisis resources
                needs_professional_help = self._check_professional_help_indicators(user_message, ai_response)
                crisis_indicators = self._check_crisis_indicators(user_message)
                
                return {
                    'response': ai_response,
                    'status': 'success',
                    'needs_professional_help': needs_professional_help,
                    'crisis_indicators': crisis_indicators,
                    'powered_by': 'Google Gemini AI'
                }
            else:
                return self._get_fallback_response(user_message)
                
        except Exception as e:
            logger.error(f"Gemini AI error: {e}")
            return self._get_fallback_response(user_message)
    
    def _check_crisis_indicators(self, message: str) -> bool:
        """Check if the message contains crisis indicators requiring immediate attention."""
        crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'want to die', 'self harm', 
            'hurt myself', 'cutting', 'overdose', 'jump off', 'no point in living',
            'better off dead', 'can\'t go on', 'hopeless', 'worthless'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in crisis_keywords)
    
    def _check_professional_help_indicators(self, user_message: str, ai_response: str) -> bool:
        """Check if the situation warrants professional help recommendation."""
        help_indicators = [
            'professional', 'counselor', 'therapist', 'psychiatrist', 'doctor',
            'serious', 'persistent', 'ongoing', 'seek help', 'talk to someone'
        ]
        
        combined_text = (user_message + " " + ai_response).lower()
        return any(indicator in combined_text for indicator in help_indicators)
    
    def _get_fallback_response(self, user_message: str) -> dict:
        """
        Provide fallback responses when AI is unavailable.
        Uses rule-based responses similar to the original implementation.
        """
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['anxious', 'anxiety', 'worried', 'stress']):
            response = "I understand you're feeling anxious. This is very common among students. Try taking slow, deep breaths - in for 4 counts, hold for 4, out for 4. Would you like to speak with one of our counselors who can provide more personalized support?"
        elif any(word in message_lower for word in ['sad', 'depressed', 'down', 'hopeless']):
            response = "I'm sorry you're feeling this way. These feelings are valid, and you're not alone. Many students experience similar challenges. It's important to reach out for support - would you like information about our counseling services?"
        elif any(word in message_lower for word in ['exam', 'test', 'study', 'academic']):
            response = "Academic pressure can be overwhelming. Try breaking your work into smaller, manageable tasks. Remember to take regular breaks and get enough sleep. Our academic counselors can help you develop effective study strategies."
        elif self._check_crisis_indicators(user_message):
            response = "I'm concerned about what you've shared. Please know that you matter and help is available. Please reach out to a crisis counselor immediately: National Suicide Prevention Lifeline: 988. You can also contact our campus counseling center right away."
        else:
            response = "Thank you for sharing with me. I'm here to listen and support you. Can you tell me more about what's been on your mind? Remember, our counseling center is also available if you'd like to speak with a professional."
        
        return {
            'response': response,
            'status': 'success',
            'fallback': True,
            'needs_professional_help': 'counselor' in response.lower(),
            'crisis_indicators': self._check_crisis_indicators(user_message)
        }
    
    def get_coping_strategies(self, category: str = "general") -> list:
        """
        Get AI-generated coping strategies for specific mental health categories.
        
        Args:
            category (str): Category like 'anxiety', 'depression', 'stress', 'academic'
            
        Returns:
            list: List of coping strategies
        """
        if not self.is_configured:
            return self._get_fallback_coping_strategies(category)
        
        try:
            prompt = f"""As a mental health assistant for college students, provide 5 practical, evidence-based coping strategies for {category}. 

Make them:
- Specific and actionable
- Suitable for college students
- Evidence-based
- Easy to implement
- 1-2 sentences each

Format as a numbered list."""

            response = self.model.generate_content(prompt)
            
            if response.text:
                # Parse the response into a list
                strategies = []
                lines = response.text.strip().split('\n')
                for line in lines:
                    if line.strip() and any(char.isdigit() for char in line[:3]):
                        # Remove numbering and clean up
                        strategy = line.strip()
                        strategy = strategy.split('.', 1)[-1].strip() if '.' in strategy else strategy
                        if strategy:
                            strategies.append(strategy)
                
                return strategies[:5]  # Limit to 5 strategies
            
        except Exception as e:
            logger.error(f"Error generating coping strategies: {e}")
        
        return self._get_fallback_coping_strategies(category)
    
    def _get_fallback_coping_strategies(self, category: str) -> list:
        """Fallback coping strategies when AI is unavailable."""
        strategies_db = {
            'anxiety': [
                "Practice deep breathing: Inhale for 4 counts, hold for 4, exhale for 4",
                "Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
                "Use progressive muscle relaxation by tensing and releasing muscle groups",
                "Write down your worries in a journal to externalize anxious thoughts",
                "Take a 10-minute walk outside to clear your mind and get fresh air"
            ],
            'depression': [
                "Maintain a daily routine, even if it's simple",
                "Get some sunlight and fresh air each day, even for 10 minutes",
                "Connect with one person you trust - call, text, or meet in person",
                "Do one small activity you used to enjoy, even if you don't feel like it",
                "Practice self-compassion - speak to yourself like you would a good friend"
            ],
            'stress': [
                "Break large tasks into smaller, manageable steps",
                "Use the Pomodoro Technique: 25 minutes work, 5-minute break",
                "Practice mindfulness meditation for 5-10 minutes daily",
                "Prioritize tasks using the urgent/important matrix",
                "Set boundaries and learn to say 'no' to non-essential commitments"
            ],
            'academic': [
                "Create a study schedule with specific times and subjects",
                "Find a quiet, dedicated study space free from distractions",
                "Form study groups with classmates for mutual support and accountability",
                "Take regular breaks during study sessions to maintain focus",
                "Use active learning techniques like summarizing and teaching concepts aloud"
            ]
        }
        
        return strategies_db.get(category, strategies_db['anxiety'])