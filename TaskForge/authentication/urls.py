from django.urls import path
from .views import TokenObtainPairView, TokenRefreshView

from django.urls import path
from .views import login_view , register_view

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
]