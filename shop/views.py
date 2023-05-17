from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Min, Max
from .models import Product, Cart
from django.contrib.auth.decorators import login_required


def index(request):
    products_count = Product.objects.count()
    total_price = Product.objects.aggregate(Sum('price'))['price__sum']
    min_price = Product.objects.aggregate(Min('price'))['price__min']
    max_price = Product.objects.aggregate(Max('price'))['price__max']
    pc_count = Product.objects.filter(type='pc').count()
    laptop_count = Product.objects.filter(type='laptop').count()

    return render(request, 'index.html',
                  {'products_count': products_count,
                   'total_price': total_price,
                   'pc_count': pc_count,
                   'laptop_count': laptop_count,
                   'min_price': min_price,
                   'max_price': max_price})


def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})


def catalog_pc(request):
    products = Product.objects.filter(type='pc')
    return render(request, 'catalog.html', {'products': products})


def catalog_laptop(request):
    products = Product.objects.filter(type='laptop')
    return render(request, 'catalog.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    view_count = request.session.get('product_%s_view_count' % product_id, 0)
    view_count += 1
    request.session['product_%s_view_count' % product_id] = view_count
    product.view_count = view_count
    product.save()
    return render(request, 'product_detail.html', {'product': product})


def search_product(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'search.html', {'products': products, 'query': query})


def account(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
        products = cart.products.all()
        return render(request, 'account.html', {'products': products})
    else:
        return render(request, 'account.html')


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart.products.add(product)
    return redirect('/catalog')


@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart.products.remove(product)
    return redirect('account')


@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    # Можно было сделать модель orders но это
    # не прописано в требованиях
    products = cart.products.all()
    for product in products:
        product.order_count += 1
        product.save()
    cart.products.clear()
    cart.save()
    return render(request, 'account.html')
