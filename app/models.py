from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import Group

User = settings.AUTH_USER_MODEL
from datetime import datetime, date, timezone


class BaseModel(models.Model):
    def save(self, *args, full_clean=True, **kwargs):
        if full_clean:
            self.full_clean()
            super().save(*args, **kwargs)

    class Meta(object):
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status_category = (
        ('0', '1-Toifa'),
        ('1', '2-Toifa'),
        ('2', '3-Toifa'),
    )
    status = models.CharField(verbose_name='status_category', default='0', max_length=10, choices=status_category)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Oblast(models.Model):
    ordernumber = models.IntegerField(null=True, blank=True)
    shortname = models.CharField(max_length=100, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = "Oblast"


class Region(models.Model):
    oblast = models.ForeignKey(Oblast, blank=True, null=True, on_delete=models.CASCADE, related_name='oblast')
    ordernumber = models.IntegerField(null=True, blank=True)
    shortname = models.CharField(max_length=100, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = "Region"


class Classes(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"


class Products(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='productcategory')
    name = models.CharField(max_length=100, null=True, blank=True)
    cost_buy = models.CharField(max_length=100, null=True, blank=True)
    cost_sell = models.CharField(max_length=100, null=True, blank=True)
    cost_discount = models.CharField(max_length=100, null=True, blank=True)
    discount_persents = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    foto = models.FileField("Foto", upload_to='app/static/photos/', blank=True)
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0, blank=True)
    status_trent = models.IntegerField(default=0, blank=True)
    show = models.IntegerField(default=0, blank=True)
    order_amount = models.IntegerField(default=0, blank=True)
    sale_status = models.IntegerField(default=0, blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    amount_status = (
        ('0', 'Dona'),
        ('1', 'Pachka'),
    )
    amount = models.CharField(verbose_name='amount', default='0', max_length=10, choices=amount_status)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"

class Collection(models.Model):
    sinf = models.ForeignKey(Classes, blank=True, null=True, on_delete=models.CASCADE, related_name='sinf')
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    foto = models.FileField("Foto", upload_to='app/static/sets/', blank=True)
    description = models.TextField(blank=True)
    number = models.IntegerField(default=0, blank=True)
    cost_buy = models.CharField(max_length=100, null=True, blank=True)
    cost_sell = models.CharField(max_length=100, null=True, blank=True)
    cost_discount = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(default=0, blank=True)
    amount = models.IntegerField(default=0, blank=True)
    persentage = models.IntegerField(default=0, blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Collections"

class ProductSet(models.Model):
    product = models.ForeignKey(Products, blank=True, null=True, on_delete=models.CASCADE,related_name='productset')
    collection = models.ForeignKey(Collection, blank=True, null=True, on_delete=models.CASCADE,related_name='productcollection')
    product_amount = models.IntegerField(default=1, blank=True)
    info = models.TextField(blank=True)
    status = models.IntegerField(default=0, blank=True)
    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name_plural = "ProductSet"

class OrderStore(models.Model):
    product = models.ForeignKey(Products, blank=True, null=True, on_delete=models.CASCADE, related_name='productstore')
    collection = models.ForeignKey(Collection, blank=True, null=True, on_delete=models.CASCADE, related_name='productcollectionstore')

    product_amount = models.IntegerField(default=1, blank=True)
    status = models.IntegerField(default=0, blank=True)
    # status = 0 bolsa bu karzinkada turgan mahsulot hisoblanadi

    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name_plural = "OrderStore"



class Worker(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='admin', on_delete=models.PROTECT,
        verbose_name="Related user",
        help_text="User linked to this admin")

    firstname = models.CharField(verbose_name="firstname",null=True, max_length=256)
    lastname = models.CharField(verbose_name="lastname",null=True, max_length=256)

    permission = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email', default='', max_length=250, blank=True)
    email_check = models.BooleanField(default=False)
    contact = models.CharField(verbose_name='contact', default='', max_length=250, blank=True)
    status_worker = (
        ('0', 'User'),
        ('1', 'Admin'),
        ('2', 'SuperAdmin'),
    )
    status = models.CharField(verbose_name='User', default='0', max_length=10, choices=status_worker)

    live_admin = (
        ('0', 'Faol emas'),
        ('1', 'Faol'),
    )
    live = models.CharField(verbose_name='faol', default='0', max_length=10, choices=live_admin)

    class Meta(object):
        verbose_name = "Worker"
        verbose_name_plural = "Workers"


    def __str__(self):
        return self.firstname

class Order(models.Model):
    user = models.ForeignKey(Worker, blank=True, null=True, on_delete=models.CASCADE, related_name='workerorder')
    product = models.ForeignKey(Products, blank=True, null=True, on_delete=models.CASCADE, related_name='productorder')
    collection = models.ForeignKey(Collection, blank=True, null=True, on_delete=models.CASCADE, related_name='productcollectionorder')
    address = models.CharField(verbose_name="address", null=True, max_length=256)
    region = models.CharField(verbose_name="region", null=True, max_length=256)
    payment_method = models.IntegerField(default=1, blank=True)

    product_amount = models.IntegerField(default=1, blank=True)
    status = models.IntegerField(default=0, blank=True)
    # status = 0 bolsa bu karzinkada turgan mahsulot hisoblanadi

    active_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name_plural = "Order"