from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Product
from .models import Product, Order, OrderItem, Review, Wishlist, Coupon
import razorpay
from django.conf import settings
from django.http import HttpResponse

from reportlab.pdfgen import canvas

def home(request):

    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    categories = Product.objects.values_list(
        'category',
        flat=True
    ).distinct()

    return render(request, 'store/index.html', {
        'products': products,
        'categories': categories
    })

def add_to_cart(request, product_id, quantity):

    cart = request.session.get('cart')

    if not isinstance(cart, dict):
        cart = {}

    product_id = str(product_id)

    if product_id in cart:
       cart[product_id] += quantity
    else:
       cart[product_id] = quantity

    request.session['cart'] = cart

    return redirect('home')

def cart(request):

    cart = request.session.get('cart', {})

    products = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        product.quantity = quantity

        product.subtotal = product.price * quantity

        total += product.subtotal

        products.append(product)

    discount = request.session.get(
        'discount',
        0
    )

    final_total = total - discount

    if final_total < 0:
        final_total = 0

    return render(request, 'store/cart.html', {

        'products': products,

        'total': total,

        'discount': discount,

        'final_total': final_total
    })

def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)

    reviews = Review.objects.filter(
        product=product
    ).order_by('-created_at')

    return render(request, 'store/product_detail.html', {

        'product': product,

        'reviews': reviews
    })

def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def signup(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(request, 'store/signup.html', {
        'form': form
    })
def checkout(request):

    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'GET':

        return render(
            request,
            'store/checkout.html'
        )

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    total = 0

    full_name = request.POST.get('full_name')

    phone = request.POST.get('phone')

    address = request.POST.get('address')

    city = request.POST.get('city')

    pincode = request.POST.get('pincode')

    order = Order.objects.create(

        user=request.user,

        full_name=full_name,

        phone=phone,

        address=address,

        city=city,

        pincode=pincode,

        total_price=0
    )

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        product.stock -= quantity
        product.save()

    order.total_price = total
    order.save()

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        'amount': int(total * 100),
        'currency': 'INR',
        'payment_capture': '1'
    })

    request.session['cart'] = {}

    return render(request, 'store/payment.html', {
        'payment': payment,
        'total': total,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })
def orders(request):

    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'store/orders.html', {
        'orders': orders
    })
def payment_success(request):

    return render(request, 'store/payment_success.html')

def add_review(request, product_id):

    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':

        product = Product.objects.get(id=product_id)

        rating = request.POST.get('rating')

        comment = request.POST.get('comment')

        Review.objects.create(

            product=product,

            user=request.user,

            rating=rating,

            comment=comment
        )

    return redirect('product_detail', product_id=product_id)

def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(

        user=request.user,

        product=product
    )

    return redirect('product_detail', product_id=product_id)

def wishlist(request):

    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(request, 'store/wishlist.html', {

        'wishlist_items': wishlist_items
    })

def apply_coupon(request):

    if request.method == 'POST':

        code = request.POST.get('coupon_code')

        try:

            coupon = Coupon.objects.get(
                code=code,
                active=True
            )

            request.session['discount'] = coupon.discount

        except Coupon.DoesNotExist:

            request.session['discount'] = 0

    return redirect('cart')

def download_invoice(request, order_id):

    order = Order.objects.get(
        id=order_id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="invoice_{order.id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        200,
        800,
        "EliteCart Invoice"
    )

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        750,
        f"Order ID: {order.id}"
    )

    pdf.drawString(
        50,
        730,
        f"Customer: {order.full_name}"
    )

    pdf.drawString(
        50,
        710,
        f"Total: ₹ {order.total_price}"
    )

    y = 650

    pdf.drawString(
        50,
        y,
        "Products:"
    )

    y -= 30

    items = OrderItem.objects.filter(
        order=order
    )

    for item in items:

        pdf.drawString(
            70,
            y,
            f"{item.product.name}  x {item.quantity}"
        )

        y -= 25

    pdf.save()

    return response