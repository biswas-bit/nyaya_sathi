from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import json
from .bot import LegalAssistant
import os
from .models import ChatHistory

# Initialize assistant
PDF_PATH = os.path.join(os.path.dirname(__file__), 'C:\\Users\\Dell\\OneDrive - City Community Education Consultancy Pvt. Ltd\\Desktop\\hackathon\\digital_nyaya_sathi\\nyaya_sathi\\Naya_sathi\\guide\\cmurder_Forgery_merged (1).pdf')
assistant = LegalAssistant(PDF_PATH)

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('query', '')
            
            if not user_query:
                return JsonResponse({'error': 'Empty query'}, status=400)
            
            # Ensure session exists for anonymous users
            if not request.session.session_key:
                request.session.create()
            
            # Store user message in database
            ChatHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                message=user_query,
                is_user_message=True
            )
            
            # Get response from the LegalAssistant
            response = assistant.get_response(user_query)
            bot_response = response['simplified_response']
            
            # Store bot response in database
            ChatHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                message=user_query,
                response=bot_response,
                is_user_message=False
            )
            
            return JsonResponse({
                'response': bot_response
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET request - render the chat page
    return render(request, 'guidence.html')

def home(request):
    # Get chat history for the current user or session
    if request.user.is_authenticated:
        # For logged-in users, get their chat history
        chat_history = ChatHistory.objects.filter(user=request.user).order_by('created_at')
    else:
        # For anonymous users, get chat history by session key
        if not request.session.session_key:
            request.session.create()
        chat_history = ChatHistory.objects.filter(
            user=None,
            session_key=request.session.session_key
        ).order_by('created_at')
    
    # Prepare context with chat history
    context = {
        'chat_history': chat_history
    }
    
    return render(request, 'guidence.html', context)
