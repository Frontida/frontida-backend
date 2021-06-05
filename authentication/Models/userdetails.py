from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from .user import User

CITY = [
    ("Jaipur", "Jaipur"),
    ("Kanpur", "Kanpur"),
    ("Jabalpur", "Jabalpur"),
    ("Indore", "Indore"),
    ("Nainital", "Nainital"),
    ("Ahmedabad", "Ahmedabad"),
    ("Gandinagar", "Gandhinagar"),
    ("Bhilwara", "Bhilwara"),
    ("Haldwani", "Haldwani"),
    ("Ajmer", "Ajmer")
]

class UserDetails(models.Model):
    store_name = models.CharField(max_length=100, unique=False)
    store_owner = models.CharField(max_length=70)
    address = models.CharField(max_length=500)
    landmark = models.CharField(null=True, max_length=50)
    city = models.CharField(max_length=50, choices=CITY)
    pincode = models.PositiveIntegerField()
    contact = models.BigIntegerField()
    point = models.PointField(geography=True, default=Point(0.0, 0.0))
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.email