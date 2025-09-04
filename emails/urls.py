from django.urls import path
from .import views

urlpatterns = [
    path('send-mail/', views.send_email, name='send_email'),
]



