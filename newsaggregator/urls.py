from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from userauths import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('userauths.urls')),
    path('',include('core.urls')),
    path('login/',views.login, name ='login'),
    path('logout/',auth_views.LogoutView.as_view(),name ='logout'),
    path('auth/',include('social_django.urls',namespace='social')),
    path("",views.home,name='home'),
]
