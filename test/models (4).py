from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length = 156)
    def __str__(self):
        return self.category
    

class Tags(models.Model):
    tags = models.CharField(max_length = 156)
    def __str__(self):
        return self.tags   


# class Team(models.Model):
#     name = models.CharField(max_length = 156)
#     position = models.CharField(max_length = 156)
#     image  = models.ImageField(upload_to="TEAM")
    
#     def __str__(self):
#         return self.name  

class Blog(models.Model):
    status  = models.BooleanField(default=True)
    
    h1  = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    page_name = models.CharField(max_length = 1256,blank=True, null=True)
    keyword = models.CharField(max_length = 156)
    description = models.CharField(max_length = 900)
    title = models.CharField(max_length = 156)
    breadcrumb = models.CharField(max_length = 156)
    canonical = models.CharField(max_length = 900, default="https://kenshinegroup.com/blogs/")
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    og_title=models.CharField(max_length = 100,blank=True, null=True)
    meta_title=models.CharField(max_length = 100,blank=True, null=True)
    og_description=models.CharField(max_length = 250,blank=True, null=True)
    meta_description=models.CharField(max_length = 250,blank=True, null=True)
    image  = models.ImageField(upload_to="SEO")
    
    banner_image  = models.ImageField(upload_to="banner", blank=True, null=True)
    category = models.ManyToManyField(Category)
    tag  = models.ManyToManyField(Tags)
    updated  = models.DateField(auto_now=True)
    

    
    
    published  = models.DateField()
    content = RichTextUploadingField()
    active = True
    edits = RichTextUploadingField( blank=True, null=True)
    schema = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return self.h1 
    

class Solution(models.Model):
    status  = models.BooleanField(default=True)
    sol  = models.BooleanField(default=True)
    sl_no = models.IntegerField(blank=True, null=True)
    h1  = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    page_name = models.CharField(max_length = 1256,blank=True, null=True)
    keyword = models.CharField(max_length = 156)
    description = models.CharField(max_length = 900,blank=True, null=True)
    description1 = models.CharField(max_length = 900,blank=True, null=True)
    title = models.CharField(max_length = 156)
    breadcrumb = models.CharField(max_length = 156)
    canonical = models.CharField(max_length = 900, default="https://kenshinegroup.com/service/")
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    og_title=models.CharField(max_length = 100,blank=True, null=True)
    meta_title=models.CharField(max_length = 100,blank=True, null=True)
    og_description=models.CharField(max_length = 250,blank=True, null=True)
    meta_description=models.CharField(max_length = 250,blank=True, null=True)
    image  = models.ImageField(upload_to="SEO")
    banner_image  = models.ImageField(upload_to="banner", blank=True, null=True)
    icon   = models.ImageField(upload_to="SEO", blank=True, null=True)
    category = models.ManyToManyField(Category)
    tag  = models.ManyToManyField(Tags)
    updated  = models.DateField(auto_now=True)
    

    blog_banner_lg = models.ImageField(upload_to="data", blank=True, null=True)
    
    published  = models.DateField()
    content = RichTextUploadingField()
    active = True
    edits = RichTextUploadingField( blank=True, null=True)
    schema = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.h1

        
    



class Gallery(models.Model):   
    image  = models.ImageField(upload_to="SEO")
    name = models.CharField(max_length = 156)
    def __str__(self):
        return self.name
    

class Contact(models.Model):   
    name =models.CharField(max_length = 1256,blank=True, null=True)
    email = models.CharField(max_length = 1256,blank=True, null=True)
    phone = models.CharField(max_length = 156)
    company = models.CharField(max_length = 156)
    mode = models.CharField(max_length = 156)
    message =RichTextUploadingField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Newsletter(models.Model):   
    
    email = models.CharField(max_length = 150)
    
    def __str__(self):
        return self.email 


class Vertical(models.Model):
    status  = models.BooleanField(default=True)
    sol  = models.BooleanField(default=True)
    sl_no = models.IntegerField(blank=True, null=True)
    h1  = models.CharField(max_length = 156)
    slug =models.CharField(max_length = 1256,blank=True, null=True)
    page_name = models.CharField(max_length = 1256,blank=True, null=True)
    keyword = models.CharField(max_length = 156)
    description = models.CharField(max_length = 900)
    title = models.CharField(max_length = 156)
    breadcrumb = models.CharField(max_length = 156)
    canonical = models.CharField(max_length = 900, default="")
    og_type =models.CharField(max_length = 156)
    og_card = models.CharField(max_length = 156)
    og_site = models.CharField(max_length = 156)
    og_title=models.CharField(max_length = 100,blank=True, null=True)
    meta_title=models.CharField(max_length = 100,blank=True, null=True)
    og_description=models.CharField(max_length = 250,blank=True, null=True)
    meta_description=models.CharField(max_length = 250,blank=True, null=True)
    image  = models.ImageField(upload_to="SEO")
    banner_image  = models.ImageField(upload_to="banner",blank=True, null=True)
    icon   = models.ImageField(upload_to="SEO", blank=True, null=True)
    
    category = models.ManyToManyField(Category)
    tag  = models.ManyToManyField(Tags)
    updated  = models.DateField(auto_now=True)
    

    blog_banner_lg = models.ImageField(upload_to="data", blank=True, null=True)
    
    published  = models.DateField()
    content = RichTextUploadingField()
    active = True
    edits = RichTextUploadingField( blank=True, null=True)
    schema = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.h1
    


class Affiliation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="Description of the affiliation.")
    date_added = models.DateField(auto_now_add=True, help_text="The date when the Affiliation was added.")
    image = models.ImageField(upload_to='data', blank=True, null=True, help_text="Image for the Affiliation.")

    def __str__(self):
        return f"Affiliation by {self.name}"
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the person giving the testimonial.")
    testimonial = models.TextField(help_text="The testimonial text.")
    date_added = models.DateField(auto_now_add=True, help_text="The date when the testimonial was added.")
    image = models.ImageField(upload_to='data', blank=True, null=True, help_text="Image for the testimonial.")

    def __str__(self):
        return f"Testimonial by {self.name}"

class Team(models.Model):
    name = models.CharField(max_length=100, help_text="The name of the team.")
    description = models.TextField(help_text="A short description of the team.")
    image = models.ImageField(upload_to='data', blank=True, null=True, help_text="An image representing the team.")
    
    def __str__(self):
        return self.name

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.document.name
    
class Faq(models.Model):
    status= models.BooleanField(default=True)
    servicefaq= models.BooleanField(default=False)
    question = models.CharField(max_length=100, help_text="The name of the team.")
    answer = models.TextField(help_text="Answer of the question.")
    number= models.IntegerField(default=1)
    def __str__(self):
        return self.question