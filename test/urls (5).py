from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .views import StaticSitemap, BlogSitemap, VerticalSitemap  # Import your sitemap classes


app_name='home'


sitemaps = {
    'static': StaticSitemap,
    'blogs': BlogSitemap,
    'verticals': VerticalSitemap,
    # Add other sitemaps here if you create more classes
}
urlpatterns = [
    
  
    
    path('', views.home, name='home'),
    path('vessel-schedule/', views.vessel, name = 'vessel'),
    path('about/', views.about, name = 'about'),
    path('service/', views.service, name = 'service'),
    path('service/<str:pk>/', views.service_detail, name='service_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.blog, name='blog'),
    path('blogs/<str:pk>/', views.blog_detail, name='blog_detail'),
    path('verticals/', views.verticals, name = 'verticals'),
    path('vertical/<str:pk>/', views.vertical_detail, name='vertical_detail'),
    path('careers/', views.careers, name = 'careers'),
    path('misson/', views.misson, name = 'misson'),
    path('teams/', views.teams, name = 'teams'),
    path('clients/', views.clients, name = 'clients'),
    path('affilations/', views.affilations, name = 'affilations'),
    path('privacy/', views.privacy, name = 'privacy'),
    path('terms/', views.terms, name = 'terms'),
    path('support/', views.support, name = 'support'),
    path('faq/', views.faq, name = 'faq'),
    path('testimonial/', views.testimonial, name = 'testimonial'),
    path('newsletter/', views.newsletter, name = 'newsletter'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    
    
    #redirects
    path('<str:old_url>/', views.handle_redirect, name='redirect_handler'),
    #end redirects
    
]