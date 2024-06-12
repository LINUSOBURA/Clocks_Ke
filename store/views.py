import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import LoginForm, ProductForm, SignupForm
from .models import *

# Create your views here


def store(request):
    """
    Renders the store page for the user. If the user is authenticated, retrieves their order and its items. If not,
    initializes an empty order and items list. Retrieves the three most recently created products and passes them to
    the store template along with the order and items.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered store page with the trending products, order, and items.
    """
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,
                                                         complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
    except:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    trending_products = Product.objects.order_by('-created_at')[:3]

    context = {
        'trending_products': trending_products,
        'items': items,
        'order': order
    }
    return render(request, 'store/store.html', context)


def shop(request):
    """
    Retrieves all products from the database and renders the 'store/shop.html' template with the retrieved products.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered 'store/shop.html' template with the retrieved products.
    """
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/shop.html', context)


def product(request, product_id):
    """
    Retrieves a specific product from the database based on the provided product_id.
    If the user is authenticated, retrieves the user's order and its items.
    If the user is not authenticated, initializes an empty order and items list.
    Renders the 'store/product.html' template with the retrieved product, items, and order.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - product_id (int): The ID of the product to retrieve.

    Returns:
    - HttpResponse: The rendered 'store/product.html' template with the retrieved product, items, and order.
    """
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,
                                                         complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
    except:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'product': product, 'items': items, 'order': order}
    return render(request, 'store/product.html', context)


def cart(request):
    """
    Retrieves the user's cart items and order information. If the user is authenticated, retrieves their order and its items. If not, initializes an empty order and items list. Renders the 'store/cart.html' template with the items and order.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered 'store/cart.html' template with the items and order.
    """

    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,
                                                         complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
    except:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    """
    Retrieves the user's cart items and order information. If the user is authenticated, retrieves their order and its items. If not, initializes an empty order and items list. Renders the 'store/checkout.html' template with the items and order.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered 'store/checkout.html' template with the items and order.
    """
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer,
                                                         complete=False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
    except:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


# Signup page
def user_signup(request):
    """
    Handles the user signup process.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered 'store/signup.html' template with the signup form.

    This function handles the user signup process. It checks if the request method is POST. If it is, it creates a SignupForm instance with the data from the request. If the form is valid, it saves the form data and displays a success message. If the form is not valid, it displays error messages for each field with errors. If the request method is not POST, it creates an empty SignupForm instance. Finally, it renders the 'store/signup.html' template with the signup form.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = SignupForm()

    return render(request, 'store/signup.html', {'form': form})


# Login page
def user_login(request):
    """
    Handles the user login process.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered 'store/login.html' template with the login form.

    This function handles the user login process. It checks if the request method is POST. If it is, it creates a LoginForm instance with the data from the request. If the form is valid, it authenticates the user with the provided email and password, and if successful, logs the user in and redirects to the 'store' page. If the form is not valid, it displays error messages for each field with errors. If the request method is not POST, it creates an empty LoginForm instance. Finally, it renders the 'store/login.html' template with the login form.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('store')
            else:
                messages.error(request, 'Invalid email or password')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")
                print(form.error_messages)

    else:
        form = LoginForm()

    return render(request, 'store/login.html', {'form': form})


# Logout page
def user_logout(request):
    """
    Logs out the user from the current session and redirects them to the login page.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponseRedirect: A redirect to the 'login' page.

    This function logs out the user from the current session by calling the `logout` function with the `request` object as an argument. It then redirects the user to the 'login' page using the `redirect` function.

    Note:
    - This function assumes that the user is already authenticated.
    - The 'login' page is assumed to have a URL named 'login'.
    """
    logout(request)
    return redirect('login')


