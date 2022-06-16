from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as dj_login, logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
from django.core.serializers import serialize
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def counter(request):
    counter = {}
    counter['all_products'] = Products.objects.all().count()
    counter['all_products_set'] = Collection.objects.all().count()

    return counter


def index(request):
    products = Products.objects.order_by('-id').all()
    categories = Category.objects.all()

    products_new_sales =  Products.objects.filter(sale_status=1).order_by('-id')[:10]
    products_new =  Products.objects.order_by('-id')[:10]

    context = {'products':products,'categories':categories,'products_new_sales':products_new_sales, 'products_new':products_new}
    return render(request, 'index/index.html', context)

def contact(request):
    products = Products.objects.order_by('-id').all()
    categories = Category.objects.all()

    products_new_sales =  Products.objects.filter(sale_status=1).order_by('-id')[:10]
    products_new =  Products.objects.order_by('-id')[:10]

    context = {'products':products,'categories':categories,'products_new_sales':products_new_sales, 'products_new':products_new}
    return render(request, 'index/contact_us.html', context)

def error_page(request):
    products = Products.objects.order_by('-id').all()
    categories = Category.objects.all()

    context = {'products':products,'categories':categories}
    return render(request, 'index/404error.html', context)

def show_product_list(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('category')
        category = Category.objects.filter(id=id).first()
        if category:
            products = Products.objects.filter(category=category)
        # print(subdivisions)
        # pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)

        return JsonResponse({'products': list(products.values())}, safe=False)
    else:
        return HttpResponse(0)

def sets(request):
    products = Products.objects.order_by('-id').all()
    products_sets = ProductSet.objects.order_by('-id').all()
    collections = Collection.objects.order_by('-id').all()
    classess = Classes.objects.all()
    categories = Category.objects.all()

    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories}
    return render(request, 'index/products_sets.html', context)

def set_by_class(request,id):

    collections = Collection.objects.filter(sinf=id).all()
    sinf = Classes.objects.filter(id=id).first()
    classes = Classes.objects.all()
    categories = Category.objects.all()
    context = {'collections':collections,'sinf':sinf,'categories':categories,'classess':classes}
    return render(request, 'index/products_sets_by_class.html', context)

def show_set_product(request,id):

    classes = Classes.objects.all()
    categories = Category.objects.all()

    collection = Collection.objects.filter(id=id).first()
    products = ProductSet.objects.filter(collection=collection).all()

    context = {'categories':categories, 'classess':classes, 'products':products, 'collection':collection,'products':products}

    return render(request, 'index/show_set_product.html', context)

def show_product(request,id):

    classes = Classes.objects.all()
    categories = Category.objects.all()
    product = Products.objects.filter(id=id).first()
    products = Products.objects.filter(category=product.category).filter(~Q(id=id)).order_by('-id')[:10]
    context = {'product':product,'categories':categories,'classess':classes,'products':products}
    return render(request, 'index/show_product.html', context)


def sets_list_view(request):
    categories = Category.objects.all()
    products = Products.objects.order_by('-id').all()
    products_sets = ProductSet.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories}
    return render(request, 'index/shop_list_sets.html', context)


def products_by_category(request,id):
    products = Products.objects.filter(category=id).all()
    one = Category.objects.filter(id=id).first()

    categories = Category.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products': products, 'products_sets': products_sets, 'collections': collections, 'classess': classess,
               'categories': categories,'one':one}
    return render(request, 'index/products_by_cetegory.html', context)


def products_lists_by_category(request,id):
    products = Products.objects.filter(category=id).all()
    one = Category.objects.filter(id=id).first()

    categories = Category.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products': products, 'products_sets': products_sets, 'collections': collections, 'classess': classess,
               'categories': categories, 'one': one}
    return render(request, 'index/products_lists_by_categoy.html', context)

def sale_products(request):
    categories = Category.objects.all()
    products = Products.objects.order_by('-id').filter(sale_status=1).all()

    products_sets = ProductSet.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories}
    return render(request, 'index/sale_product.html', context)

def new_products(request):
    categories = Category.objects.all()
    products = Products.objects.order_by('-id').all()

    products_sets = ProductSet.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories}
    return render(request, 'index/new_product.html', context)

