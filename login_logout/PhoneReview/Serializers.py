from rest_framework import serializers
from .models import Brand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name','origin','manufacturingSince']

    def create(self, validated_data):
        return Brand.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.manufacturingSince = validated_data.get('manufacturingSince', instance.manufacturingSince)
        instance.save()
        return instance