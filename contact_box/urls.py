from django.urls import path
from contact_box.views import home

urlpatterns = [
    path('home/', home),
]