from django.test import TestCase, Client
from api.models import Author, Book, Review

class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create_author("J.K.", "Rowling", "52")

    def create_author(self):
        response = self.client.post('/author/create', {'first_name': 'J.K.', 'last_name': 'Rowling', 'age': 52})
        self.assertContains(response, 'first_name')
        self.assertContains(response, 'last_name')
        self.assertContains(response, 'age')

    def read_author(self):
        response = self.client.get('/author/1')
        self.assertContains(response, 'first_name')
        self.assertContains(response, 'last_name')
        self.assertContains(response, 'age')

    def update_author(self):
        response = self.client.post('/author/1', {'first_name': 'Jennifer', 'last_name': 'Fang', 'age': 19})
        self.assertContains(response, 'first_name')
        self.assertContains(response, 'last_name')
        self.assertContains(response, 'age')

    def delete_author(self):
        self.client.get('/author/delete/1')
        response = self.client.get('/author/1')
        self.assertEqual(response.status_code, 404)

    def fails_invalid(self):
        response = self.client.get('/author')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass



class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create_author("Harry Potter", 1997, 5.0, 1)

    def create_book(self):
        response = self.client.post('/book/create', {'title': 'Harry Potter', 'year_published': 1997, 'rating': 5.0,
            'author': 1})
        self.assertContains(response, 'title')
        self.assertContains(response, 'year_published')
        self.assertContains(response, 'rating')
        self.assertContains(response, 'author')

    def read_book(self):
        response = self.client.get('/book/1')
        self.assertContains(response, 'title')
        self.assertContains(response, 'year_published')
        self.assertContains(response, 'rating')
        self.assertContains(response, 'author')

    def update_book(self):
        response = self.client.post('/book/1', {'title': 'Harry Potter 2', 'year_published': 2000, 'rating': 3.0,
            'author': 5})
        self.assertContains(response, 'title')
        self.assertContains(response, 'year_published')
        self.assertContains(response, 'rating')
        self.assertContains(response, 'author')

    def delete_book(self):
        self.client.get('/book/delete/1')
        response = self.client.get('/book/1')
        self.assertEqual(response.status_code, 404)

    def fails_invalid(self):
        response = self.client.get('/book')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass



class ReviewTestCase(TestCase):
    def setUp(self):
        Review.objects.create_author("Jennifer Fang", "2017-09-30", 1, 4.0, "This book was great!")

    def create_review(self):
        response = self.client.post('/review/create', {'reviewer': 'Jennifer Fang', 'pub_date': "2017-09-30", 'book': 1,
            'rating': 5.0, 'author': 1})
        self.assertContains(response, 'reviewer')
        self.assertContains(response, 'pub_date')
        self.assertContains(response, 'book')
        self.assertContains(response, 'rating')
        self.assertContains(response, 'content')

    def read_review(self):
        response = self.client.get('/review/1')
        self.assertContains(response, 'reviewer')
        self.assertContains(response, 'pub_date')
        self.assertContains(response, 'book')
        self.assertContains(response, 'rating')
        self.assertContains(response, 'content')

    def update_review(self):
        response = self.client.post('/review/1', {'reviewer': 'Brandon Liu', 'pub_date': "2017-10-01", 'book': 2,
            'rating': 3.0, 'author': 2})
        self.assertContains(response, 'reviewer')
        self.assertContains(response, 'pub_date')
        self.assertContains(response, 'book')
        self.assertContains(response, 'rating')
        self.assertContains(response, 'content')

    def delete_review(self):
        self.client.get('/review/delete/1')
        response = self.client.get('/review/1')
        self.assertEqual(response.status_code, 404)

    def fails_invalid(self):
        response = self.client.get('/review')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass


