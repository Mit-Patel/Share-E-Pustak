from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path('',views.index,name="index"),
    path('book_detail/<str:isbn>/',views.book_detail,name="book_detail"),
    path('add_book/',views.add_book,name="add_book"),
]
