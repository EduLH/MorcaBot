from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Coupon, CouponRedemption

admin.site.register(User, UserAdmin)
admin.site.register(Coupon)
admin.site.register(CouponRedemption)