# Add to Cart functionality
def UpdateItem(request):
    """
    Update the quantity of an item in the user's cart based on the given action.

    Parameters:
    - request (HttpRequest): The HTTP request object containing the JSON data.

    Returns:
    - JsonResponse: A JSON response indicating whether the item was successfully added or removed from the cart.

    This function retrieves the product ID and action from the JSON data in the request body. It then retrieves the customer object from the authenticated user, and the product object with the given product ID. 

    The function creates or retrieves the order object associated with the customer and sets the `complete` flag to False. It also creates or retrieves the order item object associated with the order and the product.

    Depending on the action, the function increments or decrements the quantity of the order item. If the quantity becomes less than or equal to 0, the order item is deleted.

    The function saves the changes to the order item and returns a JSON response indicating that the item was added to the cart.

    Note:
    - This function assumes that the request object contains valid JSON data.
    - The function assumes that the authenticated user has a valid customer object.
    - The function assumes that the product with the given ID exists in the database.
    - The function assumes that the order and order item objects have been created or retrieved successfully.
    """
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,
                                                 complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,
                                                         product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    """
    Process the order based on the given request.

    Parameters:
    - request (HttpRequest): The HTTP request object containing the order data.

    Returns:
    - JsonResponse: A JSON response indicating the status of the order processing.

    This function processes the order based on the given request. It first retrieves the order data from the request body and loads it as JSON. If the user is authenticated, it retrieves the customer object associated with the user. It then either creates a new order or retrieves an existing order that is not yet complete, associated with the customer. The function calculates the total value of the order from the data and checks if it matches the cart total of the order. If they match, the order is marked as complete. The order is then saved.

    Additionally, a new shipping address is created using the customer, order, and shipping data from the request. The shipping address is associated with the customer and order, and the address, city, state, district, and phone number are extracted from the shipping data.

    If the user is not authenticated, the function redirects to the login page.

    Finally, a JSON response is returned indicating the status of the order processing.

    Note:
    - This function assumes that the request object contains valid JSON data.
    - The function assumes that the authenticated user has a valid customer object.
    - The function assumes that the order and shipping address objects are created or retrieved successfully.
    """
    print('Data:', request.body)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)
        total = float(data['form']['total'])

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(customer=customer,
                                       order=order,
                                       address=data['shipping']['address'],
                                       city=data['shipping']['city'],
                                       state=data['shipping']['state'],
                                       district=data['shipping']['district'],
                                       phone=data['shipping']['phone'])

    else:
        return redirect('login')
    return JsonResponse('Payment complete', safe=False)


def orderComplete(request):
    """
    Render the 'order_complete.html' template for the order completion page.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered 'order_complete.html' template.
    """
    return render(request, 'store/order_complete.html')


def profile(request):
    """
    Retrieves the user's orders and order items if the user is authenticated. If the user is staff, it calls the
    `allOrders` function to retrieve all orders. Otherwise, it returns a dictionary with the orders and order items.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered 'store/profile.html' template with the orders and order items.
    """
    orders = []
    orderItems = []
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            orders = Order.objects.filter(
                customer=customer, complete=True).order_by('-date_ordered')
            for order in orders:
                orderItems = OrderItem.objects.filter(order=order)
        except Order.DoesNotExist:
            orders = ['No orders yet']
            orderItems = []

    if request.user.is_staff:
        context = allOrders()
    else:
        context = {'orders': orders, 'orderItems': orderItems}
    return render(request, 'store/profile.html', context)


def allOrders():
    """
    Retrieves all completed orders with their corresponding shipping addresses, customer, order items, and order total.

    Returns:
        dict: A dictionary containing a list of dictionaries, each representing an order with its corresponding details.
            The dictionary keys are:
                - 'order' (Order): The order object.
                - 'shipping_address' (ShippingAddress): The shipping address object associated with the order.
                - 'customer' (User): The user object associated with the order.
                - 'orderitems' (QuerySet): The queryset of order items associated with the order.
                - 'order_total' (float): The total value of the order.

    """
    orders_with_shipping = []
    all_orders = Order.objects.filter(complete=True).prefetch_related(
        'shippingaddress_set', 'orderitem_set').order_by('-date_ordered')
    for order in all_orders:
        orderitems = (OrderItem.objects.filter(
            order=order)).order_by('order_id')
        shipping_address = ShippingAddress.objects.filter(order=order).first()
        customer = order.customer.user
        order_date = timezone.localtime(order.date_ordered)
        order_total = sum(item.get_total for item in orderitems)
        orders_with_shipping.append({
            'order': order,
            'shipping_address': shipping_address,
            'customer': customer,
            'orderitems': orderitems,
            'order_total': order_total,
            'order_date': order_date
        })
    context = {
        'orders_with_shipping': orders_with_shipping,
    }
    return (context)


