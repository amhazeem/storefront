from django.db import models
from django.db.models import Sum

from shared import TimeStampedModel


class Book(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def on_rent(self):
        if self.quantity == 0:
            return 0
        # Check OrderLines
        from rentals.models import Rental
        items = self.rent_history.select_related('rental').filter(returned_at__isnull=True)
        if not items.exists():
            return 0
        sum = items.aggregate(sum=Sum('quantity'))['sum']
        return sum

    @property
    def in_stock(self):
        return self.quantity - self.on_rent
