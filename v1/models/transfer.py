from django.db import models
from v1.models.users import Partner  # Assuming user is a Partner


class Transfer(models.Model):
    user = models.ForeignKey(Partner, on_delete=models.CASCADE)
    ext_id = models.CharField(max_length=128)
    sender = models.CharField(max_length=128)
    receiver = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ext_id')
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfers'

    def __str__(self):
        return f"Transfer {self.ext_id} by {self.user}"
