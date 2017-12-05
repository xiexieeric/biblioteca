from django.db import models


class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)

	def __str__(self):
		return "%s - %s - %s - %s" % (self.username, 
			self.password, self.first_name, self.last_name)


class Authenticator(models.Model):
	authenticator = models.CharField(primary_key = True, max_length=200)
	user_id = models.IntegerField()
	date_created = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return "%s - %s - %s" % (self.authenticator, 
			self.user_id, self.date_created)


class Author(models.Model):
	first_name = models.CharField(max_length = 200)
	last_name = models.CharField(max_length = 200)
	age = models.IntegerField()

	def __str__(self):
		return "%s - %s - %s" % (self.first_name, self.last_name, self.age)


class Book(models.Model):
	title = models.CharField(max_length = 200)
	year_published = models.IntegerField()
	rating = models.FloatField()
	author = models.ForeignKey(Author, on_delete = models.CASCADE)

	def __str__(self):
		return "%s - %s - %s - %s %s" % (self.title, 
			self.year_published, self.rating, self.author.first_name, self.author.last_name)


class Review(models.Model):
	reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
	pub_date = models.DateTimeField(auto_now_add = True)
	book = models.ForeignKey(Book)
	rating = models.FloatField(default = 0)
	content = models.TextField()

	def __str__(self):
		return "%s - %s - %s - %s - %s" % (self.reviewer, 
			self.pub_date, self.book.title, self.rating, self.content)


class Listing(models.Model):
	lister = models.ForeignKey(User, on_delete = models.CASCADE)
	post_date = models.DateTimeField(auto_now_add = True)
	book = models.ForeignKey(Book)
	book_title = models.CharField(max_length=200, default="")
	price = models.FloatField(default = 0)

	def __str__(self):
		return "%s - %s - %s - %s" % (self.lister, 
			self.post_date, self.book.title, self.price)


class Recommendation(models.Model):
	item = models.ForeignKey(Listing, on_delete=models.CASCADE)
	recommended_items = models.TextField()

	def __str__(self):
		return "%s - %s" % (self.item_id, self.recommended_items)

