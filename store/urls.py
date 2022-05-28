from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('profile/', views.profile, name='profile'),
    path('product/<int:id>', views.product_view, name='product_view'),
    path('login/',views.loginpage,name='login'),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.logoutuser, name="logout")
]