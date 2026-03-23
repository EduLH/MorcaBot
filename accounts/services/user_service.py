from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from cupom_service import apply_coupon_to_user

User = get_user_model()


def create_user_with_optional_coupon(phone: str, name: str = "", coupon_code: str = None):
    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={"name": name or ""}
    )

    if created:
        trial_days = getattr(settings, "TRIAL_DURATION_DAYS", 7)

        user.plan_expires_at = timezone.now() + timedelta(days=trial_days)
        user.save()

    if coupon_code:
        success, message = apply_coupon_to_user(user, coupon_code)
        return user, success, message

    return user, True, "Usuário criado com sucesso"