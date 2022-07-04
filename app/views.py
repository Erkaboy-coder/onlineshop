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
from django.contrib.auth.models import User
from django.db.models import Count

def counter(request):
    counter = {}
    counter['all_products'] = Products.objects.all().count()
    counter['all_products_set'] = Collection.objects.all().count()
    counter['new_orders'] = Order.objects.filter(status=0).values('user').annotate(dcount=Count('user')).order_by().count()

    return counter

# def oderstore(request):
#     orderstore = {}
#     orderstore['orderstore'] = OrderStore.objects.all()
#
#     return orderstore

def index(request):
    products = Products.objects.order_by('-id').all()
    categories = Category.objects.all()
    ordersstore = OrderStore.objects.all()
    most_saled = Products.objects.order_by('-status_trent')[:10]

    products_most_showed =  Products.objects.order_by('-show')[:10]
    trendproduct =  Products.objects.order_by('-show').first()
    products_new =  Products.objects.order_by('-id')[:10]

    context = {'products':products,'categories':categories,'products_most_showed':products_most_showed, 'products_new':products_new,'ordersstore':ordersstore,
               'trendproduct':trendproduct,'most_saled':most_saled}
    return render(request, 'index/index.html', context)

def contact(request):
    products = Products.objects.order_by('-id').all()
    categories = Category.objects.all()

    products_new_sales =  Products.objects.filter(sale_status=1).order_by('-id')[:10]
    products_new =  Products.objects.order_by('-id')[:10]
    ordersstore = OrderStore.objects.all()
    context = {'products':products,'categories':categories,'products_new_sales':products_new_sales, 'products_new':products_new,'ordersstore':ordersstore}
    return render(request, 'index/contact_us.html', context)

def error_page(request):
    products = Products.objects.order_by('-id').all()
    categories = Category.objects.all()

    context = {'products':products,'categories':categories}
    return render(request, 'index/404error.html', context)
def order_store(request):
    orders = OrderStore.objects.all()
    categories = Category.objects.all()
    ordersstore = OrderStore.objects.all()
    products = Products.objects.order_by('-id')[:10]
    cost = 0
    for i in orders:
        cost = cost + int(i.product_amount)*int(i.product.cost_discount)
    context = {'orders': orders,'cost':cost,'categories':categories,'ordersstore':ordersstore,'products':products}
    return render(request, 'index/orderstore.html', context)

def delete_product_from_store(request,id):

    order = OrderStore.objects.filter(product=id).first()
    order.delete()
    return redirect('/order_store')

def order_page(request):
    orders = OrderStore.objects.all()
    categories = Category.objects.all()
    ordersstore = OrderStore.objects.all()
    oblasts = Oblast.objects.all()
    products = Products.objects.order_by('-id')[:10]
    cost = 0
    for i in orders:
        cost = cost + int(i.product_amount)*int(i.product.cost_discount)
    context = {'orders': orders,'cost':cost,'categories':categories,'ordersstore':ordersstore,'products':products,'oblasts':oblasts}
    return render(request, 'index/order.html', context)


