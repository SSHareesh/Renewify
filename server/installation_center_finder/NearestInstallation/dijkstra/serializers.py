from rest_framework import serializers
from .models import SolarInstallationCenter

class SolarInstallationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarInstallationCenter
        fields = ['external_id', 'name', 'address', 'phone', 'latitude', 'longitude']
