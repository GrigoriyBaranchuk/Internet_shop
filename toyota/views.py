from django.shortcuts import render, redirect
from toyota.models import Category, Product, Basket, ProductInBasket, ProductIMG, Order, ProductInOrder
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
    categories_dict = {cat.id: cat for cat in categories}
    category = categories_dict[category_pk]
    # import pdb
    # pdb.set_trace()
    products = Product.objects.filter(category=category_pk)
    return render(request, 'toyota/category.html', {'products': products,
                                                    'categories': categories,
                                                    'category_name': category.name
                                                    })


def product_details(request, product_pk):
    product = Product.objects.filter(id=product_pk).first()
    image = ProductIMG.objects.filter(product_id=product_pk).first()
    categories = Category.objects.all()
    return render(request, 'toyota/product_details.html', {'product': product,
                                                           'categories': categories,
                                                           'images': image
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


def user_basket(request, user_pk):
    basket_id = Basket.objects.filter(user_id=user_pk).first()
    products_set = ProductInBasket.objects.filter(basket_id=basket_id)
    categories = Category.objects.all()
    return render(request, 'toyota/user_basket.html', {'user_pk': user_pk,
                                                       'products_set': products_set,
                                                       'categories': categories,
                                                       'basket': basket_id,
                                                       })


def add_product_to_basket(request, product_pk):
    user = request.user
    product = Product.objects.filter(id=product_pk).first()
    basket = Basket.objects.filter(user_id=user.id).first()
    quantity = float(request.POST.get('quantity'))
    product_in_basket = ProductInBasket.objects.filter(basket=basket, product=product).first()

    if not product_in_basket:
        ProductInBasket.objects.create(product=product,
                                       basket=basket,
                                       quantity=quantity,
                                       )
    else:
        product_in_basket.quantity = float(product_in_basket.quantity) + quantity
        product_in_basket.save()

    return redirect('index')


def delete_product_from_basket(request, product_in_basket_pk):
    user = request.user
    instance_for_del = ProductInBasket.objects.filter(id=product_in_basket_pk)
    instance_for_del.delete()

    return redirect('user_basket', **{'user_pk': user.id})


"""User
pwd: user123456789 """


def action_with_product_weight(request, action, product_in_basket_pk):
    from decimal import Decimal
    product_in_basket = ProductInBasket.objects.filter(id=product_in_basket_pk).first()

    if action == 'add':
        product_in_basket.quantity += Decimal('0.100')
    elif action == 'reduce':
        product_in_basket.quantity -= Decimal('0.100')

    product_in_basket.save()
    if product_in_basket.quantity <= 0:
        product_in_basket.delete()

    return redirect('user_basket', **{'user_pk': request.user.id})


def buy(request, basket):
    b = Basket.objects.get(id=basket)
    products = ProductInBasket.objects.filter(basket_id=b.id)
    if products:
        order = Order.objects.create(basket=b)
        for prod in products:
            ProductInOrder.objects.create(order=order,
                                          product=prod.product,
                                          quantity=prod.quantity,
                                          price=prod.price_per_weight,
                                          )
        order.sum_of_order()
        products.delete()

    return redirect('user_basket', **{'user_pk': request.user.id})



