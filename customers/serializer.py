from rest_framework import serializers

from .models import company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = "__all__"