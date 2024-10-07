from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('', views.home, name='home'),
    path('create-account/', views.create_account, name='create_account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('remove/<str:pk>/', views.remove_item, name='remove_item'),
    path('wishlist/<str:pk>/', views.wishlist, name='wishlist'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('byebye/', views.byebye, name='byebye'),
    path('login-user/', views.login_user, name='login_user'),

    path('blogs/', views.blogs, name='blogs'),
    path('about-us/', views.about_us, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('blogs/<str:pk>/', views.blogsd, name='blogsd'),
    
    #search
    path('search/', views.product_search, name='product_search'),

    #static page
    path('contact/', views.contact, name='contact'),
    path('returnPolicy/', views.returnPolicy, name='returnPolicy'),
    path('calculate-shipping-cost/', views.calculate_shipping_cost, name='calculate_shipping_cost'),

    path('brouchure/', views.brouchure, name='brouchure'),
    
    path('products/', views.products, name='products'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),


    path('product/<str:pk>/', views.product_list, name='product_list'),
    path('product/<str:pk>/<str:fk>/', views.product_detail, name='product_detail'),
    
] 
