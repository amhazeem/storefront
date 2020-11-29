from django.db import models
from django.utils import timezone

from books.models import Book
from shared import optional, TimeStampedModel


class Customer(TimeStampedModel):
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127, default='', **optional)
    email = models.EmailField(**optional)
    phone = models.CharField(max_length=127, default='', **optional)

    def __str__(self):
        return self.first_name


class Rental(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    notes = models.TextField(**optional)

    @property
    def price(self):
        # Gets the price of the entire order using the lines attached
        if not self.lines.exists():
            return 0
        total = 0
        for order in self.lines.all():
            total += order.price
        return total

    def __str__(self):
        return self.customer.__str__()


class RentalLine(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='lines', help_text='Select a book')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rent_history', help_text='Select a book')
    quantity = models.PositiveIntegerField(default=1)
    returned_at = models.DateTimeField(**optional)

    def __str__(self):
        return self.book.__str__()

    @property
    def price(self):
        """
        Calculates the pricing for a book borrowed, per day rental charge is $1
        :return:
        """
        rate = 1
        if not self.returned_at:
            difference = timezone.now() - self.rental.created_at
        else:
            difference = self.returned_at - self.rental.created_at
        days = difference.days + 1
        return days * rate * self.quantity
