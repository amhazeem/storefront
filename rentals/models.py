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
        if not self.lines.filter(returned_at__isnull=False).exists():
            return 0
        total = 0
        for order in self.lines.filter(returned_at__isnull=False):
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

        if not self.returned_at:
            difference = timezone.now() - self.rental.created_at
        else:
            difference = self.returned_at - self.rental.created_at
        # Calculate the rate based on the book type
        days = difference.days + 1
        if self.book.type == Book.BookTypes.FICTION:
            rate = 3
            return days * rate * self.quantity
        else:
            rate = 1.5
            discounted_days = 2 if self.book.type == self.book.BookTypes.REULAR else 3
            days_left = days - discounted_days
            base_amount = 2 if self.book.type == self.book.BookTypes.REULAR else 4.5
            if days_left >= 0:
                return discounted_days * 1 * self.quantity + \
                       (rate * days_left * self.quantity) # Remaining
            else:
                return base_amount


