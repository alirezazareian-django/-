from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, CommentForm, ProfileForm, DiscountCodeForm
from .models import Book, Customer, Order, Comment, Profile, Cart, CartItem, DiscountCode
from django.views.generic import CreateView
from .forms import BookForm

class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class HomeView(TemplateView):
    template_name = 'home.html'

class BookListView(ListView):
    model = Book
    template_name = 'accounts/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'accounts/book_detail.html'
    context_object_name = 'book'

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = CommentForm()

    return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'form': form})

class CustomerListView(ListView):
    model = Customer
    template_name = 'accounts/customer_list.html'
    context_object_name = 'Customer'

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'accounts/customer_detail.html'
    context_object_name = 'customer'

class OrderListView(ListView):
    model = Order
    template_name = 'accounts/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'accounts/order_detail.html'
    context_object_name = 'order'

class ProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.book.price * item.quantity for item in cart_items)

        discount_code = request.session.get('discount_code', None)
        discount_value = request.session.get('discount_value', 0)
        discount_type = request.session.get('discount_type', 'fixed')

        if discount_code:
            if discount_type == 'percentage':
                discount_amount = total_price * (discount_value / 100)
            else:
                discount_amount = discount_value
        else:
            discount_amount = 0

        final_price = total_price - discount_amount

        return render(request, 'accounts/cart.html', {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
            'discount_code': discount_code,
            'discount_amount': discount_amount,
            'final_price': final_price,
        })

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        cart_item.quantity += int(request.POST.get('quantity', 1))
        cart_item.save()

        return redirect('cart')

@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect('cart')

class ApplyDiscountCodeView(FormView):
    template_name = 'cart.html'
    form_class = DiscountCodeForm

    def form_valid(self, form):
        discount_code = form.cleaned_data['discount_code']
        try:
            discount = DiscountCode.objects.get(code=discount_code)
            if discount.is_valid():
                self.request.session['discount_code'] = discount_code
                self.request.session['discount_value'] = discount.discount_value
                self.request.session['discount_type'] = discount.discount_type
                messages.success(self.request, f'کد تخفیف "{discount_code}" با موفقیت اعمال شد.')
            else:
                messages.error(self.request, 'کد تخفیف منقضی شده یا غیرقابل استفاده است.')
        except DiscountCode.DoesNotExist:
            messages.error(self.request, 'کد تخفیف وارد شده معتبر نیست.')

        return redirect('cart')
    
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'accounts/add_book.html'
    success_url = reverse_lazy('book_list')  # به صفحه لیست کتاب‌ها هدایت می‌کند
