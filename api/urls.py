from django.urls import path
from . import views

urlpatterns = [
    path('hook/', views.hook, name='hook'),
]