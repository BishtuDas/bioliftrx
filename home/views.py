from django.shortcuts import render, redirect
from .models import *
from .forms import *


def home(request):
    
    context = {
        
    }
    return render(request, 'index.html', context)


def contact(request):

    return render(request,'contact.html')


def blogs(request):
    data = Blog.objects.all().order_by('-id')
    context = {
        'data':data,
    }
    return render(request, 'blogs.html', context)


def blogsd(request, pk):
    data = Blog.objects.all().order_by('-id')[:5]   
    data2 = Blog.objects.get(slug=pk)

    # Handle contact form submission
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the contact form data to the database
            return render(request, 'blog-details.html', {'form': form, 'success': True})  # Render the same template with a success flag
    else:
        form = ContactForm()  # If not a POST request, initialize an empty form

    context = {
        'data': data,
        'data2': data2,
        'form': form,  # Pass the form to the template
    }

    return render(request, 'blog-details.html', context)