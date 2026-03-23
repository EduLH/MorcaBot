import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from expenses.services.message_service import process_incoming_message


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    message = data.get("message")
    phone = data.get("phone")

    if not message or not phone:
        return JsonResponse({"error": "missing fields"}, status=400)

    result = process_incoming_message(phone, message)

    return JsonResponse(result, status=200)