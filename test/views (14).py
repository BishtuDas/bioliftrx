from django.http import JsonResponse
from django.shortcuts import render, redirect 
from .models import *
from .forms import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
# from .decorators import check_recaptcha
from django.contrib.sitemaps import Sitemap
from django.urls import reverse




from urllib.parse import urlparse






class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return ['home:home', 'home:about', 'home:service', 'home:gallery', 'home:contact', 'home:faq', 'home:terms', 'home:privacy', 'home:testimonial', 'home:careers', 'home:clients', 'home:affilations']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Blog.objects.all()

    def location(self, obj):
        return reverse('home:blog_detail', args=[obj.slug])

class VerticalSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Vertical.objects.all()

    def location(self, obj):
        return reverse('home:vertical_detail', args=[obj.slug])




# Dictionary mapping old paths to new URLs (without domain/protocol)
REDIRECT_MAP = {
    'blogs/navigating_customs_clearance': 'https://www.kenshinegroup.com/blogs/navigating-customs-clearance/',
    'blogs/streamlining_your_supply_chain': 'https://www.kenshinegroup.com/blogs/streamlining-your-supply-chain/',
    'blogs/the_role_of_technology_in_modern_warehousing': 'https://www.kenshinegroup.com/blogs/the-role-of-technology-in-modern-warehousing/',
    'service/sea-freight': 'https://www.kenshinegroup.com/service/sea-freight/',
    'vertical/retail-and-e-commerce': 'https://www.kenshinegroup.com/vertical/retail-and-e-commerce/',
    'index.html': 'https://www.kenshinegroup.com',
    'service/packaging/packaging-palletization-fumigation': 'https://www.kenshinegroup.com/service/packaging/',
    'freight-forwarding': 'https://www.kenshinegroup.com/service/freight-forwarding/',
    'service/exim-consultancy/exim-consultancy': 'https://www.kenshinegroup.com/service/exim-consultancy/',
    'service/warehousing/warehousing': 'https://www.kenshinegroup.com/service/warehousing/',
    'blogs/streamlining_your_supply_chain': 'https://www.kenshinegroup.com/blogs/streamlining-your-supply-chain/',
    'service/supply-chain-management': 'https://www.kenshinegroup.com/service/supply-chain-management/',
    'air-freight': 'https://www.kenshinegroup.com/service/freight-forwarding/',
    'about/{search_term_string}': 'https://www.kenshinegroup.com/about/',
    'blogs/the-future-of-the-logistics-industry-in-india': 'https://www.kenshinegroup.com/blogs/the-future-of-the-logistics-industry-in-india/'
}

def handle_redirect(request, old_url):
    # Parse the incoming URL to extract the path, ignoring scheme, domain, and query params
    parsed_url = urlparse(old_url).path.strip('/').lower()

    # Attempt to find the URL in the REDIRECT_MAP, normalizing slashes and case
    new_url = REDIRECT_MAP.get(parsed_url)
    
    # If the path is found in the map, redirect to the corresponding new URL
    if new_url:
        return redirect(new_url)
    
    # Handle case where old URL doesn't exist in the map
    return redirect('home:home')  # Redirect to homepage or any default page



# Create your views here.
def home(request):
    data = Blog.objects.all().order_by('-id')[:3]
    vertical = Vertical.objects.all().order_by('-id')
    testimonials = Testimonial.objects.all()
    context = {
        'data':data,
        'vertical':vertical,
        'testimonials':testimonials,
        
    }
    return render(request, 'index.html', context)


def vessel(request):
    context = {
        
    }
    return render(request, 'vessel.html', context)

def about(request):
    team=Team.objects.all()
    blog=Blog.objects.all().order_by('-id')
    affiliation=Affiliation.objects.all()
    
    context = {
        'data':team,
        'blog':blog,
        'affiliation':affiliation,
    }
    return render(request, 'aboutus.html', context)

def verticals(request):
    context = {
        
    }
    return render(request, 'verticals.html', context)

def vertical_detail(request, pk):
    data = Vertical.objects.get(slug=pk)
    data2 = Vertical.objects.all().order_by('sl_no')
    
    context = {
        'data':data,
        'data2':data2,
    }
    return render(request, 'vertical_detail.html', context)

def service(request):
    context = {
        
    }
    return render(request, 'service.html', context)

def service_detail(request, pk):
    data = Solution.objects.get(slug=pk)
    data2 = Solution.objects.all().order_by('sl_no')
    context = {
        'data':data,
        'data2':data2,
    }
    return render(request, 'service_detail.html', context)




def gallery(request):
    data = Gallery.objects.all().order_by('-id')
    context = {
        'data':data,
    }
    return render(request, 'gallery.html', context)
 
# @check_recaptcha   
# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid() and request.recaptcha_is_valid:
#             form.save()
#             messages.success(request, 'Your data is sent successfully.')
#             return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
#         else:
#             messages.error(request, "Your data is not sent! Try Again")
#             print(form.errors)
#             return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
#     context = {

#     }
#     return render(request, 'contact.html',context)
    

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your data is sent successfully.')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            messages.error(request, "Your data is not sent! Try Again")
            print(form.errors)
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
    context = {

    }
    return render(request, 'contact.html',context)
    

def blog(request):
    data = Blog.objects.all().order_by('-id')
    context = {
        'data':data,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, pk):
    data = Blog.objects.get(slug=pk)
    data2 = Blog.objects.all().order_by('-id')[:7]
    context = {
        'data':data,
        'data2':data2,
    }
    return render(request, 'blog_detail.html', context)


def testimonial(request):
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('testimonials_list')  # Redirect to the list of testimonials
    else:
        form = TestimonialForm()
    return render(request, 'testimonial.html', {'form': form})


def careers(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'careers.html')
    else:
        form = DocumentForm()
   
    context = {
        'form': form
    }
    return render(request, 'careers.html', context)

def misson(request):
    context = {
        
    }
    return render(request, 'misson.html', context)

def teams(request):
    data=Team.objects.all()
    context = {
        'data':data
    }
    return render(request, 'teams.html', context)

def clients(request):
    testimonials = Testimonial.objects.all()
    context = {
        'testimonials':testimonials,
    }
    return render(request, 'clients.html', context)

def affilations(request):
    affiliation=Affiliation.objects.all()
    context = {
        'affiliation':affiliation,
    }
    return render(request, 'affilations.html', context)

def privacy(request):
    context = {
        
    }
    return render(request, 'privacy.html', context)

def terms(request):
    context = {
        
    }
    return render(request, 'terms.html', context)

def support(request):
    context = {
        
    }
    return render(request, 'support.html', context)


def faq(request):
    faq=Faq.objects.all()
    context = {
        'faq':faq
    }
    return render(request, 'faq.html', context)

def testimonial(request):
    context = {
        
    }
    return render(request, 'testimonial.html', context)

def newsletter(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your email is stored successfully")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            messages.error(request, "Your email is not stored! Try Again")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 
    context = {

    }
    return render(request, 'index.html', context)
    
    

    


