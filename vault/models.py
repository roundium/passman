from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('Email'), unique=True,
                              error_messages={'unique': _('A user with that email already exists.')})

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Credential(models.Model):
    username_validator = UnicodeUsernameValidator()

    owner = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(_('name'), max_length=150)
    username = models.CharField(_('username'), max_length=254,
                                help_text=_('Required. 254 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator])
    password = models.CharField(_('password'), max_length=128)
    url = models.URLField(_('URL'), blank=True)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    def __str__(self):
        return self.name


class SecureNote(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=150)
    note = models.TextField(_('note'))
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Secure Notes'
