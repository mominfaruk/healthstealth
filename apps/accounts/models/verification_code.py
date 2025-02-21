from apps.gist.models.key import Key
from apps.gist.models.activity import Activity
from apps.gist.models.timelog import TimeLog
from apps.accounts.models.users import User
from datetime import timedelta, timezone
from django.db import models

class VerificationCode(Key, Activity, TimeLog):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_verification_code = models.CharField(
        max_length=6, 
        blank=True, 
        null=True,
        help_text="Verification code sent to the user's email."
    )
    phone_verification_code = models.CharField(
        max_length=6, 
        blank=True, 
        null=True,
        help_text="Verification code sent to the user's phone."
    )
    email_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the user's email has been verified."
    )
    phone_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the user's phone has been verified."
    )
    email_verification_code_expiry = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Expiry date and time of the email verification code."
    )
    phone_verification_code_expiry = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Expiry date and time of the phone verification code."
    )
    email_verification_code_attempts = models.IntegerField(
        default=0,
        help_text="Number of email verification code attempts."
    )
    phone_verification_code_attempts = models.IntegerField(
        default=0,
        help_text="Number of phone verification code attempts."
    )
    email_verification_code_last_sent = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Date and time the last email verification code was sent."
    )
    phone_verification_code_last_sent = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Date and time the last phone verification code was sent."
    )


    class Meta:
        verbose_name = "Verification Code"
        verbose_name_plural = "Verification Codes"
        db_table = "verification_codes"
    
    def __str__(self):
        return f"{self.user.email} - {self.email_verification_code}"
    
    def is_email_verification_code_expired(self):
        return self.email_verification_code_expiry < timezone.now()
    
    def is_phone_verification_code_expired(self):
        return self.phone_verification_code_expiry < timezone.now()
    
    def increment_email_verification_code_attempts(self):
        self.email_verification_code_attempts += 1
        self.save()

    def increment_phone_verification_code_attempts(self):
        self.phone_verification_code_attempts += 1
        self.save()

    def reset_email_verification_code_attempts(self):
        self.email_verification_code_attempts = 0
        self.save()

    def reset_phone_verification_code_attempts(self):
        self.phone_verification_code_attempts = 0
        self.save()

    def set_email_verification_code_expiry(self):
        self.email_verification_code_expiry = timezone.now() + timedelta(minutes=15)
        self.save()

    def set_phone_verification_code_expiry(self):
        self.phone_verification_code_expiry = timezone.now() + timedelta(minutes=15)
        self.save()

    def set_email_verification_code_last_sent(self):
        self.email_verification_code_last_sent = timezone.now()
        self.save()

    def set_phone_verification_code_last_sent(self):
        self.phone_verification_code_last_sent = timezone.now()
        self.save()

    