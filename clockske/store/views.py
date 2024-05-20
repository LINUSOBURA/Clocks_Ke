from django.shortcuts import render

# Create your views here


def store(request):
    context = {}
    return render(request, 'store/store.html', context)


def shop(request):
    context = {}
    return render(request, 'store/shop.html', context)


def product(request):
    context = {}
    return render(request, 'store/product.html', context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)
