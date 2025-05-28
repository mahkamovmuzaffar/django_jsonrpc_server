# app/models/app_settings.py
from django.db import models


class AppSettings(models.Model):
    TWO_FA_CHOICES = [
        ("none", "None"),
        ("sms", "SMS"),
        ("email", "Email"),
        ("auth_app", "Authenticator App"),
    ]

    enable_admin_firewall = models.BooleanField(default=False)
    two_fa_type = models.CharField(max_length=20, choices=TWO_FA_CHOICES, default="none")

    def __str__(self):
        return "Application Settings"

    class Meta:
        verbose_name = "App Setting"
        verbose_name_plural = "App Settings"
