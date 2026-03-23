import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from accounts.services.cupom_service import apply_coupon_to_user

User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    data = json.loads(request.body)

    phone = data.get("phone")
    name = data.get("name")
    coupon_code = data.get("coupon")

    if not phone:
        return JsonResponse({"error": "phone required"}, status=400)

    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={"name": name or ""}
    )

    # aplica trial padrão
    if created:
        user.plan_expires_at = timezone.now() + timedelta(days=7)
        user.save()

    # aplica cupom
    if coupon_code:
        success, message = apply_coupon_to_user(user, coupon_code)

        return JsonResponse({
            "status": "ok" if success else "error",
            "message": message
        })

    return JsonResponse({
        "status": "ok",
        "message": "Usuário criado"
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