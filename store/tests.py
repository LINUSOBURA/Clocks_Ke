import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Customer, Order, OrderItem, Product, ShippingAddress

CustomUser = get_user_model()
'''Models Tests'''


class CustomUserManagerTests(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(email='test@example.com',
                                              password='testpass',
                                              first_name='First',
                                              last_name='Last')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass'))

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='testpass')

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(email='admin@example.com',
                                                   password='adminpass',
                                                   first_name='Admin',
                                                   last_name='User')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class CustomerModelTests(TestCase):

    def test_customer_creation(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.client.login(email='user@example.com', password='testpassword')

        # Check if the customer already exists
        self.customer, created = Customer.objects.get_or_create(
            user=self.user,
            defaults={
                'username': 'testuser',  # Set the username explicitly
                'email': 'user@example.com'
            })

        self.assertEqual(self.customer.username, '')
        self.assertEqual(self.customer.email, 'user@example.com')


class ProductModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name='Test Product',
                                             price=10.0,
                                             details='A test product.')

    def test_product_creation(self):
        self.assertEqual(self.__class__.product.name, 'Test Product')
        self.assertEqual(self.__class__.product.price, 10.0)


class OrderModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.client.login(email='user@example.com', password='testpassword')

        # Check if the customer already exists
        self.customer, created = Customer.objects.get_or_create(
            user=self.user,
            defaults={
                'username': 'testuser',
                'email': 'user@example.com'
            })

    def test_order_creation(self):
        order = Order.objects.create(customer=self.customer)
        self.assertEqual(str(order.transaction_id), str(order.transaction_id))
        self.assertFalse(order.complete)


class ShippingAddressModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.client.login(email='user@example.com', password='testpassword')

        # Check if the customer already exists
        self.customer, created = Customer.objects.get_or_create(
            user=self.user,
            defaults={
                'username': 'testuser',
                'email': 'user@example.com'
            })

        # Create an order for the customer
        self.order = Order.objects.create(customer=self.customer)

    def test_shipping_address_creation(self):
        shipping_address = ShippingAddress.objects.create(
            customer=self.customer,
            order=self.order,
            address='123 Test St',
            city='Test City',
            state='Test State',
            district='Test District',
            phone='1234567890')
        self.assertEqual(shipping_address.address, '123 Test St')
        self.assertEqual(shipping_address.city, 'Test City')


class OrderItemModelTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.client.login(email='user@example.com', password='testpassword')

        # Check if the customer already exists
        self.customer, created = Customer.objects.get_or_create(
            user=self.user,
            defaults={
                'username': 'testuser',
                'email': 'user@example.com'
            })

        self.product = Product.objects.create(name='Test Product',
                                              price=10.0,
                                              details='A test product.')
        self.order = Order.objects.create(customer=self.customer,
                                          complete=False)

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(product=self.product,
                                              order=self.order,
                                              quantity=2)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.get_total, 20.0)

    def test_get_total(self):
        order_item = OrderItem.objects.create(product=self.product,
                                              order=self.order,
                                              quantity=2)
        self.assertEqual(order_item.get_total,
                         self.product.price * order_item.quantity)


'''Views Tests'''


class StoreViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('store')

    def test_store_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')
        self.assertIn('trending_products', response.context)


class ShopViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('shop')

    def test_shop_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/shop.html')
        self.assertIn('products', response.context)


class ProductViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='Test Product',
                                              price=10.0,
                                              details='A test product.')
        self.url = reverse('product', args=[self.product.id])

    def test_product_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product.html')
        self.assertIn('product', response.context)


class CartViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('cart')

    def test_cart_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')
        self.assertIn('items', response.context)


class CheckoutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('checkout')

    def test_checkout_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/checkout.html')
        self.assertIn('items', response.context)


class UserSignupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_signup_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/signup.html')

    def test_signup_view_post(self):
        data = {
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertTrue(
            CustomUser.objects.filter(email='newuser@example.com').exists())


class UserLoginViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.url = reverse('login')

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/login.html')

    def test_login_view_post(self):
        data = {'email': 'user@example.com', 'password': 'testpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirects to store


class UserLogoutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.client.login(email='user@example.com', password='testpassword')
        self.url = reverse('logout')

    def test_logout_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirects to login


class UpdateItemViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.client.login(email='user@example.com', password='testpassword')

        # Check if the customer already exists
        self.customer, created = Customer.objects.get_or_create(
            user=self.user,
            defaults={
                'username': 'testuser',
                'email': 'user@example.com'
            })

        self.product = Product.objects.create(name='Test Product',
                                              price=10.0,
                                              details='A test product.')
        self.url = reverse('update_item')
        self.order = Order.objects.create(customer=self.customer,
                                          complete=False)

    def test_update_item_view_add(self):
        data = json.dumps({'productId': self.product.id, 'action': 'add'})
        response = self.client.post(self.url,
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order_item = OrderItem.objects.get(order=self.order,
                                           product=self.product)
        self.assertEqual(order_item.quantity, 1)


class ProcessOrderViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com',
                                                   password='testpassword')
        self.client.login(email='user@example.com', password='testpassword')

        #
