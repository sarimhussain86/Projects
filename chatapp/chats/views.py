from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

def chat_view(request, room_name):
    return render(request, 'chats/chat.html', {'room_name': room_name})

@csrf_exempt
def random_chat_view(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            return JsonResponse({
                'status': 'success',
                'received_json': json_data
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }, status=405)