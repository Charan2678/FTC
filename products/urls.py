from django.urls import include, re_path 
from . import views
from . import order_views
from . import email_diagnostic_view

app_name = 'products'

urlpatterns = [
    re_path(r'^$', views.products, name="products"),
    re_path(r'^filters/(?P<typeID>\w{0,50})/$', views.product_filter, name="product_filter"),
    re_path(r'^product-listing$', views.productlisting, name="productlisting"),
    re_path(r'^payment$', views.payment, name="payment"),
    re_path(r'^cart_listing$', views.cart_listing, name="cart_listing"),
    re_path(r'^order-listing$', views.orderlisting, name="orderlisting"),
    re_path(r'^order-items/(?P<orderID>\w{0,50})/$', views.order_items, name="order_items"),
    re_path(r'^order-edit/(?P<orderID>\w{0,50})/$', views.order_edit, name="order_edit"),
    re_path(r'^order-cancel/(?P<orderID>\w{0,50})/$', views.cancel_order, name="cancel_order"),
    re_path(r'^add/', views.add, name="add"),
    re_path(r'^product-details/(?P<productId>\w{0,50})/$', views.product_details, name="product_details"),
    re_path(r'^update/(?P<productId>\w{0,50})/$', views.update, name="update"),
    re_path(r'^cart-delete/(?P<itemId>\w{0,50})/$', views.delete_item, name="delete_item"),
    re_path(r'^delete/(?P<prodId>\w{0,50})/$', views.delete, name="delete"),
    re_path(r'^stock$', views.stock, name="stock"),
    re_path(r'^deletestock/(?P<id>\w{0,50})/$', views.deletestock, name="deletestock"),
    re_path(r'^order$', views.order, name="order"),
    re_path(r'^companylisting$', views.companylisting, name="companylisting"),
    re_path(r'^addcompany$', views.addcompany, name="addcompany"),
    re_path(r'^deletecompany/(?P<id>\w{0,50})/$', views.deletecompany, name="deletecompany"),
    
    # New Order System with Email Notifications
    re_path(r'^place-order/$', order_views.place_order, name="place_order"),
    re_path(r'^order-confirmation/(?P<order_id>\d+)/$', order_views.order_confirmation, name="order_confirmation"),
    re_path(r'^api/quick-order/$', order_views.quick_order_api, name="quick_order_api"),
    re_path(r'^update-order-status/(?P<order_id>\d+)/$', order_views.update_order_status, name="update_order_status"),
    re_path(r'^admin/orders/$', order_views.order_list, name="admin_orders"),
    re_path(r'^my-orders/$', order_views.customer_orders, name="my_orders"),

    re_path(r'^email-test-page/$', views.email_test_page, name="email_test_page"),
    re_path(r'^email-diagnostics/$', email_diagnostic_view.email_diagnostic_view, name="email_diagnostics"),
    re_path(r'^test-email/$', email_diagnostic_view.email_diagnostic_view, name="test_email"),



]
