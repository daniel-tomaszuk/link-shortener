from django.urls import path
from links_handling.views import ShortUrlCreateAPIView

urlpatterns = [
    path("create-short-url", ShortUrlCreateAPIView.as_view(), name="create-short-url"),
]
