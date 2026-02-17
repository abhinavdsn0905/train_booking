from django.db import models

# Create your models here.
from trains.models import Train
import random


class Booking(models.Model):
    username = models.CharField(max_length=50)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)

    travel_date = models.DateField(null=True, blank=True)
    passengers = models.IntegerField(default=1)
    passenger_details = models.TextField(null=True, blank=True)

    pnr = models.CharField(max_length=10, unique=True, null=True, blank=True)
    total_price = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pnr:
            import random
            self.pnr = str(random.randint(1000000000, 9999999999))
        super().save(*args, **kwargs)


 