import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from accounts.services.user_service import create_user_with_optional_coupon


User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "invalid json"}, status=400)

    phone = data.get("phone")
    name = data.get("name")
    coupon_code = data.get("coupon")

    if not phone:
        return JsonResponse({"error": "phone required"}, status=400)

    user, success, message = create_user_with_optional_coupon(
        phone=phone,
        name=name,
        coupon_code=coupon_code
    )

    return JsonResponse({
        "status": "ok" if success else "error",
        "message": message
    })


@require_http_methods(["GET"])
def list_users(request):
    users = list(
        User.objects.values(
            "id", "phone", "first_name", "last_name", "email"
        )
    )
    return JsonResponse(users, safe=False)


@require_http_methods(["GET"])
def get_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse(
        {
            "id": str(user.id),
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
    )


@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    try:
        data = json.loads(request.body)

        user.phone = data.get("phone", user.phone)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)

        user.save()

        return JsonResponse(
            {
                "id": str(user.id),
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        )
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({"status": "deleted"}, status=204)