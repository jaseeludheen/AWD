"""
URL configuration for awd_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from django .conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'), 
    
    # Include the URLs from the dataentry app
    path('dataentry/', include('dataentry.urls')),

    path('celery-test/', views.celery_test , name='celery_test'),  # URL for the Celery test view
    path('email-test/', views.email_test, name='email_test'),  # URL for the email test view
    path('register/', views.register, name='register'),  # URL for the registration view)
    path('login/', views.login, name='login'),  # URL for the login view
    path('logout/', views.logout, name='logout'),  # URL for the logout view

    # Include the URLs from the emails app
    path('emails/', include('emails.urls')),  
    # Include the URLs from the image_compression app
    path('image-compression/', include('image_compression.urls')),  
    # Include the URLs from the stockanalysis app
    path('stockanalysis/', include('stockanalysis.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                             