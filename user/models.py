from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UsersManager(BaseUserManager):

    def create_user(self, id, name, type, password=None):
        user = self.model(id=id, name=name, type=type)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, id, name, type, password):
        user = self.create_user(id, password=passowrd)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
	
    id = models.CharField(max_length=11, primary_key=True, unique=True)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UsersManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name', 'type']

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.id
    
    def get_short_name(self):
        return self.id
