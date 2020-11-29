from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from books.models import Book
from rentals.models import Customer, Rental, RentalLine
from shared import get_random_str


def create_customer(first_name, **kwargs):
    return Customer.objects.create(first_name=first_name  + get_random_str(), **kwargs)

def create_book(title="Book 1", description="This is a sample book written by XY", book_type=Book.BookTypes.REULAR):
    return Book.objects.create(title=title + get_random_str(), description=description, type=book_type)

def create_rental(customer=None, books=None, **kwargs):
    if not customer:
        customer = create_customer('Sample Customer')
    if not books:
        books = [create_book()]
    if not isinstance(books,list):
        return
    rental=Rental.objects.create(customer=customer,)

    force_empty_books = kwargs.pop('force_empty_books',None)
    if force_empty_books:
        books = []

    for book in books:
        RentalLine.objects.create(
            rental_id=rental.pk,
            book = book,**kwargs
        )
    rental.refresh_from_db()

    return rental


class CustomerTest(TestCase):

    def test_customer_creation(self):
        obj = create_customer(first_name='Customer')
        self.assertTrue(isinstance(obj, Customer))
        self.assertEqual(obj.__str__(), obj.first_name)


class RentalTest(TestCase):

    def test_rental_creation(self):
        obj = create_rental()
        self.assertTrue(isinstance(obj, Rental))
        self.assertIsInstance(obj.__str__(), str)

    def test_rental_line_creation(self):
        book = create_book(title='Sample Rental Book')
        obj = create_rental(books=[book])
        self.assertTrue(isinstance(obj, Rental))
        self.assertEqual(obj.lines.first().__str__(), book.__str__())

    def test_rental_price_of_returned_regular_book_greater_than_2days(self):
        expected_price = 5
        tomorrow = timezone.now() + timedelta(days=4)
        obj = create_rental(returned_at=tomorrow)
        self.assertTrue(isinstance(obj, Rental))
        self.assertEqual(expected_price, obj.price)

    def test_rental_price_of_returned_regular_book_lesser_than_2days(self):
        expected_price = 2
        tomorrow = timezone.now() + timedelta(days=1)
        obj = create_rental(returned_at=tomorrow)
        self.assertTrue(isinstance(obj, Rental))
        self.assertEqual(expected_price, obj.price)

    def test_rental_price_of_returned_novel_book_lesser_than_3days(self):
        expected_price = 4.5
        tomorrow = timezone.now() + timedelta(days=2)
        book = create_book(book_type=Book.BookTypes.NOVEL)
        obj = create_rental(books=[book], returned_at=tomorrow)
        self.assertTrue(isinstance(obj, Rental))
        self.assertEqual(expected_price, obj.price)

    def test_rental_price_of_returned_novel_book_gte_than_3days(self):
        expected_price = 4.5
        tomorrow = timezone.now() + timedelta(days=4)
        book = create_book(book_type=Book.BookTypes.NOVEL)
        obj = create_rental(books=[book], returned_at=tomorrow)
        self.assertTrue(isinstance(obj, Rental))
        self.assertEqual(expected_price, obj.price)

    def test_rental_price_of_returned_fiction_book(self):
        expected_price = 15
        tomorrow = timezone.now() + timedelta(days=5)
        fiction_book = create_book(book_type=Book.BookTypes.FICTION)
        obj = create_rental(books=[fiction_book],returned_at=tomorrow)
        self.assertTrue(isinstance(obj, Rental))
        self.assertEqual(expected_price, obj.price)

    def test_empty_order_is_zero(self):
        expected_price = 0
        tomorrow = timezone.now() + timedelta(days=5)
        rental = create_rental(returned_at=tomorrow, force_empty_books =True)
        self.assertTrue(isinstance(rental, Rental))
        self.assertEqual(expected_price, rental.price)

