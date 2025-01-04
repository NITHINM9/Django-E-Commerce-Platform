from django.urls import path
from . import views
from .views import EditProductView



urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),  
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'), 
    path('product/edit/<int:product_id>/',EditProductView.as_view(), name='edit_product'), 
    path('users/', views.user_management, name='user_management'),
    path('pop_up/', views.pop_up, name='pop_up'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('checkout/process/', views.processOrder, name='checkout_process'),
  
]





