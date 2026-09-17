from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from .models import Product, Order, OrderItem, Profile, Favorite
from django.contrib.auth.decorators import login_required


def product_list(request):
    category = request.GET.get("category")
    search = request.GET.get("search")

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if search:
        products = products.filter(name__icontains=search)

    categories = Product.objects.values_list(
        "category", flat=True
    ).distinct()

    favorite_product_ids = []

    if request.user.is_authenticated:
        favorite_product_ids = list(
            Favorite.objects.filter(
                user=request.user
            ).values_list("product_id", flat=True)
        )

    return render(request, "products.html", {
        "products": products,
        "categories": categories,
        "search": search,
        "favorite_product_ids": favorite_product_ids,
    })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(request, "product_detail.html", {
        "product": product
    })


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return render(
                request,
                "registration_success.html",
                {"user": user}
            )
    else:
        form = RegistrationForm()

    return render(request, "register.html", {
        "form": form
    })


def user_login(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")
        next_url = request.POST.get("next_url")

        user = authenticate(
            request,
            username=username_or_email,
            password=password
        )

        if user is None:
            try:
                account = User.objects.get(
                    email=username_or_email
                )

                user = authenticate(
                    request,
                    username=account.username,
                    password=password
                )

            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            if next_url:
                return redirect(next_url)

            return render(
                request,
                "login_success.html",
                {"user": user}
            )

        return render(request, "login.html", {
            "error": "Invalid username/email or password.",
            "next_url": next_url,
        })

    return render(request, "login.html")


def user_logout(request):
    logout(request)

    return render(
        request,
        "logout_success.html"
    )

@login_required(login_url="/login/")
def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        return render(request, "cart.html", {
            "cart_items": [],
            "total": 0,
            "error": "Your cart is empty."
        })

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    # Create ONE order for the whole checkout
    order = Order.objects.create(
        user=request.user,
        total_price=0
    )

    order_total = 0

    # Add each product to that order
    for product in products:

        quantity = cart[str(product.id)]

        item_total = product.price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            total_price=item_total
        )

        order_total += item_total

    # Save the total for the complete order
    order.total_price = order_total
    order.save()

    # Empty cart
    request.session["cart"] = {}

    return render(
        request,
        "checkout_success.html"
    )

def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    quantity = int(
        request.GET.get("quantity", 1)
    )

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session["cart"] = cart

    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


def cart(request):
    cart = request.session.get("cart", {})

    if isinstance(cart, list):
        cart = {}
        request.session["cart"] = cart

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []

    for product in products:
        quantity = cart[str(product.id)]

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": product.price * quantity,
        })

    total = sum(
        item["subtotal"]
        for item in cart_items
    )

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


def increase_quantity(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart

    return redirect("cart")


def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")

@login_required(login_url="/login/")
def profile(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )
    return render(request, "profile.html", {
        "profile": profile,
        "user": request.user,
    })


@login_required(login_url="/login/")
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.save()

        profile.name = request.POST.get("name")
        profile.age = request.POST.get("age") or None
        profile.gender = request.POST.get("gender")

        if request.POST.get("remove_profile_picture"):
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)
            profile.profile_picture = None

        elif request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        profile.save()

        return redirect("profile")

    return render(request, "edit_profile.html", {
        "profile": profile,
        "user": request.user,
    })


@login_required(login_url="/login/")
def toggle_favorite(request, product_id):
    product = Product.objects.get(id=product_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        favorite.delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "/products/"
        )
    )

@login_required(login_url="/login/")
def favorites(request):
    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related("product")

    return render(request, "favorites.html", {
        "favorites": favorites,
    })