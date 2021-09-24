from rest_framework import serializers
from .models import UserImages

class BasicPlanListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = UserImages
        fields = ['id','title','first_thumbnail','user','original_image',]
        extra_kwargs = {'original_image': {'write_only': True},}

class PremiumPlanListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_thumbnail = serializers.ImageField(read_only=True)
    second_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = UserImages
        fields = ['id','title','first_thumbnail', 'user', 'second_thumbnail','original_image',]

class EnterprisePlanListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_thumbnail = serializers.ImageField(read_only=True)
    second_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = UserImages
        fields = ['id','title','expire_time','first_thumbnail', 'user', 'second_thumbnail','original_image',]

