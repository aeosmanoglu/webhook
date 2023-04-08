import json
import os

import requests
from django.http import JsonResponse


# http://localhost:8000/hook?appname=myapp&id=1&id=2&id=3
def hook(request):
    # Only allow POST requests
    if request.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    # Get the appname and ids from the query string
    appname = request.GET.get('appname')
    ids = request.GET.getlist('id')

    # Validate the query string
    if not appname:
        return JsonResponse({'error': 'appname is required'}, status=400)
    if not ids:
        return JsonResponse({'error': 'at least one id is required'}, status=400)

    # Get the message from the request body
    try:
        data = json.loads(request.body)
        message = data.get('message', None) or data.get('msg', None)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid json'}, status=400)
    if not message:
        return JsonResponse({'error': 'message or msg is required'}, status=400)

    # Send the message to the users with the given ids over IMS
    try:
        url = os.environ['IMS_URL']
        payload = {
            "users": ids,
            "message": "${appname}:\n${message}".format(appname=appname, message=message)
        }
        headers = {
            "Content-Type": "application/json",
            "username": os.environ['IMS_USERNAME'],
            "accessToken": os.environ['IMS_ACCESS_TOKEN']
        }
        response = requests.request("Post", url, json=payload, headers=headers, timeout=5)

        if response.status_code == 204:
            return JsonResponse({'success': 'Message send'}, status=200)
        else:
            return JsonResponse({'error': response.text}, status=response.status_code)
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'IMS timeout'}, status=504)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
