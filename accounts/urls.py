from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('register', views.register, name='register'),
    path('signout', views.signout, name='signout'),
    path('updateProfile', views.UpdateProfile.as_view(), name='update_profile'),
]
