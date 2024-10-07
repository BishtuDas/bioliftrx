from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .form import *
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect 
from .form import RegisterForm, ProfileForm, LoginForm
from .models import Profile

from decimal import Decimal

from django.http import JsonResponse
from .services import get_ups_shipping_rate
from .models import Product, Cart
import os
import resend
import logging
resend.api_key = "re_jB5B3sEb_P8XKNsF5TXKjt89th84QVDtb"
logger = logging.getLogger(__name__)

def calculate_shipping_cost(request):
    if request.method == "POST":
        pin_code = request.POST.get("pin_code")
        user = request.user
        
        cart_items = Cart.objects.filter(user=user)
        
        total_shipping_cost = 0
        for item in cart_items:
            product = item.product
            weight = product.weight_in_lbs
            length = product.lenght_in_inch
            width = product.width_in_inch
            height = product.height_in_inch
            
            # Debugging: Print or log the product details
            # logger.debug(f"Product ID: {product.id}, Weight: {weight}, Length: {length}, Width: {width}, Height: {height}")
            
            try:
                shipping_response = get_ups_shipping_rate('08830', pin_code, weight, length, width, height)
                # logger.debug(f"Shipping Response: {shipping_response}")
                
                # Check for errors in the response
                rate_response = shipping_response.get('RateResponse', None)
                if rate_response and 'RatedShipment' in rate_response:
                    total_charges = rate_response['RatedShipment']['TotalCharges']['MonetaryValue']
                    shipping_cost = Decimal(total_charges)
                    total_shipping_cost += shipping_cost
                else:
                    logger.error(f"Error in shipping response: {shipping_response}")
                    return JsonResponse({"error": "Failed to retrieve shipping rate. Please try again later."}, status=500)
            
            except Exception as e:
                logger.error(f"Error retrieving shipping rate: {str(e)}")
                return JsonResponse({"error": str(e)}, status=500)
        final_shipping_cost = 0
        for item in cart_items:
            item.shipping_cost = (Decimal(shipping_cost) * Decimal(item.qty))
            final_shipping_cost += item.shipping_cost
            item.total_price_with_shipping = (Decimal(item.price.price) * Decimal(item.qty)) + (Decimal(shipping_cost))
            item.save()

        print(rate_response )
        return JsonResponse({
            "total_shipping_cost": float(final_shipping_cost),
            "total_cost_with_shipping": float(total_shipping_cost + sum(item.amount() for item in cart_items))
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

# Create your views here.
def home(request):

    data = Product.objects.filter(featured=True)
    data1 = Product.objects.filter(sale1=True)
    data2 = Product.objects.filter(sale2=True)
    data4 = Blog.objects.all().order_by('-id')[:3]
    data5= Product.objects.filter(bestseller=True)             #[:4] Limiting the queryset to 4 items
    
    context = {
        'data':data,
        'data1':data1,
        'data2':data2,
        'data4':data4,
        'data5':data5,
    }
    return render(request, 'index.html', context)

def create_account(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            try:
                user = User.objects.get(username-username)
                messages.success(request, 'Your profile aleardy exists!')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

            except:
                profile =  profile_form.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request, 'Your profile was create & login successful!')
                #authenticate checks if credentials exists in db
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        if 'next' in request.POST:
                            return redirect(request.POST.get('next'))
                        else:
                            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                    else:
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                        
                else:
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                
        else:
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = RegisterForm()
        profile_form = ProfileForm()
    context = {
      'user_form':user_form,
      'profile_form':profile_form,
    }

    return render(request, 'singup.html', context)


def byebye(request):
    logout(request)
    return redirect ('home:home')


def login_user(request):
    
    if request.method == "POST":
        # your sign in logic goes here
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            #authenticate checks if credentials exists in db
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                else:
                    messages.error(request, 'Login failed!')
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                    
            else:
                messages.error(request, 'Login failed!')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='home:home')
def dashboard(request):
    data = Order.objects.filter(user_id=request.user)
    context = {
        'data':data,
    }
    return render(request, 'dashboard.html', context)

def product_list(request, pk):
    data = ProductCategory.objects.get(slug=pk)
    
    data1 = Product.objects.filter(product_category=data)
    page = request.GET.get('page', 1)
    paginator = Paginator(data1, 6)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {
        'data':data,
        'product':product,
    }
    return render(request, 'product_list.html', context)





@login_required(login_url='home:home')
def wishlist_page(request):
    
    data1 = Wishlist.objects.filter(user=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(data1, 6)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {
        'product':product,
    }
    return render(request, 'wishlist.html', context)

def product_detail(request, pk, fk):
    if request.method == 'POST':
        qty = request.POST.get('qty')
        product_id = request.POST.get('product')
        mm = request.POST.get('mm')
        shade = request.POST.get('shade')

        print(f"Received POST data: qty={qty}, product_id={product_id}, mm={mm}, shade={shade}")

        try:
            # Fetch the product and price objects
            product = Product.objects.get(id=product_id)
            price = Price.objects.get(mm=mm, product=product)
            
        except Product.DoesNotExist:
            print("Product not found.")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        except Price.DoesNotExist:
            print("Price not found.")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        if request.user.is_authenticated:
            user = request.user
            try:
                # Check if the item already exists in the user's cart
                existing_cart_item = Cart.objects.get(product=product, user=user, price=price)
                existing_cart_item.qty += int(qty)
                existing_cart_item.shade = shade
                existing_cart_item.save()
                print("Cart updated for authenticated user.")
            except Cart.DoesNotExist:
                # If it doesn't exist, create a new cart item
                Cart.objects.create(product=product, user=user, qty=qty, price=price, shade=shade)
                print("Cart item created for authenticated user.")
        else:
            # If the user is not authenticated, use the session cart

            # Clear the session cart to keep only the current submission
            request.session['cart'] = []

            session_cart = request.session.get('cart', [])
            print(f"Initial session cart: {session_cart}")

            # Add the new item to the session cart
            session_cart.append({
                'product_id': product.id,
                'qty': qty,
                'price_id': price.id,
                'shade': shade,
                'mm': mm
            })
            print("New item added to session cart.")

            # Save the updated cart back to the session
            request.session['cart'] = session_cart
            print(f"Updated session cart: {session_cart}")

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    # Fetch product details for display on the page
    product = Product.objects.get(slug=fk)
    shades = Shade.objects.all()
    related_products = Product.objects.all()[:5]
    price_data = Price.objects.all()

    context = {
        'data': product,
        'product2': related_products,
        'shade': shades,
        'data2': price_data,
    }
    return render(request, 'product_detail.html', context)


from django.shortcuts import get_object_or_404

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            discount = coupon.discount_percentage
            request.session['coupon_discount'] = float(discount)
            return redirect('home:cart')
        except Coupon.DoesNotExist:
            request.session['coupon_error'] = 'Invalid coupon code!'
            return redirect('home:cart')

    return redirect('home:cart')

def remove_coupon(request):
    if request.method == 'POST':
        # Clear the coupon discount from the session
        request.session['coupon_discount'] = None
        request.session['coupon_error'] = None
        return redirect('home:cart')

    return redirect('home:cart')


def cart(request):
    cart_items = []
    subtotal = 0

    if request.user.is_authenticated:
        # Get cart items for authenticated user
        user = request.user
        data = Cart.objects.filter(user=user)
        
        for item in data:
            item_price = item.price.price  
            item_subtotal = item_price * item.qty
            subtotal += item_subtotal
            
            cart_items.append({
                'product': item.product,
                'qty': item.qty,
                'price': item_price,
                'shade': item.shade,
                'mm': item.price.mm,
                'subtotal': item_subtotal
            })
    else:
        # Get cart items for guest user from session
        session_cart = request.session.get('cart', [])
        
        for item in session_cart:
            product = get_object_or_404(Product, id=item['product_id'])
            price = get_object_or_404(Price, id=item['price_id'])
            item_price = price.price  # Assuming `price` is a field in the Price model
            item_subtotal = item_price * item['qty']
            subtotal += int(item_subtotal)
            
            cart_items.append({
                'product': product,
                'qty': item['qty'],
                'price': item_price,
                'shade': item['shade'],
                'mm': price.mm,
                'subtotal': item_subtotal
            })

    # Check if a coupon is applied
    discount = request.session.get('coupon_discount', 0)  # Default to 0 if not set
    discount_amount = subtotal * (discount / 100) if discount else 0

    # Calculate total
    total = subtotal - discount_amount
    
    # Clear the error message after displaying it
    coupon_error = request.session.pop('coupon_error', None)
    #pop() retrieves the value associated with the key 'coupon_error' from the session and then removes that key-value pair from the session data.
    print(coupon_error)
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'discount_amount': discount_amount,
        'total': total,
        'coupon_error': coupon_error,
    }

    return render(request, 'cart.html', context)

@login_required(login_url='home:home')
def checkout(request):
    if request.user.is_authenticated:
        try:
            user =request.user
            user = User.objects.get(username=request.user)
            data = Cart.objects.filter(user=user)
            subtotal = 0
            for ie in data:
                subtotal = subtotal + int(ie.price.price*ie.qty)
            context = {
                'data':data,
            
            }
        except:
            subtotal = 0
            context = {

            }
    else:
        # Guest user cart data from session
        cart_items = []
        session_cart = request.session.get('cart', {})
        for item in session_cart.values():
            product = get_object_or_404(Product, id=item['product_id'])
            cart_items.append({
                'product': product,
                'qty': item['qty'],
                'price': item['price'],
                'shade': item['shade'],
                'mm': item['mm'],
            })
        

    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.total_amount = int(subtotal)
            data.save()
            return redirect('home:payment')
        else:
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return render(request, 'checkout.html', context)


def remove_item(request, pk):
    
    try:
        user =request.user
        data = Cart.objects.get(user=user, id=pk)
        data.delete()



    except:
        pass    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



def wishlist(request, pk):
    
    try:
        user =request.user
        product =Product.objects.get(id=pk)
        data = Wishlist.objects.get(user=user, product=product)
        data.delete()
    except:
        user =request.user
        product =Product.objects.get(id=pk)
        data = Wishlist.objects.create(user=user, product=product)
        data.save()    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



def payment(request):
    try:
        user =request.user
        user = User.objects.get(username=request.user)
        data = Order.objects.filter(user_id=user).last()
        
        context = {
            'data':data,
           
        }
    except:
        context = {

        }

    if request.method =='POST':
       form = PaymentForm(request.POST)
       print('abc 1')
       if form.is_valid():
            # Process payment
            merchantAuth = apicontractsv1.merchantAuthenticationType()
            # merchantAuth.name = '25krzX54A2X'
            # merchantAuth.transactionKey = '956ZY3N22cQpVn5E'

            merchantAuth.name = '25krzX54A2X'
            merchantAuth.transactionKey = '9MVpm42s98LrCa4m'

            creditCard = apicontractsv1.creditCardType()
            creditCard.cardNumber = form.cleaned_data['card_number']
            creditCard.expirationDate = f"{form.cleaned_data['exp_year']}-{form.cleaned_data['exp_month']}"
            creditCard.cardCode = str(form.cleaned_data['cvv'])
            payment = apicontractsv1.paymentType()
            payment.creditCard = creditCard
            
            uuid_id = request.POST.get('uuid')
            uuid_id = str(uuid_id)
            print(uuid_id)
            uprice = Order.objects.get(uuid_id=uuid_id)
            uprice = uprice.total_amount    
            price = int(uprice)
            
            transactionrequest = apicontractsv1.transactionRequestType()
            transactionrequest.transactionType = "authCaptureTransaction"
            transactionrequest.amount = price  # Set the amount
            transactionrequest.payment = payment

            createtransactionrequest = apicontractsv1.createTransactionRequest()
            createtransactionrequest.merchantAuthentication = merchantAuth
            createtransactionrequest.transactionRequest = transactionrequest

            controller = createTransactionController(createtransactionrequest)
            controller.execute()

            response = controller.getresponse()
            if response is not None:
                # Handle the response...
                user = Order.objects.get(uuid_id=uuid_id)
                print(user)
                user.paid = True
                print('abc 3')
                uid = request.user.id
                cart = Cart.objects.filter(user=uid)

                cart_dict = {"name":[], "qty":[], "size":[]}
                a = cart_dict["name"]
                for ie in cart:
                    d = OrderItem.objects.create(order=user, product=ie.product, qty=ie.qty, price=ie.price)
                    d.save()
                    if a:
                        for i in a:
                            if ie.price.mm in cart_dict["size"]:
                                pass
                            else:
                                cart_dict["name"].append(ie.product.name)
                                cart_dict["qty"].append(ie.qty) 
                                cart_dict["size"].append(ie.price.mm) 
                                
                    else:
                        cart_dict["name"].append(ie.product.name)
                        cart_dict["qty"].append(ie.qty)     
                        cart_dict["size"].append(ie.price.mm)
                    ie.delete()    
            
                print(cart_dict)
                user.bill = cart_dict   
                user.save() 
                # Send confirmation email
                order_details = f"""
                <strong>Order Confirmation for {user.username}</strong><br><br>
                Order Details:<br>
                Name: {user.username}<br>
                Total Amount: {user.total_amount}<br>
                Items:<br>
                <ul>
                """

               
                for name, qty, size in zip(user.bill["name"], user.bill["qty"], user.bill["size"]):
                    order_details += f"<li>{name} - Quantity: {qty}, Size: {size}</li>"

                order_details += "</ul>"

                params = resend.Emails.SendParams(
                    from_="onboarding@resend.dev",
                    to=["info@alvydental.com"],
                    subject="Order Confirmation",
                    html=order_details,
                    headers={"X-Entity-Ref-ID": "123456789"},
                )

                email = resend.Emails.send(params)
                print(email)  # Log email response

                messages.success(request, 'Order Placed Successfully')
                return redirect('home:dashboard')  # Example success page

       else:
            # Redirect or show a success/failure page
            print(form.errors)

            messages.error(request, 'Payment Failed! Try Again')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = PaymentForm()

    return render(request, 'payment.html', context)




def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your query is sent successfully")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            messages.error(request, "Your query is not sent! Try Again")
            print(form.errors)
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  
    context = {

    }
    return render(request, 'contact.html', context)
    
def blogs(request):
    data = Blog.objects.all().order_by('-id')
    context = {
        'data':data,
    }
    return render(request, 'blog.html', context)


def blogsd(request, pk):
    data = Blog.objects.all().order_by('-id')[:5]
    data2 = Blog.objects.get(slug=pk)
    context = {
        'data':data,
        'data2':data2,
    }
    return render(request, 'blog_detail.html', context)

def gallery(request):
    data = Gallery.objects.all(19).order_by('-id')
    context = {
        'data':data,
    }
    return render(request, 'gallery.html', context)


def about_us(request):
    data4 = Blog.objects.all().order_by('-id')[:3]
    data = Product.objects.all().order_by('-id')[:6]
    context = {
        'data':data,
        'data4':data4,
    }
    return render(request, 'about.html', context)


def newsletter(request):
    
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            data = NewsLetter.objects.create(email=email)
            data.save()
            messages.success(request, 'Subscription Successful')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        
        except:
            return redirect('home:home')
            

def product_search(request):
    query = request.GET.get('q')
    product= Product.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'product': product,
    }
    return render(request, 'product_list.html', context)
    
def returnPolicy(request):
    context = {
        
    }
    return render(request, 'return.html', context)
    
def brouchure(request):
    
    
    context = {
        
    }
    return render(request, 'brouchure.html', context)
    

def products(request):
    data = Product.objects.all().order_by('name')
    context = {
        'data':data,
    }
    return render(request, 'products.html', context)