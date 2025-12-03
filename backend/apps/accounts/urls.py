from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

def logout_view(request):
    logout(request)
    from django.contrib import messages
    messages.success(request, 'Logged out successfully!')
    return redirect('product_list')

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/', include(router.urls)),
]
