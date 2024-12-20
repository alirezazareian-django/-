from django.contrib import admin

from .models import Book, Customer, Order
from .models import Comment

admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Order)


