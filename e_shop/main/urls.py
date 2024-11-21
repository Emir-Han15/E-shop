from django.urls import path
from main.views import *

urlpatterns = [
    path('',index_page),
    path('category/<int:pk>/',category),
    path('login/',login_page),
    path('cart/',cart),
    path('add_to_cart/<int:pk>',add_to_cart),
    path('register/',register_page),
    path('logout/',logout_page),
    path('det_prod/<int:pk>/',detail),
    path('delete_cart_item/<int:pk>/',delete_cart_item),
    path('checkout/',checkout),
    path('save_ord/',save_order),
]