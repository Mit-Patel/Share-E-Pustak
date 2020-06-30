from django.urls import path
from django.conf.urls import url
from . import views
from .views import ActivateAccount

app_name = 'authenticate_app'

urlpatterns = [
    path('register/', views.register, name="register"),  
    path('login/', views.user_login, name="user_login"),  
    path('logout/', views.user_logout, name="user_logout"),  
    path('send_otp/', views.send_otp, name="send_otp"),  
    path('verify_otp/', views.verify_otp, name="verify_otp"),  
    path('validate_username/', views.validate_username, name="validate_username"),  
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', ActivateAccount.as_view(), name="activate"),  
]