def order(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        region = data.get('region')
        district = data.get('district')
        address = data.get('address')
        payment_method = data.get('payment_method')
        contact = data.get('contact')

        user = User.objects.filter(username=first_name).first()
        orders = OrderStore.objects.all()

        if not user:
            user = User.objects.create_user(username=first_name, password=contact)
            user.save()
            worker = Worker(firstname=first_name,lastname=last_name,contact=contact,user=user)
            worker.save()

        else:
            worker = Worker.objects.filter(user=user).first()
            if not worker:
                worker = Worker(firstname=first_name, lastname=last_name, contact=contact, user=user)
                worker.save()

        for i in orders:
            order = Order(user=worker, product=i.product, product_amount=i.product_amount,payment_method=payment_method, address=address, region=region,district=district)
            order.save()

        for i in orders:
            i.delete()

        messages.success(request,"Xarid amalga oshirildi. Xarid chekini shaxsiy kabinetga kirib ko'rishingiz mumkin bo'ladi")
        return HttpResponse(1)
    else:
        return HttpResponse(0)

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
def change_product_amount(request):
    if request.method == 'POST':
        data = request.POST
        order_id = data.get('order_id')
        product_amount = data.get('product_amount')
        order = OrderStore.objects.filter(id=order_id).first()
        order.product_amount = product_amount
        order.save()

        return HttpResponse(1)
    else:
        return HttpResponse(0)

def show_districts(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('region')
        district = Region.objects.filter(oblast=id)
        # print(subdivisions)
        # pdowork = PdoWork.objects.filter(id=work.first().pdowork.id)

        return JsonResponse({'district': list(district.values())}, safe=False)
    else:
        return HttpResponse(0)

# order
import json
def set_add_to_card(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id')
        lists = []
        if id:
            collection = Collection.objects.filter(id=id).first()
            if collection:
                products_sets = ProductSet.objects.filter(collection=collection).all()
                for i in products_sets:
                    # if i.product:
                    #     return HttpResponse(2)
                    # else:
                    orderstore = OrderStore(product=i.product, product_amount=i.product_amount)
                    orderstore.save()

                    product = Products.objects.filter(id=i.product.id)
                    lists.append(product)

        # orders = OrderStore.objects.all()
        # for i in orders:
        #     products = Products.objects.filter(id__in=i.product.id)
        # print(products)

        count = OrderStore.objects.all().count()
        costs = OrderStore.objects.all()
        cost = 0

        for i in costs:
            cost = cost + int(i.product.cost_discount)*int(i.product_amount)

        return JsonResponse({'product': json.dumps(lists, sort_keys=True), 'count': count, 'cost': cost}, safe=False)
    else:
        return HttpResponse(0)


def add_card(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id')
        if id:
            product = Products.objects.filter(id=id).first()
            if product:
                check = OrderStore.objects.filter(product=product).first()
                if check:
                    return HttpResponse(2)
                else:
                    orderstore = OrderStore(product=product)
                    orderstore.save()
        count = OrderStore.objects.all().count()
        costs = OrderStore.objects.all()
        cost = 0
        for i in costs:
            cost = cost + int(i.product.cost_discount)
        object = OrderStore.objects.filter(id=orderstore.id).first()
        product = Products.objects.filter(id=object.product.id)

        return JsonResponse({'product': list(product.values()), 'count': count, 'cost': cost}, safe=False)
        # return HttpResponse(1)
    else:
        return HttpResponse(0)

# order
def sets(request):
    products = Products.objects.order_by('-id').all()
    products_sets = ProductSet.objects.order_by('-id').all()
    collections = Collection.objects.order_by('-id').all()
    classess = Classes.objects.all()
    categories = Category.objects.all()
    ordersstore = OrderStore.objects.all()
    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories,'ordersstore':ordersstore}
    return render(request, 'index/products_sets.html', context)

def set_by_class(request,id):
    ordersstore = OrderStore.objects.all()
    collections = Collection.objects.filter(sinf=id).all()
    sinf = Classes.objects.filter(id=id).first()
    classes = Classes.objects.all()
    categories = Category.objects.all()
    context = {'collections':collections,'sinf':sinf,'categories':categories,'classess':classes,'ordersstore':ordersstore}
    return render(request, 'index/products_sets_by_class.html', context)

def show_set_product(request,id):
    ordersstore = OrderStore.objects.all()
    classes = Classes.objects.all()
    categories = Category.objects.all()

    collection = Collection.objects.filter(id=id).first()
    collections = Collection.objects.filter(~Q(id=id)).filter(name=collection.name)[:10]
    products = ProductSet.objects.filter(collection=collection).all()

    context = {'categories':categories, 'classess':classes, 'products':products, 'collection':collection, 'ordersstore':ordersstore, 'collections':collections}

    return render(request, 'index/show_set_product.html', context)

def show_product(request,id):
    ordersstore = OrderStore.objects.all()
    classes = Classes.objects.all()
    categories = Category.objects.all()
    product = Products.objects.filter(id=id).first()
    product.show=product.show+1
    product.save()
    products = Products.objects.filter(category=product.category).filter(~Q(id=id)).order_by('-id')[:10]
    context = {'product':product,'categories':categories,'classess':classes,'products':products,'ordersstore':ordersstore}
    return render(request, 'index/show_product.html', context)


def sets_list_view(request):
    categories = Category.objects.all()
    products = Products.objects.order_by('-id').all()
    products_sets = ProductSet.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    ordersstore = OrderStore.objects.all()
    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories,'ordersstore':ordersstore}
    return render(request, 'index/shop_list_sets.html', context)


def products_by_category(request,id):
    products = Products.objects.filter(category=id).all()
    one = Category.objects.filter(id=id).first()
    ordersstore = OrderStore.objects.all()
    categories = Category.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products': products, 'products_sets': products_sets, 'collections': collections, 'classess': classess,'ordersstore':ordersstore,
               'categories': categories,'one':one}
    return render(request, 'index/products_by_cetegory.html', context)


def products_lists_by_category(request,id):
    products = Products.objects.filter(category=id).all()
    one = Category.objects.filter(id=id).first()
    ordersstore = OrderStore.objects.all()
    categories = Category.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products': products, 'products_sets': products_sets, 'collections': collections, 'classess': classess,'ordersstore':ordersstore,
               'categories': categories, 'one': one}
    return render(request, 'index/products_lists_by_categoy.html', context)

