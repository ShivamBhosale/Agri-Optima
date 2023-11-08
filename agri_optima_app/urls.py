from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('', views.home, name='home'),
   path('register/', views.registerPage, name='register'),
   path('login/', views.loginPage, name='login'),
   path('logout/', views.logoutUser, name='logout'),
   path('profile/', views.profile, name='profile'),
   path('dummy/', views.dummy, name='dummy'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)