import uuid
from accounts.models import Coupon


def generate_referral_coupon(user):
    code = f"REF-{str(uuid.uuid4())[:8].upper()}"

    coupon = Coupon.objects.create(
        code=code,
        duration_days=30,
        max_uses=5,
        created_by=user,
        is_referral=True,
    )

    return coupon.code