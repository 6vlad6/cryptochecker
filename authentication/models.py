from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    img = models.FileField(upload_to='avatars', null=True, blank=True, verbose_name="Фото профиля")
    username = models.TextField(max_length=1000, unique=True, verbose_name="Имя пользователя")


    def __str__(self):
        return str(self.username)
