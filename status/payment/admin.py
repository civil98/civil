from django.contrib import admin
from .models import Order, Payment, Balance

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Balance)