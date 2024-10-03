from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.blogs, name='blogs'),
    
    path('blogs/<str:pk>/', views.blogsd, name='blogsd'),
    
    
] 