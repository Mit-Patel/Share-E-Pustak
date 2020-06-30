from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('user_profile/',views.user_profile,name='user_profile'),
    path('about_us/',views.about_us,name='about_us'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('send_request/',views.send_request,name='send_request'),
    path('request_accepted/',views.request_accepted,name='request_accepted'),
]
