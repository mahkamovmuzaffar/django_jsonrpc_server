from django.db import models


class CardBIN(models.Model):
    bin = models.CharField(max_length=8, unique=True, db_index=True)
    pc_type = models.CharField(max_length=32)  # e.g., Processing Type Humo, Visa, etc.

    def __str__(self):
        return f"{self.bin} -({self.pc_type})"

    class Meta:
        verbose_name = "Card BIN"
        verbose_name_plural = "Card BINs"
        ordering = ["bin"]
