import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, SignupForm
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
            orders = Order.objects.filter(customer=customer, complete=True)
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
        'shippingaddress_set', 'orderitem_set')
    for order in all_orders:
        orderitems = OrderItem.objects.filter(order=order)
        shipping_address = ShippingAddress.objects.filter(order=order).first()
        customer = order.customer.user
        order_total = sum(item.get_total for item in orderitems)
        orders_with_shipping.append({
            'order': order,
            'shipping_address': shipping_address,
            'customer': customer,
            'orderitems': orderitems,
            'order_total': order_total
        })
    context = {
        'orders_with_shipping': orders_with_shipping,
    }
    return (context)
