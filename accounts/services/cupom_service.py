from django.utils import timezone
from datetime import timedelta

from accounts.models import Coupon, CouponRedemption


def apply_coupon_to_user(user, code: str):
    try:
        coupon = Coupon.objects.get(code=code.upper().strip())
    except Coupon.DoesNotExist:
        return False, "Cupom inválido"

    if not coupon.is_valid():
        return False, "Cupom expirado ou indisponível"

    # evita reuse
    if CouponRedemption.objects.filter(user=user, coupon=coupon).exists():
        return False, "Cupom já utilizado"

    now = timezone.now()
    if user.plan_expires_at and user.plan_expires_at > now:
        base_date = user.plan_expires_at
    else:
        base_date = now

    user.plan_expires_at = base_date + timedelta(days=coupon.duration_days)
    user.save()

    CouponRedemption.objects.create(user=user, coupon=coupon)

    coupon.used_count += 1
    coupon.save()

    return True, f"{coupon.duration_days} dias adicionados"
