"""
URL configuration for ecommerce project.
"""

from django.contrib import admin
from django.urls import path

from store.views import (
    product_list,
    product_detail,
    add_to_cart,
    register,
    user_login,
    user_logout,
    checkout,
    remove_from_cart,
    cart,
    increase_quantity,
    decrease_quantity,
    profile,
    edit_profile,
    toggle_favorite,
    favorites,
)

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path("admin/", admin.site.urls),

    path("products/", product_list),

    path("products/<int:product_id>/", product_detail),

    path("cart/add/<int:product_id>/", add_to_cart),

    path("register/", register),

    path("login/", user_login),

    path("logout/", user_logout),

    path("checkout/", checkout),

    path("cart/remove/<int:product_id>/", remove_from_cart),

    path("cart/", cart, name="cart"),

    path("cart/increase/<int:product_id>/", increase_quantity),

    path("cart/decrease/<int:product_id>/", decrease_quantity),

    path("profile/", profile, name="profile"),

    path("profile/edit/", edit_profile, name="edit_profile"),

    path(
        "favorite/<int:product_id>/",
        toggle_favorite,
        name="toggle_favorite"
    ),

    path(
        "favorites/",
        favorites,
        name="favorites"
    ),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )