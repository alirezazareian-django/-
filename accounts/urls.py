from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignupView, LoginView, DashboardView, HomeView
from . import views
from django.urls import path, include
from .views import ProfileView
from .views import CartView, AddToCartView, RemoveFromCartView


urlpatterns = [
    # Custom Views
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('home/', HomeView.as_view(), name='home'),
   
    path('auth/', include('django.contrib.auth.urls')),

    # لیست کتاب‌ها
    path('books/', views.BookListView.as_view(), name='book_list'),

    # جزئیات کتاب
    path('books/<int:pk>/', views.BookListView.as_view(), name='book_detail'),

     # لیست مشتری‌ها
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
   
    # جزئیات مشتری
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    
    # لیست سفارش‌ها
    path('orders/', views.OrderListView.as_view(), name='order_list'),
   
    # جزئیات سفارش
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    path('profile/', ProfileView.as_view(), name='profile'),

   
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:book_id>/', AddToCartView.as_view(), name='add_to_cart'),  
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]





