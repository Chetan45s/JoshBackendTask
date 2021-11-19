from django.contrib import admin
from .models import VideoDetail

@admin.register(VideoDetail)
class VideoDetailAdmin(admin.ModelAdmin):
    pass
