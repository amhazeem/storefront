from django.db import models
from django.utils import timezone

from books.models import Book
from shared import optional, TimeStampedModel


class Customer(TimeStampedModel):
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127, default='',**optional)
    email = models.EmailField(**optional)
    phone = models.CharField(max_length=127, default='',**optional)

    def __str__(self):
        return self.first_name

class Rental(TimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rent_history', help_text='Select a book')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    returned_at = models.DateTimeField(**optional)

    @property
    def price(self):
        """
        Calculates the pricing for a book borrowed, per day rental charge is $1
        :return:
        """
        rate = 1
        if not self.returned_at:
            difference = timezone.now() - self.created_at
        else:
            difference = self.returned_at - self.created_at
        days = difference.days + 1
        return days * rate


    def __str__(self):
        return self.book.__str__()

