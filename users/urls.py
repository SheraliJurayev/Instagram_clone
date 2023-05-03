from .serializers import SignUpSerializer
from .views import CreateUserView
from django.urls import path

urlpatterns = [
    path('signup/' ,  CreateUserView.as_view() , name = 'signup'),
]