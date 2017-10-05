from django.test import TestCase, Client
from api.models import Author, Book, Review

class AuthorTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_author(self):
        response = self.client.post(
            '/api/v1/author/create', 
            { 
                'first_name': 'J.K.', 
                'last_name': 'Rowling', 
                'age': 52
            }
        )
        author = Author.objects.get(first_name='J.K.')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(author.first_name, 'J.K.')
        self.assertEqual(author.last_name, 'Rowling')
        self.assertEqual(author.age, 52)

    def test_read_author(self):
        author = Author.objects.create(first_name='Stephen', last_name='King', age=50)
        response = self.client.get('/api/v1/author/' + str(author.pk))
        json = response.json()['result']['fields']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['first_name'], 'Stephen')
        self.assertEqual(json['last_name'], 'King')
        self.assertEqual(json['age'], 50)

    def test_update_author(self):
        author = Author.objects.create(first_name='Mark', last_name='Twain', age=50)
        response = self.client.post(
            '/api/v1/author/' + str(author.pk), 
            {
                'first_name': 'Jennifer', 
                'last_name': 'Fang', 
                'age': 19
            }
        )
        author = Author.objects.get(pk=author.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(author.first_name, 'Jennifer')
        self.assertEqual(author.last_name, 'Fang')
        self.assertEqual(author.age, 19)

    def test_delete_author(self):
        author = Author.objects.create(first_name='Ernest', last_name='Hemmingway', age=50)
        response = self.client.get('/api/v1/author/delete/' + str(author.pk))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(pk=author.pk)

    def test_fails_invalid(self):
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


