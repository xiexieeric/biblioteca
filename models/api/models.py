from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	age = models.IntegerField()

	def __str__(self):
		return "%s - %s - %s" % (self.first_name, self.last_name, self.age)


class Book(models.Model):
	title = models.CharField(max_length=200)
	year_published = models.IntegerField()
	rating = models.FloatField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	def __str__(self):
		return "%s - %s - %s - %s %s" % (self.title, 
			self.year_published, self.rating, self.author.first_name, self.author.last_name)


class Review(models.Model):
	reviewer = models.CharField(max_length=200)
	pub_date = models.CharField(max_length=200)
	book = models.ForeignKey(Book)
	rating = models.FloatField(default=0)
	content = models.TextField()

	def __str__(self):
		return "%s - %s - %s - %s - %s" % (self.reviewer, 
			self.pub_date, self.book.title, self.rating, self.content)
