from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import SignupForm, LoginForm
from .models import Book, Customer, Order
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Comment
from .forms import CommentForm
from django.views.generic import UpdateView
from .models import Profile
from .forms import ProfileForm
from django.views import View
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SignupView(FormView):
    template_name = 'signup.html' 
    form_class = SignupForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        user = form.save()  
        login(self.request, user)  
        return super().form_valid(form)

# Login View
class LoginView(FormView):
    template_name = 'registration/login.html' 
    form_class = LoginForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        login(self.request, form.get_user())  
        return super().form_valid(form)

# Dashboard View
class DashboardView(TemplateView):
    template_name = 'dashboard.html'  


class HomeView(TemplateView):
    template_name = 'home.html'  

class BookListView(ListView):
    model=Book
    template_name='accounts/book_list.html'
    context_object_name='books'

class BookDetailView(DetailView):
    model=Book
    template_name='accounts/book_detail.html'
    context_object_name = 'book'
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.comments.all()  # گرفتن نظرات مرتبط با کتاب
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # اضافه کردن کاربر
            comment.book = book  # اضافه کردن کتاب مرتبط
            comment.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = CommentForm()

    return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'form': form})   

class CustomerListView(ListView):
    model=Customer
    template_name='accounts/customer_list.html'
    context_object_name='Customer'

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'accounts/customer_detail.html'
    context_object_name = 'customer'

# برای نمایش لیست سفارش‌ها
class OrderListView(ListView):
    model = Order
    template_name = 'accounts/order_list.html'
    context_object_name = 'orders'

# برای نمایش جزئیات یک سفارش
class OrderDetailView(DetailView):
    model = Order
    template_name = 'accounts/order_detail.html'
    context_object_name = 'order'   




class ProfileView(UpdateView):
    model=Profile
    form_class=ProfileForm
    template_name='accounts/profile.html'
    success_url=reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile  # دریافت پروفایل کاربر جاری

@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'accounts/cart.html', {'cart': cart})

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, book_id):  
        book = get_object_or_404(Book, id=book_id)  
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Add item to cart or update quantity
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)  # تغییر product به book
        cart_item.quantity += int(request.POST.get('quantity', 1))
        cart_item.save()

        return redirect('cart')

@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect('cart')


    





