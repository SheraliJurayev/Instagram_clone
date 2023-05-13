from .models import User , UserConfirmation , VIA_EMAIL , VIA_PHONE , NEW , CODE_VERIFIED , DONE , PHOTO_STEP
from rest_framework import exceptions , serializers
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from shared.utility import check_email_or_phone
from shared.utility import send_email


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
            'auth_type': { 'read_only':True , 'required' : False}, 
            'auth_status': { 'read_only':True , 'required' : False} 
        }

    def create(self, validated_data):
        user  = super(SignUpSerializer , self).create(validated_data)
        print(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.mail , code)

        elif  user.auth_type == VIA_PHONE:
            code  = user.create_verify_code(VIA_PHONE)
            # send_phone_code(user.phone_number, code)

        user.save()    
        return user
    def validate(self, data):  
        super(SignUpSerializer , self).validate(data)
        data =self.auth_validate(data)  
        return data

    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('email_phone_number')).lower()
        input_type = check_email_or_phone(user_input)
        if input_type == 'email':
            data = {
                'email' : user_input ,
                'auth_type' : VIA_EMAIL
            }
        elif input_type == 'phone':
             data = {
                'phone_number' : user_input ,
                'auth_type' : VIA_PHONE
            }
             
        else:
            data = {
                'success' : False , 
                'message' : 'You must send email or phone number'
            }
            raise ValidationError(data)
        return data
    
    def validate_email_phone_number(self , value):
        value = value.lower()

        return value


         