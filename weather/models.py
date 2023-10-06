from django.db import models


# Create your models here.
class Weather(models.Model):
    district = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    temp = models.FloatField()

    def __str__(self):
        return f"{self.district} {str(self.date)} {str(self.time)}"
