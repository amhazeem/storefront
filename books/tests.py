from django.test import TestCase

from books.models import Book
from rentals.tests import create_rental


class BookTest(TestCase):

    def create_book(self, title="Book 1", description="This is a sample book written by XY", **kwargs):
        return Book.objects.create(title=title, description=description, **kwargs)

    def test_book_creation(self):
        book = self.create_book(quantity=10)
        self.assertTrue(isinstance(book, Book))
        self.assertEqual(book.__str__(), book.title)
        self.assertEqual(book.quantity, 10)

    def test_book_in_stock_is_valid(self):
        book = self.create_book(quantity=10)
        # We need to create orders
        create_rental(books=[book])
        book.refresh_from_db()
        self.assertEqual(book.in_stock, 9)
        book = self.create_book(quantity=10)
        # We need to create orders
        book.refresh_from_db()
        self.assertEqual(book.in_stock, 10)

    def test_book_detects_empty_stock(self):
        book = self.create_book(quantity=0)
        # We need to create orders
        self.assertEqual(book.in_stock, 0)

