import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    billing_cycle_day = models.IntegerField(default=1)

    phone = models.CharField(max_length=20, unique=True)

    is_active_user = models.BooleanField(default=True)

    plan_expires_at = models.DateTimeField(null=True, blank=True)

    used_coupon = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name} - {self.phone}'

    def has_active_plan(self) -> bool:
        if not self.plan_expires_at:
            return False

        return self.plan_expires_at >= timezone.now()


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_referral = models.BooleanField(default=False)
    duration_days = models.IntegerField()  # quanto tempo libera

    max_uses = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)

    expires_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_coupons"
    )

    def is_valid(self):
        from django.utils import timezone

        if not self.is_active:
            return False

        if self.expires_at and self.expires_at < timezone.now():
            return False

        if self.max_uses and self.used_count >= self.max_uses:
            return False

        return True

    def __str__(self):
        return self.code

class CouponRedemption(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    coupon = models.ForeignKey("Coupon", on_delete=models.CASCADE)

    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "coupon")