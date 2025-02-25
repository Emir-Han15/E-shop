from django.db import models
from django.contrib.auth.models import User

class Info(models.Model):
    shop_email = models.EmailField()
    inf_text = models.CharField(max_length=250)
    tel = models.CharField(max_length=150)

class Social_account(models.Model):
    name = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=100)
    url = models.URLField()


class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='category_images/')


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE , related_name='products')
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    discount = models.IntegerField(default=0)
    desc = models.TextField()
    stock = models.BooleanField(default=True)
    weight = models.DecimalField(max_digits=10 , decimal_places=1,null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name 
    @property
    def final_price(self):
        return float(self.price) * (1-(self.discount/100))
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE , related_name='images')
    image = models.ImageField(upload_to='product_images/',null=True)

    def __str__(self):
        return f'Image for {self.product.name} ' 
    

class Cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        total = 0
        for i in self.items.all():
            total += i.total_price
        return total
    
    @property
    def total2_price(self):
        if self.total_price >200:
            return self.total_price
        else:
        
            return self.total_price + 20


class Cartitem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_price(self):
        return self.product.final_price * self.quantity
    
   

class Order(models.Model):

    REGIONS = [
        ('ag','Ag'),
        ('ak','Ak'),
        ('mr','Mr'),
        ('ah','Ah'),
        ('bn','Bn'),
        ('lb','Lb'),
        ('dz','Dz'),
    ]

    ORDER_ST = [
        ('ordered','Ordered'),
        ('pending','Pending'),
        ('sendend','Sendend'),
        ('delivered','Delivered'),
    ]

    PAYMENT = [
        ('card','Card'),
        ('cash','Cash'),
    ]


    cart = models.OneToOneField(Cart , on_delete=models.CASCADE , related_name='order')
    customer_name = models.CharField(max_length=150)
    region = models.CharField(max_length=30 ,choices=REGIONS)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    order_status = models.CharField(max_length=20 , choices=ORDER_ST , default='ordered')
    payment_type = models.CharField(max_length=20 , choices=PAYMENT)
    created_at = models.DateTimeField(auto_now_add=True)
    desc = models.TextField(null=True , blank=True)