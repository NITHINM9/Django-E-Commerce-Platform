from django.http import JsonResponse
import json
from .models import * 
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Customer
from .forms import UserForm 
from .models import Order
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, UserActivity  
from django.views.decorators.csrf import csrf_exempt
from .models import Order, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

def store(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except Customer.DoesNotExist:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)




def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items 
        except Customer.DoesNotExist:
            return redirect('register')  

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()  
        cartItems = order.get_cart_items  
        payment_available = order.get_cart_total > 0 
        shipping_required = order.shipping  

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0  
        payment_available = False 
        shipping_required = False  

    fields_list = ["name", "email", "address", "city", "state", "zipcode", "country"]

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'payment_available': payment_available,
        'fields_list': fields_list,  
        'shipping_required': shipping_required, 
    }
    return render(request, 'store/checkout.html', context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)








def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:  
                    return redirect('admin_dashboard')  
                else:
                    return redirect('store')  
            else:
                error = 'Invalid username or password'
                return render(request, 'login.html', {'form': form, 'error': error})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})




def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')

            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                messages.error(request, "User with this email or username already exists. Please login.")
                return redirect('login')
            else:
                user = form.save()  
                Customer.objects.create(user=user, name=username, email=email)
                messages.success(request, "Registration successful! Please login.")
                return redirect('login') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('store')  



# @staff_member_required
# def admin_dashboard(request):
#     return render(request, 'admin_dashboard.html')




@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    products = Product.objects.all()  
    users = User.objects.all()  
    username = request.user.username 
    user_activities = UserActivity.objects.all().order_by('-login_time')
    for data in user_activities:
        print(data.username)
        
        
    
    
    if request.method == 'POST':
        # Handling Product Management
        if 'create' in request.POST:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product created successfully.")
                return redirect('admin_dashboard')

        elif 'update' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully.")
                return redirect('admin_dashboard')

        elif 'delete' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            messages.success(request, "Product deleted successfully.")
            return redirect('admin_dashboard')

        # Handling User Deletion (not via AJAX)
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, "User deleted successfully.")
            return redirect('admin_dashboard')

    elif request.method == 'GET':
        form = ProductForm()

    # Handling AJAX Requests for User Management
    elif request.method == 'POST' and request.is_ajax():
        data = json.loads(request.body)
        user_id = data.get('user_id')
        username = data.get('username')
        email = data.get('email')
        
        if user_id and username and email:
            user = get_object_or_404(User, id=user_id)
            user.username = username
            user.email = email
            user.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Missing user data.'})
        

    context = {
        'products': products,
        'users': users,  
        'form': ProductForm(),
        'username': username,  
        'user_activities': user_activities,  
    }
    return render(request, 'admin/admin_dashboard.html', context)



class EditProductView(LoginRequiredMixin, View):
    template_name = 'admin/edit_product.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        context = {
            'product': product
        }
        return render(request, self.template_name, context)

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Extract form fields
        product_name = request.POST.get('name')
        product_description = request.POST.get('description')
        product_category = request.POST.get('category')
        product_brand = request.POST.get('brand')
        product_quantity_in_stock = request.POST.get('quantity_in_stock')
        product_is_active = request.POST.get('is_active') == 'on'
        product_image = request.FILES.get('image')

        prices_json = request.POST.get('prices')
        try:
            prices = json.loads(prices_json)  
        except json.JSONDecodeError:
            prices = []


        for price in prices:
            amount = price.get('amount')
            color = price.get('color')
            print(f"Price Amount: {amount}, Color: {color}")


        messages.success(request, "Product updated successfully.")

        return redirect('admin_dashboard')



def pop_up(request):
    form = UserForm()
    # print(request.method)

    if request.method == 'POST':
        # if request.is_ajax():  # Handling AJAX requests
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")  
            user_id = data.get('user_id')
            username = data.get('username')
            email = data.get('email')

            if user_id and username and email:
                print(f"Updating user {user_id} with username: {username} and email: {email}")
                user = get_object_or_404(User, id=user_id)
                user.username = username
                user.email = email
                user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Missing user data.'})
            
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format.'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def user_management(request):
    form = UserForm()
    if 'create' in request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    elif 'update_user' in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    elif 'delete_user' in request.POST:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('user_management')

    users = User.objects.all() 
    return render(request, 'store/user_management.html', {'users': users, 'form': form})






def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UserForm(instance=user)
    return render(request, 'store/user_edit.html', {'form': form, 'user': user})



def logout_view(request):
    if request.user.is_authenticated:
        logout(request) 
    return redirect('login')  





@csrf_exempt
def processOrder(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

    try:
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == order.get_cart_total:
                order.complete = True
            else:
                return JsonResponse({'error': 'Order total does not match.'}, status=400)

            order.save()

            if order.shipping:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                    country=data['shipping']['country'],  
                )

            return JsonResponse({'message': 'Order processed successfully.'}, status=200)

        else:
            return JsonResponse({'error': 'User must be logged in to process the order.'}, status=403)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except Exception as e:
        print(f'Error processing order: {e}')
        return JsonResponse({'error': 'An error occurred while processing your order. Please try again.'}, status=500)









