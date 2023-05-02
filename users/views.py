from rest_framework import permissions
from .models import User
from rest_framework.generics import CreateAPIView

class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny)

