from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    # re_path(r'^/$', views.index, name='index'),
    re_path(r'^sets/$', views.sets, name='sets'),
    re_path(r'^sets_list_view/$', views.sets_list_view, name='sets_list_view'),

    re_path(r'^set_by_class/(?P<id>\d+)/$', views.set_by_class, name='set_by_class'),
    re_path(r'^show_product/(?P<id>\d+)/$', views.show_product, name='show_product'),
    re_path(r'^show_set_product/(?P<id>\d+)/$', views.show_set_product, name='show_set_product'),

    re_path(r'^products_by_category/(?P<id>\d+)/$', views.products_by_category, name='products_by_category'),
    re_path(r'^products_lists_by_category/(?P<id>\d+)/$', views.products_lists_by_category, name='products_lists_by_category'),

    re_path(r'^sale_products/$', views.sale_products, name='sale_products'),
    re_path(r'^new_products/$', views.new_products, name='new_products'),

    re_path(r'^error_page/$', views.error_page, name='error_page'),
    re_path(r'^contact/$', views.contact, name='contact'),
    re_path(r'^show_product_list$', views.show_product_list, name='show_product_list'),

    # order
    re_path(r'^add_card$', views.add_card, name='add_card'),

    re_path(r'^order_store/$', views.order_store, name='order_store'),
    re_path(r'^delete_product_from_store/(?P<id>\d+)/$', views.delete_product_from_store, name='delete_product_from_store'),


    re_path(r'^login_page/$', views.login, name='login_page'),
    re_path(r'^admin_page/$', views.admin_page, name='admin_page'),
    re_path(r'^sign_in/$', views.sign_in, name='sign_in'),
    re_path(r'^logout/$', views.logout, name='logout'),

    re_path(r'^products/$', views.products, name='products'),
    re_path(r'^add_product/$', views.add_product, name='add_product'),
    re_path(r'^product_store/$', views.product_store, name='product_store'),
    re_path(r'^edit_product/(?P<id>\d+)/$', views.edit_product, name='edit_product'),
    re_path(r'^product_info_change/(?P<id>\d+)/$', views.product_info_change, name='product_info_change'),
    re_path(r'^delete_product/(?P<id>\d+)/$', views.delete_product, name='delete_product'),

    re_path(r'^products_sets/$', views.products_sets, name='products_sets'),
    re_path(r'^add_collection/$', views.add_collection, name='add_collection'),
    re_path(r'^collection_create/$', views.collection_create, name='collection_create'),
    re_path(r'^delete_collection/(?P<id>\d+)/$', views.delete_collection, name='delete_collection'),
    re_path(r'^product_add_to_collection/(?P<id>\d+)/$', views.product_add_to_collection, name='product_add_to_collection'),
    re_path(r'^delete_collection_product/(?P<id>\d+)/$', views.delete_collection_product, name='delete_collection_product'),
    re_path(r'^add_product_to_collection/$', views.add_product_to_collection, name='add_product_to_collection'),

    re_path(r'^app/static/(?P<path>.*)', serve, {'document_root': 'app/static/'}),
]
# handler404 = "views.error"
