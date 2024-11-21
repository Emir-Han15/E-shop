from django.shortcuts import render,redirect
from main.models import *
from main.forms import *
from django.contrib.auth import authenticate , login , logout
from django.core.paginator import Paginator

def index_page(request):
    all_cat = Category.objects.all()
    info = Info.objects.first()
    s_accounts = Social_account.objects.all()
    product = Product.objects.all()
    lastest = Product.objects.all().order_by('-created_at')[0:3]
    context={'all_cat':all_cat,
             'info':info,
             's_accounts':s_accounts,
             'product':product,
             'lastest':lastest}
    return render(request , 'main/index.html',context)


def category(request , pk):
    

    min_val = request.GET.get('min_val') or 0
    max_val = request.GET.get('max_val')

    cat = Category.objects.get(id=pk)
    all_cat = Category.objects.all()
    cat_pro = Product.objects.filter(category=cat)
    if cat_pro:
        min_price = int(cat_pro.order_by('price')[0].final_price)
        max_price = int(cat_pro.order_by('-price')[0].final_price)+1

    else:
        min_price , max_price = 0,0

    cat_pro_disc = Product.objects.filter(category=cat , discount__gt = 0) 

    lastest = Product.objects.filter(category=cat).order_by('-created_at')[0:3]

    if max_val:
        a = int(min_val.replace('$',''))
        b = int(max_val.replace('$',''))

        cat_pro = cat_pro.filter(price__range=(a,b))


    ord_val = request.GET.get('order_val') or None


    if ord_val:
        if ord_val=='0':
            cat_pro = cat_pro.order_by('id')
        if ord_val=='1':
            cat_pro = cat_pro.order_by('name')
        if ord_val=='2':
            cat_pro = cat_pro.order_by('-name')
        if ord_val=='3':
            cat_pro = cat_pro.order_by('price')
        if ord_val=='4':
            cat_pro = cat_pro.order_by('-price')

    pagin = Paginator(cat_pro,10)
    p_n = request.GET.get('page',1)
    page_obj = pagin.get_page(p_n)

    
    context = {
        'cat_pro':page_obj,
        'cat_pro_disc':cat_pro_disc,
        'all_cat':all_cat,
        'min_price':min_price,
        'max_price':max_price,
        'cat':cat,
        'lastest':lastest
        
    }

    return render(request,'main/shop-grid.html',context)



def login_page(request):
    form = LoginForm(request)
    if request.method == 'POST':
        form = LoginForm(request , request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            p = form.cleaned_data.get('password')
            user = authenticate(username=uname , password=p)

            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return redirect('/register/')
    return render(request, 'main/login.html',context={'form':form})

def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/')
    return render(request, 'main/register.html',context={'form':form})

def logout_page(request):
    logout(request)
    return redirect('/register/')




def detail(request , pk):
    det_prod = Product.objects.get(id=pk)
    related_pro = Product.objects.filter(category=det_prod.category)
    related_pro = related_pro.exclude(id=det_prod.id)
    return render(request, 'main/shop-details.html',context={'det_prod':det_prod,'related_pro':related_pro})




def cart(request):
    return render(request, 'main/shoping-cart.html')


def add_to_cart(request,pk):
    pro = Product.objects.get(id=pk)
    cart , created = Cart.objects.get_or_create(user=request.user , is_ordered = False)

    cart_item ,created = Cartitem.objects.get_or_create(cart = cart , product = pro)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('/')

def delete_cart_item(request , pk):
    cart_item = Cartitem.objects.get(id=pk)
    cart_item.delete()
    return redirect('/cart/')


def checkout(request):
    form = OrderForm()

    return render(request , 'main/checkout.html',context={'form':form})



def save_order(request):
    cart , created = Cart.objects.get_or_create(user = request.user , is_ordered = False)
    form = OrderForm(request.POST)
    if form.is_valid():
        order = form.save(commit=False)
        order.cart = cart
        order.save()
        cart.is_ordered = True
        cart.save()
        return redirect('/')
    return render(request , 'main/checkout.html',context={'form':form})
        