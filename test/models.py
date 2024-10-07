from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from zirconiaguys.getusername import *
import uuid 
from django.contrib.auth.models import User


class Profile(models.Model):
    active = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return str(self.name)
        
# Create your models here.
class ProductCategory(models.Model):
    
    name = models.CharField(max_length= 200)
    logo = models.ImageField(upload_to='Images')
    slug = models.CharField(max_length= 200)
    site_title = models.CharField(max_length= 200)
    meta_description = models.CharField(max_length= 1200)
    cannoical_url = models.CharField(max_length= 200)
    description =RichTextUploadingField()
    order = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.name)
    
    def product(self):
        return Product.objects.filter(product_category=self.id)

class Shade(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.name)    
    
 
class System(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return str(self.name)    
        

class Colour(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.name)    
        
class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory,  on_delete=models.CASCADE)
    name = models.CharField(max_length= 200)
    image = models.ImageField(upload_to='Images',blank=True, null=True)
    # image_one = models.ImageField(upload_to='Images',blank=True, null=True)
    # image_two = models.ImageField(upload_to='Images',blank=True, null=True)
    # image_three = models.ImageField(upload_to='Images',blank=True, null=True)
    # image_four = models.ImageField(upload_to='Images',blank=True, null=True)
    
    slug = models.CharField(max_length= 200)
    site_title = models.CharField(max_length= 200)
    meta_description = models.CharField(max_length= 1200)
    cannoical_url = models.CharField(max_length= 200)
    description =RichTextUploadingField()
    listcile =RichTextUploadingField()
    


    weight_in_lbs = models.IntegerField(default=20)
    height_in_inch = models.IntegerField(default=4)
    lenght_in_inch = models.IntegerField(default=4)
    width_in_inch = models.IntegerField(default=4)

    select_shade = models.ManyToManyField(Shade, blank=True, null=True, related_name="Shade" )
    select_system = models.ManyToManyField(System, blank=True, null=True, related_name="System" )
    select_colour = models.ManyToManyField(Colour, blank=True, null=True, related_name="Colour" )
    
    element1 = models.CharField(max_length= 200, blank=True, null=True)
    element2 = models.CharField(max_length= 200, blank=True, null=True)
    element3 = models.CharField(max_length= 200, blank=True, null=True)
    element4 = models.CharField(max_length= 200, blank=True, null=True)
    sku = models.CharField(max_length= 200)
    single_price = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)
    out_of_stock = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    sale1 = models.BooleanField(default=False)
    sale2 = models.BooleanField(default=False)
    
    bestseller=models.BooleanField(default=False)
    
    def getprice(self):
        return Price.objects.filter(product=self.id)
    
    def images(self):
        return ProductImage.objects.filter(product=self.id)
    
    def incart(self):
        user = get_request().user
        user = User.objects.get(username=user)
        return Cart.objects.filter(product=self.id, user=user)
    
    def inwishlist(self):
        user = get_request().user
        user = User.objects.get(username=user)
        return Wishlist.objects.filter(product=self.id, user=user)

    def __str__(self):
        return str(self.name)




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images')
    zoom_image = models.ImageField(upload_to='Images')
    def __str__(self):
        return str(self.product)
    
class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Price_Product")
    mm = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()
        
    def __str__(self):
        return str(self.product.name + "- mm " + str(self.mm))


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
     

    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Cart_User")
    qty = models.IntegerField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name="Cart_Price")
    shade = models.CharField(max_length=20, null=True,default='')
    shipping_cost = models.CharField(max_length=20, null=True)
    total_price_with_shipping = models.CharField(max_length=20, null=True)
    def amount(self):
        amount = int(self.qty)*int(self.price.price)
        return amount
    




