from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

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
    



class Contact(models.Model):
    name  = models.CharField(max_length = 150)
    email  = models.CharField(max_length = 150)
    number  = models.CharField(max_length = 150)
    message  = models.TextField()
    
    def __str__(self):
        return str(self.email)
 
    
