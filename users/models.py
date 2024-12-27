from datetime import timezone, timedelta

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from lib.base_model import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractBaseUser):
    phone_number = models.BigIntegerField(unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'


class OTP(BaseModel):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)

    def is_valid(self):
        return timezone.now() < self.created_time + timedelta(minutes=5)

