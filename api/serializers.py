from rest_framework import serializers
from .models import VideoDetail

class VideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoDetail
        fields = '__all__'