def sale_products(request):
    categories = Category.objects.all()
    products = Products.objects.order_by('-id').filter(sale_status=1).all()
    ordersstore = OrderStore.objects.all()
    products_sets = ProductSet.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories,'ordersstore':ordersstore}
    return render(request, 'index/sale_product.html', context)

def new_products(request):
    categories = Category.objects.all()
    products = Products.objects.order_by('-id').all()
    ordersstore = OrderStore.objects.all()
    products_sets = ProductSet.objects.all()
    collections = Collection.objects.all()
    classess = Classes.objects.all()
    context = {'products':products,'products_sets':products_sets,'collections':collections,'classess':classess,'categories':categories,'ordersstore':ordersstore}
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

    context = {'products': products, 'all_products': all_products, 'collections':collections, 'classess':classess, 'counter': counter(request)}
    return render(request, 'admin_page/products_sets/product_sets.html', context)

@login_required(login_url='/sign_in')
def add_collection(request):

    classess = Classes.objects.all()
    collections = Collection.objects.all()
    products = ProductSet.objects.all()
    all_products = Products.objects.all()

    context = {'classess': classess, 'collections' :collections, 'products':products, 'all_products': all_products, 'counter': counter(request)}

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

        collections = Collection(sinf=cl, name=name, foto=foto, description=info, status=0)
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
            collection.cost_sell = int(str(collection.cost_sell))+int(product_amount)*int(str(pr.cost_sell))
        else:
            collection.cost_sell = int(product_amount)*int(pr.cost_sell)

        if collection.cost_buy:
            collection.cost_buy = int(str(collection.cost_buy))+int(product_amount)*int(str(pr.cost_buy))
        else:
            collection.cost_buy = int(product_amount)*int(pr.cost_buy)

        if collection.cost_discount:
            collection.cost_discount = int(str(collection.cost_discount))+int(product_amount)*int(str(pr.cost_discount))
        else:
            collection.cost_discount = int(product_amount)*int(pr.cost_discount)

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
        collection.cost_sell = int(str(collection.cost_sell)) - int(products_set.product_amount)*int(str(product.cost_sell))
    else:
        collection.cost_sell = ''

    if collection.cost_buy:
        collection.cost_buy = int(str(collection.cost_buy)) - int(products_set.product_amount)*int(str(product.cost_buy))
    else:
        collection.cost_buy = ''

    if collection.cost_discount:
        collection.cost_discount = int(str(collection.cost_discount)) - int(products_set.product_amount)*int(str(product.cost_discount))
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


@login_required(login_url='/sign_in')
def new_orders(request):
    orders = Order.objects.filter(~Q(status=2)).all()

    context = {'orders': orders,'counter': counter(request)}

    return render(request, 'admin_page/orders/orders.html', context)

@login_required(login_url='/sign_in')
def finished_orders(request):
    orders = Order.objects.filter(status=2).all()

    context = {'orders': orders,'counter': counter(request)}

    return render(request, 'admin_page/finished_orders/orders.html', context)

@login_required(login_url='/sign_in')
def show_order(request,id):

    user = Worker.objects.filter(id=id).first()
    orders = Order.objects.filter(~Q(status=2)).filter(user=user).all()
    costs = 0
    for i in orders:
        costs = costs + int(i.product.cost_discount)

    context = {'orders': orders,'counter': counter(request),'user':user,'costs':costs}

    return render(request, 'admin_page/orders/show.html', context)

@login_required(login_url='/sign_in')
def delete_order(request,id):

    user = Worker.objects.filter(id=id).first()
    orders = Order.objects.filter(user=user).all()
    for i in orders:
        i.delete()

    return HttpResponseRedirect('/new_orders')

@login_required(login_url='/sign_in')
def confirm_to_collect(request,id):

    user = Worker.objects.filter(id=id).first()
    orders = Order.objects.filter(user=user).all()
    for i in orders:
        i.status = 1
        i.save()

    return HttpResponseRedirect('/new_orders')

@login_required(login_url='/sign_in')
def confirm_order(request,id):

    user = Worker.objects.filter(id=id).first()
    orders = Order.objects.filter(user=user).all()

    for i in orders:
        i.status = 2
        product = Products.objects.filter(id=i.product.id).first()
        product.status_trent = product.status_trent + 1
        product.save()
        i.save()

    return HttpResponseRedirect('/new_orders')

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