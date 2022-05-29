from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .utils import add_watermark
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    email = models.EmailField(unique=True)
    f_name = models.CharField(max_length=50, verbose_name='Имя')
    l_name = models.CharField(max_length=50, verbose_name='Фамилия')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    longitude = models.FloatField(verbose_name='longitude', default=40.6693)
    latitude = models.FloatField(verbose_name='latitude', default=55.6201)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        if self.avatar:
            add_watermark(self)

    def __str__(self):
        return self.email


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_like')
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='got_like')
