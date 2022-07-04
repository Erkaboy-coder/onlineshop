from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Worker)
admin.site.register(Region)
admin.site.register(Oblast)
admin.site.register(Classes)
admin.site.register(Collection)
admin.site.register(ProductSet)

admin.site.register(Products)

admin.site.register(OrderStore)
admin.site.register(Order)


