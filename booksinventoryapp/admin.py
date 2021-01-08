from django.contrib import admin
from .models import Book, BookInfo


admin.site.register(Book)
admin.site.register(BookInfo)