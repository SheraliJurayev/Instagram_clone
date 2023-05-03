from .models import User , UserConfirmation , VIA_EMAIL , VIA_PHONE , NEW , CODE_VERIFIED , DONE , PHOTO_STEP
from rest_framework import exceptions , serializers
from django.db.models import Q
from rest_framework.exceptions import ValidationError



class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer , self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required = False)

    class Meta:
        model = User
        fields = (
            'id', 
            'auth_type',
            'auth_status'
        )

        extra_kwargs = {
            'auth_type': { 'read_only':True , 'required' : False} , 
            'auth_status': { 'read_only':True , 'required' : False} 

        }

    @staticmethod
    def auth_validate(attrs):
        print(attrs)
