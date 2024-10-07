from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('', views.home, name='home'),
    path('about-us', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<str:pk>/', views.blogsd, name='blogsd'),

    path('service/', views.service, name = 'service'),
    path('service/<str:pk>/', views.service_detail, name='service_detail'),
    
    
] 