class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10.00 means 10% off
    active = models.BooleanField(default=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.code
    
class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30)
    first_name = models.CharField(max_length=310)
    last_name = models.CharField(max_length=310)
    company_name = models.CharField(max_length=310,blank=True, null=True)
    address = models.CharField(max_length=300)
    appartment_no  = models.CharField(max_length=130)
    city = models.CharField(max_length=130)
    zip_code = models.CharField(max_length=130)
    country = models.CharField(max_length=1100, default='INDIA')
    phone_number= models.CharField(max_length=101)
    
    ship_somewhere_else= models.BooleanField(default=False)
    shipping_first_name = models.CharField(max_length=310, blank=True, null=True)
    shipping_last_name = models.CharField(max_length=310, blank=True, null=True)
    shipping_company_name = models.CharField(max_length=310,blank=True, null=True)
    shipping_address = models.CharField(max_length=300, blank=True, null=True)
    shipping_appartment_no  = models.CharField(max_length=130, blank=True, null=True)
    shipping_city = models.CharField(max_length=130, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=130, blank=True, null=True)
    shipping_country = models.CharField(max_length=1100, default='INDIA', blank=True, null=True)
    
    order_note = models.TextField(max_length=11130, null=True, blank=True)
    
    coupon_code = models.CharField(max_length=1200, blank=True, null=True)
    discount =  models.CharField(max_length=200, blank=True, null=True)
    total_amount  = models.IntegerField( blank=True, null=True)
    bill = models.TextField(max_length=11130, null=True, blank=True)
    payment_method = models.CharField(max_length=11200, blank=True, null=True)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=11200, blank=True, null=True)
    privacy_policy = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    uuid_id = models.UUIDField(default = uuid.uuid4, editable = False) 
    order_fulfilled = models.BooleanField(default=False)

    def itemsbought(self):
        
        return OrderItem.objects.filter(order=self.id)    

    def __str__(self):
        return self.first_name



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="Order")
    qty = models.IntegerField()
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name="Order_Cart_Price")
    shade=models.CharField(max_length=20, null=True)
    def amount(self):
        amount = int(self.qty)*int(self.price.price)
        return amount
    
    def __str__(self):
        return self.product

class NewsLetter(models.Model):
    email = models.CharField(max_length = 156,blank=True, null=True)
    date  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.email)
 


class Category(models.Model):
    category = models.CharField(max_length = 156)
    def __str__(self):
        return self.category

class Tags(models.Model):
    tags = models.CharField(max_length = 156)
    def __str__(self):
        return self.tags    

class Author(models.Model):
    description = RichTextUploadingField()
    name = models.CharField(max_length = 156)
    position = models.CharField(max_length = 156)
    fb =models.CharField(max_length = 156,blank=True, null=True)
    insta = models.CharField(max_length = 156, blank=True, null=True)
    linkedin = models.CharField(max_length = 156, blank=True, null=True)
    image  = models.ImageField(upload_to="SEO")
    def __str__(self):
        return self.name     
               
# Create your models here.
class Blog(models.Model):
    status  = models.BooleanField(default=True)
    
    h1  = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    page_name = models.CharField(max_length = 1256,blank=True, null=True)
    keyword = models.CharField(max_length = 156)
    description = models.CharField(max_length = 900)
    title = models.CharField(max_length = 156)
    breadcrumb = models.CharField(max_length = 156)
    canonical = models.CharField(max_length = 900, default="https://thegrandindianroute.com/")
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    image  = models.ImageField(upload_to="SEO")
    
    category = models.ManyToManyField(Category)
    tag  = models.ManyToManyField(Tags)
    updated  = models.DateField(auto_now=True)
    

   
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published  = models.DateField()
    content = RichTextUploadingField()
    active = True
    edits = RichTextUploadingField( blank=True, null=True)
    schema = models.TextField(max_length = 15622, blank=True, null=True)
    
    def __str__(self):
        return self.h1
    


class Team(models.Model):   
    image  = models.ImageField(upload_to="SEO")
    name = models.CharField(max_length = 156)
    position = models.CharField(max_length = 156)
    fb = models.CharField(max_length = 156)
    insta = models.CharField(max_length = 156)
    twitter = models.CharField(max_length = 156)
    youtube = models.CharField(max_length = 156)

    def __str__(self):
        return self.name

class Testimonials(models.Model):   
    image  = models.ImageField(upload_to="SEO")
    name = models.CharField(max_length = 156)
    position = models.CharField(max_length = 156)
    review = models.TextField()
 
    def __str__(self):
        return self.name
   


class Gallery(models.Model):
    name  = models.CharField(max_length = 150)
    image  = models.ImageField(upload_to="Gallery")
    date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    name  = models.CharField(max_length = 150)
    email  = models.CharField(max_length = 150)
    number  = models.CharField(max_length = 150)
    message  = models.TextField()
    
    def __str__(self):
        return str(self.email)
 