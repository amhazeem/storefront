from django.test import TestCase

from books.models import Book


class BookTest(TestCase):

    def create_book(self, title="Book 1", description="This is a sample book written by XY"):
        return Book.objects.create(title=title, description=description)

    def test_book_creation(self):
        book = self.create_book()
        self.assertTrue(isinstance(book, Book))
        self.assertEqual(book.__str__(), book.title)

