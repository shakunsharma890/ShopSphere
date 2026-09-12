from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . models import ProductModel,CartModel,OrderModel
from django.db.models import Q
from django.contrib import messages
# Create your views here.
@login_required
def home(request):
    if request.user.is_authenticated:
        cart_count = CartModel.objects.filter(host = request.user).count()
    else:
        cart_count = 0
    trend = False 
    offer = False
    if 'q' in request.GET:
        q = request.GET['q']
        print("Search query:", repr(q))
        all_products = ProductModel.objects.filter((Q(pname__icontains=q)| Q(pcategory__icontains=q)))
        print("Products found:", all_products.count())
        if len(all_products) == 0:
            messages.error(request,'NO PRODUCTS.....!')
    elif 'cat' in request.GET:
        cat = request.GET['cat']
        all_products = ProductModel.objects.filter(pcategory = cat)
    elif 'offer' in request.GET:
        all_products = ProductModel.objects.filter(Q(offer = True) & Q(is_delete = False))
        offer = True
    elif 'trending' in request.GET:
        all_products = ProductModel.objects.filter(Q(trending = True)& Q(is_delete = False))
        trend = True
    else:
        all_products = ProductModel.objects.all()
    category = []
    for i in ProductModel.objects.all():
        if i.pcategory not in category:
            category.append(i.pcategory)
    print("Products found:", all_products.count())
    for p in all_products:
        print(p.pname)
    return render(request,'home.html',{'all_products':all_products,'category':category,'trend':trend,'offer':offer,'cart_count':cart_count})

@login_required
def product_detail(request, pk):
    product = ProductModel.objects.get(id=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart(request):
    cart_count = CartModel.objects.filter(host = request.user).count()
    cart_product = CartModel.objects.filter(host = request.user)
    TA = 0
    for i in cart_product:
        TA += i.total_price
    return render(request,'cart.html',{'cart_product':cart_product,'TA':TA,'cart_count':cart_count})

@login_required
def add_to_cart(request,pk):
    product = ProductModel.objects.get(id = pk)
    try:
        cp = CartModel.objects.get(pname=product.pname,host = request.user)
        cp.quantity += 1
        cp.total_price += product.price 
        cp.save()
        return redirect('cart')
    except CartModel.DoesNotExist:
        CartModel.objects.create(
            pname = product.pname,
            pcategory =product.pcategory,
            price = product.price,
            total_price = product.price,
            host = request.user
        )
    return redirect('home')

@login_required
def remove(request,pk):
    data = CartModel.objects.get(id = pk,host = request.user).delete()
    return redirect('cart')

@login_required
def plus(request,pk):
    data = CartModel.objects.get(id=pk,host = request.user)
    data.quantity += 1
    data.total_price += data.price
    data.save()
    return redirect('cart')

@login_required
def minus(request,pk):
    data = CartModel.objects.get(id=pk,host = request.user)
    if data.quantity <= 1:
        data.delete()
    else:
        data.quantity -= 1
        data.total_price -= data.price 
        data.save()
    return redirect('cart')


def support(request):
    return render(request,'support.html')


def know_us(request):
    return render(request,'know_us.html')

@login_required
def buy_now(request, pk):
    product = ProductModel.objects.get(id=pk)

    try:
        cp = CartModel.objects.get(
            pname=product.pname,
            host=request.user
        )

        # Product is already in cart
        return redirect('cart')

    except CartModel.DoesNotExist:
        CartModel.objects.create(
            pname=product.pname,
            pcategory=product.pcategory,
            price=product.price,
            total_price=product.price,
            quantity=1,
            host=request.user
        )

        return redirect('cart')

@login_required
def checkout(request):
    cart_product = CartModel.objects.filter(host=request.user)

    TA = 0
    for i in cart_product:
        TA += i.total_price

    return render(
        request,
        'checkout.html',
        {
            'cart_product': cart_product,
            'TA': TA
        }
    )

@login_required
def place_order(request):
    cart_product = CartModel.objects.filter(host=request.user)

    for i in cart_product:
        OrderModel.objects.create(
            pname=i.pname,
            price=i.price,
            quantity=i.quantity,
            total_price=i.total_price,
            host=request.user
        )

    cart_product.delete()

    return redirect('order_success')

@login_required
def order_success(request):
    return render(request, 'order_success.html')