@require_POST
def update_shipping_status(request):
    """
    Updates the shipping status of an order.

    This function is a view that handles a POST request. It expects the request body to contain a JSON object with two keys: 'order_id' and 'shipped'. The 'order_id' key should contain the ID of the order to update, and the 'shipped' key should contain a boolean value indicating whether the order has been shipped or not.

    The function first decodes the request body from bytes to a string and then parses it as JSON. It retrieves the 'order_id' and 'shipped' values from the JSON object.

    The function then tries to retrieve the order with the given 'order_id' from the database. If the order is found, it updates the 'shipped' field of the order object with the value of the 'shipped' parameter. It then saves the changes to the order object.

    If the order is not found, the function returns a JSON response with a 'status' key set to 'error' and a 'message' key set to 'Order not found'.

    If the order is found and the shipping status is successfully updated, the function returns a JSON response with a 'status' key set to 'success'.

    Parameters:
    - request (HttpRequest): The HTTP request object containing the JSON data.

    Returns:
    - JsonResponse: A JSON response indicating the status of the shipping status update. If the update is successful, the response will have the status 'success'. If the update is unsuccessful, the response will have the status 'error' and the message 'Order not found'.
    """
    data = json.loads(request.body.decode('utf-8'))
    order_id = data.get('order_id')
    shipped = data.get('shipped') == True

    print(f'order_id:{order_id} ')
    try:
        order = Order.objects.get(transaction_id=order_id)
        order.shipped = shipped
        order.save()
        return JsonResponse({'status': 'success'})
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Order not found'})


def staff_check(user):
    return user.is_staff


@user_passes_test(staff_check,
                  login_url='login?next=/product/upload/&reason=not_staff')
def product_upload(request):
    """
    Uploads a product if the user is a staff member.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - JsonResponse: A JSON response indicating the status of the upload operation.
      - If the upload is successful, the response will have the status 'success'.
      - If the upload is unsuccessful, the response will have the status 'error' and the form errors.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = ProductForm()
    return render(request, 'store/product_upload.html', {'form': form})


@user_passes_test(staff_check)
def edit_product(request, product_id):
    """
    Edit a product by its ID.

    This view function allows staff users to edit a product by its ID. It first retrieves the product object from the database using the provided product ID. If the request method is POST, it creates a ProductForm instance with the request data and the product instance. If the form is valid, it saves the form and returns a JSON response with the status 'success' and the product ID. If the form is not valid, it returns a JSON response with the status 'error' and the form errors. If the request method is not POST, it creates a ProductForm instance with the product instance and renders the 'store/edit_product.html' template with the form, product, and product ID.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - product_id (int): The ID of the product to be edited.

    Returns:
    - JsonResponse: A JSON response indicating the status of the edit operation.
      - If the edit is successful, the response will have the status 'success' and the product ID.
      - If the edit is unsuccessful, the response will have the status 'error' and the form errors.
    - HttpResponse: The rendered 'store/edit_product.html' template with the form, product, and product ID.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'product_id': product_id
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    else:
        form = ProductForm(instance=product)

    return render(request, 'store/edit_product.html', {
        'form': form,
        'product': product,
        'product_id': product_id
    })


def delete_product(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product = get_object_or_404(Product, id=productId)
    if action == 'delete':
        product.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def search(request):
    """
    Retrieves products from the database based on a search query and returns them as a JSON response.

    Parameters:
    - request (HttpRequest): The HTTP request object containing the search query.

    Returns:
    - JsonResponse: A JSON response containing the search results. Each result is a dictionary with the following keys:
        - id (int): The ID of the product.
        - name (str): The name of the product.

    This function takes a search query from the request object and uses it to filter the Product objects in the database.
    The query is obtained from the 'q' parameter of the request GET parameters.
    The search is performed on the 'name' and 'details' fields of the Product objects.
    The results are then transformed into a list of dictionaries, where each dictionary contains the 'id' and 'name' of a product.
    Finally, the search results are returned as a JSON response.

    Note:
    - The search query is case-insensitive.
    - The 'safe' parameter of the JsonResponse is set to False to allow serializing arbitrary objects.
    """
    query = request.GET.get('q', '')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(details__icontains=query))
    data = [{'id': product.id, 'name': product.name} for product in results]
    return JsonResponse(data, safe=False)
