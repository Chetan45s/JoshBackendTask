from django.urls import path
from django import views
from .views import *


urlpatterns = [
    path('',FetchAPI.as_view(),name='api'),   # calling fetchapi view to render data
]
