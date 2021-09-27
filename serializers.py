from rest_framework import serializers
from apitest1.models import brewery

class brewery_serializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100)