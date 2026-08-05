from django.contrib import admin
from django.urls import include, path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("register/", views.register_view, name="register"),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
]