#!/usr/bin/env python
"""
Test script for Gemini AI integration in the Mental Health Platform
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/suraj/project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_platform.settings')
django.setup()

from ai_support.gemini_service import GeminiMentalHealthAssistant

def test_gemini_integration():
    """Test the Gemini AI integration with various mental health scenarios"""
    
    print("🧠 Testing Gemini AI Mental Health Assistant")
    print("=" * 50)
    
    # Initialize the assistant
    assistant = GeminiMentalHealthAssistant()
    
    if not assistant.is_configured:
        print("❌ Gemini AI is not properly configured!")
        print("Check your API key in settings.py")
        return
    
    print("✅ Gemini AI initialized successfully!")
    print(f"🔧 Model configured: {assistant.model._model_name}")
    
    # Test scenarios for college students
    test_scenarios = [
        {
            'category': 'Anxiety',
            'message': "I have a big exam tomorrow and I can't stop worrying about it. My heart is racing and I can't focus on studying.",
            'expected_keywords': ['anxiety', 'exam', 'breathing', 'study']
        },
        {
            'category': 'Depression', 
            'message': "I've been feeling really down lately. Nothing seems fun anymore and I don't want to hang out with friends.",
            'expected_keywords': ['depression', 'feelings', 'friends', 'support']
        },
        {
            'category': 'Academic Stress',
            'message': "I'm overwhelmed with assignments and I feel like I'm falling behind in all my classes.",
            'expected_keywords': ['academic', 'assignments', 'overwhelmed', 'time management']
        },
        {
            'category': 'Social Issues',
            'message': "I'm having trouble making friends at college and I feel really lonely.",
            'expected_keywords': ['lonely', 'friends', 'social', 'connect']
        },
        {
            'category': 'Crisis Situation',
            'message': "I feel hopeless and sometimes think things would be better if I wasn't here.",
            'expected_keywords': ['crisis', 'help', 'support', 'counselor']
        }
    ]
    
    print("\n🧪 Testing AI Responses:")
    print("-" * 30)
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}. Testing: {scenario['category']}")
        print(f"Student Message: \"{scenario['message']}\"")
        
        # Generate response
        response_data = assistant.generate_response(scenario['message'])
        
        if response_data['status'] == 'success':
            print(f"✅ AI Response: {response_data['response']}")
            
            # Check for important indicators
            if response_data.get('crisis_indicators'):
                print("🚨 Crisis indicators detected!")
            
            if response_data.get('needs_professional_help'):
                print("👨‍⚕️ Professional help recommended")
                
            if response_data.get('powered_by'):
                print(f"🤖 Powered by: {response_data['powered_by']}")
                
        else:
            print(f"❌ Error: {response_data.get('error', 'Unknown error')}")
            if response_data.get('fallback'):
                print("🔄 Using fallback response")
        
        print("-" * 50)
    
    # Test coping strategies
    print("\n🛠️ Testing AI-Generated Coping Strategies:")
    print("-" * 30)
    
    strategy_categories = ['anxiety', 'depression', 'stress', 'academic']
    
    for category in strategy_categories:
        print(f"\n📚 {category.title()} Coping Strategies:")
        strategies = assistant.get_coping_strategies(category)
        
        for j, strategy in enumerate(strategies, 1):
            print(f"  {j}. {strategy}")
    
    print("\n🎉 Gemini AI Integration Test Completed!")
    print("The mental health platform now has advanced AI support powered by Google Gemini!")

if __name__ == "__main__":
    test_gemini_integration()