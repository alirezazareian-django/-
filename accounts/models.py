from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField()
    description = models.TextField()
    image=models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.book.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # نویسنده نظر
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='comments')  # کتاب مرتبط
    text = models.TextField()  # متن نظر
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ارتباط یک به یک با User
    bio = models.TextField(blank=True, null=True)  # بخش بیوگرافی
    location = models.CharField(max_length=100, blank=True, null=True)  # موقعیت مکانی
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # تصویر پروفایل

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"   

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.quantity} x {self.book.title}"

def get_total_price(self):
    return self.book.price * self.quantity

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)  # کد تخفیف
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')])  # نوع تخفیف
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)  # مقدار تخفیف (درصد یا مبلغ ثابت)
    expiration_date = models.DateTimeField()  # تاریخ انقضای کد تخفیف
    is_active = models.BooleanField(default=True)  # فعال بودن کد تخفیف

    def __str__(self):
        return self.code

    def is_valid(self):
        return self.is_active and self.expiration_date > timezone.now()



    


   
