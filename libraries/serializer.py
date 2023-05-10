from rest_framework import serializers
from libraries.models import Items

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        field = '__all__'

  