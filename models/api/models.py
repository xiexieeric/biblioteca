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
	pub_date = models.DateField(auto_now_add=True)
	rating = models.FloatField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % (self.title)

class Review(models.Model):
	reviewer = models.ForeignKey(User)
	pub_date = models.DateTimeField('date published')
	book = models.ForeignKey(Book)
	rating = models.IntegerField(default=0)
	content = models.TextField()

	def __str__(self):
		return "%s" % (self.reviewer)
