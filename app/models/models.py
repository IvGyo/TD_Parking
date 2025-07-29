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
