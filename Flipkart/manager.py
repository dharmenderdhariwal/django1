from django.contrib.auth.base_user import BaseUsermanager
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class UserManager(BaseUsermanager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    

 