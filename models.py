from django.db import models
from django.contrib.auth.models import User

class ParkingLot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Camera(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    camera_type = models.CharField(max_length=20)  # 'entry' или 'exit'
    is_active = models.BooleanField(default=True)

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=False)

# models.py - Разширение за SaaS
class Subscription(models.Model):
    PLANS = [
        ('basic', 'Basic - 1 паркинг'),
        ('pro', 'Pro - 5 паркинга'),
        ('enterprise', 'Enterprise - Неограничено')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLANS)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2)

class Revenue(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=8, decimal_places=2)
