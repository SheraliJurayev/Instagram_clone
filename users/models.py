from django.db import models
from django.core.validators import FileExtensionValidator

from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel

from datetime import datetime , timedelta



ORDINARY_USER , MANAGER , ADMIN = ('ordinary_user', 'manager' , 'admin')
VIA_EMAIL , VIA_PHONE  = ('via_email' , 'via_phone')
NEW , CODE_VERIFIED , DONE ,PHOTO_STEP = ('new', 'code_verified','done' , 'photo_step')

class User(AbstractUser , BaseModel):
    USER_ROLES = (
        (ORDINARY_USER , ORDINARY_USER ) ,
        (MANAGER , MANAGER),
        (ADMIN , ADMIN)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_EMAIL , VIA_EMAIL) ,
        (VIA_PHONE , VIA_PHONE)
    )
    AUTH_STATUS = (
        (NEW , NEW) ,
        (CODE_VERIFIED , CODE_VERIFIED),
        (DONE , DONE),
        (PHOTO_STEP , PHOTO_STEP) 
    )
    user_roles = models.CharField(max_length=31 , choices=USER_ROLES , default=ORDINARY_USER)
    AUTH_TYPE = models.CharField(max_length=31 , choices=AUTH_TYPE_CHOICES)
    AUTH_STATUS = models.CharField(max_length=31 , choices=AUTH_STATUS , default = NEW)
    email = models.EmailField(null=True , unique=True,blank=True)
    phone_number = models.CharField(max_length=13 , null=True , unique=True ,blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True ,blank=True , 
                         validators=FileExtensionValidator(allowed_extensions=['jpg', 'jpeg' ,'png']) , unique=True , blank=True
                               )


    def __str__(self):
        return self.username
    
PHONE_EXPIRE = 2
EMAIL_EXPAIR = 5

class UserConfirmation(BaseModel):
    TYPE_ChOICES = (
        (VIA_PHONE , VIA_PHONE) , 
        (VIA_EMAIL , VIA_EMAIL)
    )
    verify_type = models.CharField(max_length=31 , choices= TYPE_ChOICES)
    code = models.CharField(max_length=4)
    user = models.ForeignKey('users.User', models.CASCADE , related_name = 'verify_code')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user.__str__())
    
    def save(self , *args, **kwargs):
        if not self.pk:
            if self.verify_type == VIA_EMAIL:
                self.expiration_time = datetime.now() + timedelta(minutes = EMAIL_EXPAIR)
            else:
                self.expiration_time = datetime.now() + timedelta(minutes = PHONE_EXPIRE)

        super(UserConfirmation,self).save(*args , **kwargs)


