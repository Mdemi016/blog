from django.urls import path
from app. views import *

urlpatterns = [
  path('', Homepage, name="home"),
  path('about', About, name="about"),
  path('hello', hello, name="hello"),
  path('blogs', blogs, name='blogs'),
  path('read/<str:id>',read, name="read"),
  path('delete/<str:id>',delete, name="delete"),
  path('create', create, name= "create"),
  path('edit/<str:id>',edit, name="edit"),
  path('signup',signup, name="signup"),
  path('login',login, name="login"),
  path('logout',logout, name="logout"),
  path('contact', contact, name="contact")
]