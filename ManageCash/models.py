
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class AddCash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cash_entries')
    source = models.CharField(max_length=120)
    datetime = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'Added Cash'
        verbose_name_plural = 'Added Cash'

    def __str__(self):
        return f'{self.source} - {self.amount}'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return f'{self.description[:40]} - {self.amount}'
