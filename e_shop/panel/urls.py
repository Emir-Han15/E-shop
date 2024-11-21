from django.urls import path
from panel.views import *

urlpatterns = [
    path('',index_page),
    path('category/',category_list),
    path('category/form/',category_form),
    path('edit-form/<int:pk>',edit_category),
    
    path('delete-form/<int:pk>',delete_category),

    path('product/',product_list),
    path('product/form/',product_form),
    path('edit-product-form/<int:pk>',edit_product),
    
    path('delete-product-form/<int:pk>',delete_product),

    path('ord_list/',order_list),
    path('det_prod/<int:pk>',product_details),
    path('order/<int:pk>',order),



]