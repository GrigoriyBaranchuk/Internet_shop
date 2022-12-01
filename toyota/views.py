from django.shortcuts import render, redirect
from toyota.models import Category, Product, Basket, ProductInBasket
from toyota.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.


def index(request):
    categories = Category.objects.all()
    return render(request=request, template_name='toyota/index.html', context={'categories': categories,
                                                                               })


def category_details(request, category_pk):
    categories = Category.objects.all()
    products = Product.objects.filter(category=category_pk)
    return render(request, 'toyota/category.html', {'products': products,
                                                    'categories': categories,
                                                    })


def product_details(request, product_pk):
    product = Product.objects.filter(id=product_pk).first()
    categories = Category.objects.all()
    return render(request, 'toyota/product_details.html', {'product': product,
                                                           'categories': categories,
                                                           })


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Basket.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "registration/register.html", {"register_form": form})


def add_product_to_basket(request, product_pk):
    # import pdb
    # pdb.set_trace()
    user = request.user
    quantity = int(request.POST.get('quantity'))

    ProductInBasket.objects.create(product=Product.objects.filter(id=product_pk).first(),
                                   basket=Basket.objects.filter(id=user.id).first(),
                                   quantity=quantity)
    return redirect('index')