@login_required(login_url='/sign_in')
def admin_page(request):
    products = Products.objects.order_by('-id').all()
    context = {'products':products, 'counter': counter(request)}
    return render(request, 'admin_page/index.html', context)

@login_required(login_url='/sign_in')
def products(request):
    products = Products.objects.order_by('-id').all()

    context = {'products':products,'counter': counter(request)}
    return render(request, 'admin_page/products/products.html', context)


@login_required(login_url='/sign_in')
def add_product(request):

    categories = Category.objects.all()

    context = {'categories': categories, 'counter': counter(request)}

    return render(request, 'admin_page/products/create.html', context)


@login_required(login_url='/sign_in')
def product_store(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        name = request.POST.get('name')
        cost_buy = request.POST.get('cost_buy')
        cost_sell = request.POST.get('cost_sell')
        cost_discount = request.POST.get('cost_discount')
        # discount_persents = request.POST.get('discount_persents')
        amount = request.POST.get('amount')
        company = request.POST.get('company')
        foto =request.FILES.get('foto')
        info = request.POST.get('info')
        category_id = Category.objects.filter(id=category).first()
        if cost_sell:
            sale_status = 1
        else:
            sale_status = 0

        if category:
            product = Products(category=category_id, amount=amount, name=name, cost_buy=cost_buy, cost_sell=cost_sell, cost_discount=cost_discount,
                               company=company, foto=foto, info=info, sale_status=sale_status)
            product.save()

        return redirect('/products')
    else:
        return redirect('/login_page')

@login_required(login_url='/sign_in')
def edit_product(request,id):

    categories = Category.objects.all()
    product = Products.objects.filter(id=id).first()
    context = {'product': product,'categories':categories, 'counter': counter(request)}

    if product:
        return render(request, 'admin_page/products/edit.html', context)

@login_required(login_url='/sign_in')
def product_info_change(request,id):
    if request.method == 'POST':
        category = request.POST.get('category')
        name = request.POST.get('name')
        cost_buy = request.POST.get('cost_buy')
        cost_sell = request.POST.get('cost_sell')
        cost_discount = request.POST.get('cost_discount')
        amount = request.POST.get('amount')
        company = request.POST.get('company')
        foto = request.FILES.get('foto')
        info = request.POST.get('info')
        status = request.POST.get('status')
        category_id = Category.objects.filter(id=category).first()

        product = Products.objects.filter(id=id).first()

        if product:
            product.category=category_id
            product.name=name
            product.cost_buy=cost_buy
            product.cost_sell=cost_sell
            product.cost_discount=cost_discount
            product.amount=amount
            product.company=company
            product.status=status
            if foto:
                product.foto=foto
            else:
                product.foto=product.foto
            product.info=info
            product.save()

        return redirect('/products')
    else:
        return redirect('/login_page')

@login_required(login_url='/sign_in')
def delete_product(request,id):
    product = Products.objects.filter(id=id).first()
    product.delete()
    return redirect('/products')

@login_required(login_url='/sign_in')
def products_sets(request):
    classess = Classes.objects.all()
    collections = Collection.objects.all()
    products = ProductSet.objects.all()
    all_products = Products.objects.all()

    context = {'products': products,'all_products':all_products,'collections':collections,'classess':classess,'counter': counter(request)}
    return render(request, 'admin_page/products_sets/product_sets.html', context)

@login_required(login_url='/sign_in')
def add_collection(request):

    classess = Classes.objects.all()
    collections = Collection.objects.all()
    products = ProductSet.objects.all()
    all_products = Products.objects.all()

    context = {'classess': classess,'collections' :collections,'products':products,'all_products':all_products,'counter': counter(request)}

    return render(request, 'admin_page/products_sets/create.html', context)



@login_required(login_url='/sign_in')
def delete_collection(request,id):
    collection = Collection.objects.filter(id=id).first()
    collection.delete()
    return HttpResponseRedirect('/products_sets')

@login_required(login_url='/sign_in')
def collection_create(request):
    if request.method == 'POST':
        sinf = request.POST.get('sinf')
        if sinf:
            cl = Classes.objects.filter(id=sinf).first()
        name = request.POST.get('name')
        foto =request.FILES.get('foto')
        info = request.POST.get('info')

        collections = Collection(sinf=cl,name=name,foto=foto,description=info,status=0)
        collections.save()

        return redirect('/product_add_to_collection/%d/'%collections.id)
    else:
        return redirect('/login_page')

@login_required(login_url='/sign_in')
def product_add_to_collection(request,id):
    classess = Classes.objects.all()
    collection = Collection.objects.filter(id=id).first()
    product_sets = ProductSet.objects.filter(collection=collection).all()
    all_products = Products.objects.all()
    categories = Category.objects.all()

    context = {'collection': collection, 'counter': counter(request), 'product_sets': product_sets, 'classess': classess, 'all_products': all_products, 'categories': categories}
    if collection:
        # messages.success(request, "To'plam yaratildi. Mahsulot qo'shishingiz mumkin!")
        return render(request, 'admin_page/products_sets/add_product.html', context)
    else:
        messages.error(request, "Bu turdagi to'plam  topilmadi")
        return HttpResponseRedirect('/products_sets')

@login_required(login_url='/sign_in')
def add_product_to_collection(request):
    if request.method == 'POST':
        # sinf = request.POST.get('sinf')
        product = request.POST.get('product')
        product_amount = request.POST.get('product_amount')

        collection_id = request.POST.get('collection_id')

        collection = Collection.objects.filter(id=collection_id).first()
        if product:
            pr = Products.objects.filter(id=product).first()
        else:
            messages.error(request, "Bunday mahsulot topilmadi")
            return HttpResponseRedirect('/product_add_to_collection/%d/'%collection.id)

        product_set = ProductSet(product=pr, collection=collection, product_amount=product_amount)
        product_set.save()

        collection.amount = collection.amount+1

        if collection.cost_sell:
            collection.cost_sell = int(str(collection.cost_sell))+int(str(pr.cost_sell))
        else:
            collection.cost_sell = pr.cost_sell

        if collection.cost_buy:
            collection.cost_buy = int(str(collection.cost_buy))+int(str(pr.cost_buy))
        else:
            collection.cost_buy = pr.cost_buy

        if collection.cost_discount:
            collection.cost_discount = int(str(collection.cost_discount))+int(str(pr.cost_discount))
        else:
            collection.cost_discount = pr.cost_discount

        collection.save()

        messages.success(request, "To'plamga mahsulot qo'shildi")
        return HttpResponseRedirect('/product_add_to_collection/%d/'%collection.id)
    else:
        return redirect('/login_page')


@login_required(login_url='/sign_in')
def delete_collection_product(request,id):

    product = Products.objects.filter(id=id).first()
    products_set = ProductSet.objects.filter(product=product).first()
    collection = Collection.objects.filter(id=products_set.collection.id).first()

    if collection.cost_sell:
        collection.cost_sell = int(str(collection.cost_sell)) - int(str(product.cost_sell))
    else:
        collection.cost_sell = ''

    if collection.cost_buy:
        collection.cost_buy = int(str(collection.cost_buy)) - int(str(product.cost_buy))
    else:
        collection.cost_buy = ''

    if collection.cost_discount:
        collection.cost_discount = int(str(collection.cost_discount)) - int(str(product.cost_discount))
    else:
        collection.cost_discount = ''

    if collection.amount != 0:
        collection.amount = collection.amount - 1
    else:
        collection.amount = 0
    collection.save()
    products_set.delete()

    messages.success(request, "Mahsulot to'plamdan olib tashlandi")
    return HttpResponseRedirect('/product_add_to_collection/%d/'%products_set.collection.id)

def login(request):
    context = {}

    return render(request, 'admin_page/login.html', context)

def sign_in(request):
    if request.method == 'POST':
        login = request.POST.get('email')
        password = request.POST.get('password')
        print(login)
        print(password)
        user = authenticate(request, username=login, password=password)
        if user is not None:
            profile = Worker.objects.filter(user=user).first()
            if profile.permission == True:
                dj_login(request,user)
                print('asd')
                return redirect('/admin_page')
            else:
                messages.error(request, "Sizga ruxsat berilmagan! Iltimos kuting!")
                return redirect('/login_page')
        else:

            messages.error(request, "Bunday nomli foydalanuvchi mavjud emas!")
            return HttpResponseRedirect('/login_page')
    else:
        messages.error(request, "Bunday nomli foydalanuvchi mavjud emas!")
        return HttpResponseRedirect('/login_page')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login_page')