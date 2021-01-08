from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator

class BookInfo(models.Model):
    quantity = models.IntegerField(validators=[MaxValueValidator(9999)], help_text='Enter Book Quantity', null= False)
    price = models.IntegerField(validators=[MaxValueValidator(9999999999999)],help_text='Enter Price of the Book', null= False)

    def __str__(self):
        return str(self.quantity)
        

class Book(models.Model):
    isbn = models.IntegerField(validators=[MaxValueValidator(9999999999999)],help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    seller = models.ForeignKey(User, related_name='mybooks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text='Enter Book Title', null= False)
    author = models.CharField(max_length=50,help_text='Enter Author', null= False)
    publisher = models.CharField(max_length=50,help_text='Enter Publisher', null= False)
    publication_date = models.DateField(null=True, blank=True,help_text='YYYY-MM-D')
    quantity_and_price = models.ForeignKey(BookInfo, related_name='mybookinfo', on_delete=models.CASCADE, default=1)
    cover_page = models.ImageField()

    def __str__(self):
        return self.title
    



