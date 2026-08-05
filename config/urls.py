from django.contrib import admin
from django.urls import include, path
from allauth.account import views as allauth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Password Reset Views
    path('accounts/password/reset/', 
         allauth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
         name='account_reset_password'),
         
    path('accounts/password/reset/done/', 
         allauth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
         name='account_reset_password_done'),

    # Rest of includes
    path('', include('homepage.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
]