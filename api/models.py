from django.conf import urls
from django.db import models

class VideoDetail(models.Model):
    videoTitle = models.CharField(max_length=500)
    description = models.TextField()
    publishingDatetime = models.DateTimeField()
    thumbnailURL = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.videoTitle}"
    