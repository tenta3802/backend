from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from group.models import Group

class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None):
        if not user_id:
            raise ValueError('The User id must be set')
        
        user = self.model(user_id=user_id)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, user_id, password):
        superuser = self.create_user(
            user_id=user_id, password=password
            )
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser
           
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "user_id"

     

     