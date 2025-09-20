from django.db import models

class SolarInstallationCenter(models.Model):
    # external_id stores the 'id' field from your JSON
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ['external_id']

    def __str__(self):
        return f"{self.name} ({self.external_id})"
