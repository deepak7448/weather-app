from django.urls import path
from django.conf.urls import include, url
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.weather, name="weather"),
    path('current/', views.current, name="current"),
    path('forecast/', views.forecast, name="forecast"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('oauth/', include('social_django.urls', namespace="socail")),
    # path('login/', auth_views.MyView.as_view()),


]
