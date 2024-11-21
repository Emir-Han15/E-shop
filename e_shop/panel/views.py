from django.shortcuts import render , redirect
from main.models import *
from panel.models import *
from panel.forms import *
from django.forms import modelformset_factory

ProductImageSet = modelformset_factory(ProductImage , ProductImageForm , extra=5)


def index_page(request):
    return render(request , 'panel/index.html')

def category_list(request):
    cat = Category.objects.all()
    return render(request , 'panel/category-table.html',context={'cat':cat})

def category_form(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/panel/category/')
    return render(request , 'panel/category-form.html',context={'form':form})


def edit_category(request , pk):
    obj = Category.objects.get(id=pk)
    form = CategoryForm(instance=obj)
    if request.method == 'POST':
        form = CategoryForm(request.POST , request.FILES , instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/panel/category/dd')
    return render(request , 'panel/category-form.html',context={'form':form})


def delete_category(request , pk):
    cat = Category.objects.get(id=pk)
    cat.delete()
    return redirect('/panel/category/')

def product_list(request):
    pro = Product.objects.all()
    return render(request , 'panel/product-table.html',context={'pro':pro})

def product_form(request):
    form = ProductForm()
    imageforms = ProductImageSet(queryset=ProductImage.objects.none())
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        imageforms = ProductImageSet(request.POST , request.FILES)
        if form.is_valid():
            pr = form.save()
            if imageforms.is_valid():
                for i_form in imageforms:
                    if i_form.is_valid():
                        if 'image' in i_form.cleaned_data:
                            p_image = i_form.save(commit=False)
                            p_image.product = pr
                            p_image.save()
            return redirect('/panel/product/')
    return render(request , 'panel/product-form.html',context={'form':form , 'imageforms':imageforms})


def edit_product(request , pk):
    obj = Product.objects.get(id=pk)
    form = ProductForm(instance=obj)
    imageforms = ProductImageSet(queryset=ProductImage.objects.all())
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES , instance=obj)
        imageforms = ProductImageSet(request.POST , request.FILES)
        if form.is_valid():
            pro = form.save()
            if imageforms.is_valid():
                for i_form in imageforms:
                        if i_form.is_valid():
                            if 'image' in i_form.cleaned_data:
                                p_image = i_form.save(commit=False)
                                p_image.product = pro
                                p_image.save()

            return redirect('/panel/product/')
    return render(request , 'panel/product-form.html',context={'form':form,'imageforms':imageforms})


def delete_product(request , pk):
    cat = Product.objects.get(id=pk)
    cat.delete()
    return redirect('/panel/product/')




def order_list(request):
    ord = Order.objects.all()
    return render(request , 'panel/order-table.html',context={'ord':ord})

def product_details(request , pk):
    ord = Product.objects.get(id=pk)
    return render(request , 'panel/product_details.html',context={'obj':ord})


def order(request , pk):
    ord = Order.objects.get(id=pk)
    return render(request , 'panel/invoice.html',context={'order':ord})