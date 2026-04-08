from rest_framework import serializers

class MenuSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField()
    menu_name = serializers.CharField()
    category = serializers.CharField()
    price = serializers.FloatField()
    spicy_level = serializers.IntegerField(min_value=1, max_value=5)
    is_available = serializers.BooleanField()
    description = serializers.CharField()