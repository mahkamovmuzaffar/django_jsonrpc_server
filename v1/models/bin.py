from django.db import models


class CardBIN(models.Model):
    bin = models.CharField(max_length=8, unique=True, db_index=True)
    card_type = models.CharField(max_length=32)  # e.g., Uzcard, Visa, MasterCard, Humo, UnionPay, Cobadged
    processing_type = models.CharField(max_length=32)  # e.g., Uzcard, Visa, etc.
    issuer_bank = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.bin} - {self.card_type} ({self.processing_type})"

    class Meta:
        verbose_name = "Card BIN"
        verbose_name_plural = "Card BINs"
        ordering = ["bin"]
