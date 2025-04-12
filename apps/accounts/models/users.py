import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.accounts.enums.user_role import UserRole
from apps.gist.models.activity import Activity
from apps.gist.models.key import Key
from apps.gist.models.activity import Activity
from apps.gist.models.timelog import TimeLog

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("userRole", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, Key, Activity, TimeLog):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255, blank=True, null=True)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    gender = models.CharField(max_length=255, blank=True, null=True)
    userRole = models.CharField(max_length=255, choices=[(tag.value, tag.value) for tag in UserRole], default="patient")
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    isBanned = models.BooleanField(default=False)
    banReason = models.TextField(blank=True, null=True)
    limitedBan = models.BooleanField(default=False)
    limitedBanTime = models.DateTimeField(blank=True, null=True)
    lastLoginTime = models.DateTimeField(blank=True, null=True)
    isOnline = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.email
