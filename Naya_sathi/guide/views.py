from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .bot import LegalAssistant
import os


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
            
            # Get response from the LegalAssistant
            response = assistant.get_response(user_query)
            
            # Return only the simplified response without sources
            return JsonResponse({
                'response': response['simplified_response']
                # Removed sources from the response
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET request - render the chat page
    return render(request, 'guidence.html')

def home(request):
    return render(request, 'guidence.html')