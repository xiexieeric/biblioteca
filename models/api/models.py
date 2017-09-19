from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	age = models.IntegerField()

class Book(models.Model):
	title = models.CharField(max_length=200)
	pub_date = models.DateField()
	rating = models.FloatField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Review(models.Model):
	reviewer = models.ForeignKey(User)
	pub_date = models.DateTimeField('date published')
	book = models.ForeignKey(Book)
	rating = models.IntegerField(default=0)
	content = models.TextField()
