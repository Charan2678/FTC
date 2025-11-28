from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import product
from django.contrib import messages
from django.db import connection
from FTC.utils import getDropDown, dictfetchall
import datetime

# Create your views here.
def orderlisting(request):
    cursor = connection.cursor()
    if (request.session.get('user_level_id', None) == 1):
        SQL = "SELECT * FROM `order`,`users_user`,`order_status` WHERE order_status = os_id AND order_user_id = user_id"
    else:
        customerID = str(request.session.get('user_id', None))
        SQL = "SELECT * FROM `order`,`users_user`,`order_status` WHERE order_status = os_id AND order_user_id = user_id AND user_id = " + customerID
    cursor.execute(SQL)
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Product #
    context['heading'] = "Order Reports";
    return render(request, 'order-listing.html', context)

# Create your views here.
def productlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id")
    productlist = dictfetchall(cursor)

    context = {
        "productlist": productlist
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'products-listing.html', context)

# Create your views here.
def payment(request):
    from FTC.email_utils import send_order_notification_to_admin, send_order_confirmation_to_customer
    from datetime import datetime
    
    orderID = request.session.get('order_id', None);
    userID = request.session.get('user_id', None);
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(oi_total) as TotalCartValue FROM order_item WHERE oi_order_id = " + str(orderID))
    orderTotal = dictfetchall(cursor)
    
    # Get user address details
    cursor.execute("""SELECT u.*, c.city_name, s.state_name, co.country_name 
                      FROM users_user u 
                      LEFT JOIN users_city c ON u.user_city = c.city_id 
                      LEFT JOIN users_state s ON u.user_state = s.state_id 
                      LEFT JOIN users_country co ON u.user_country = co.country_id 
                      WHERE u.user_id = """ + str(userID))
    userDetails = dictfetchall(cursor)
    
    context = {
        "orderTotal": orderTotal[0],
        "userDetails": userDetails[0] if userDetails else None
    }
    
    if (request.method == "POST"):
        # Get payment method
        payment_method = request.POST.get('payment_method', 'card')
        payment_method_text = 'Cash on Delivery' if payment_method == 'cod' else 'Online Payment'
        
        # Prepare order details for email
        if userDetails:
            user = userDetails[0]
            delivery_address = f"{user['user_name']}\n{user['user_add1']}\n{user['user_add2']}\n{user['city_name']}, {user['state_name']}\n{user['country_name']}\nMobile: {user['user_mobile']}"
            
            order_details = {
                'order_id': orderID,
                'customer_name': user['user_name'],
                'customer_email': user['user_email'],
                'customer_mobile': user['user_mobile'],
                'order_total': orderTotal[0]['TotalCartValue'],
                'payment_method': payment_method_text,
                'order_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'delivery_address': delivery_address,
                'status': 'Pending Confirmation'
            }
            
            # Send email to admin
            try:
                print("🔄 Attempting to send admin notification...")
                send_order_notification_to_admin(order_details)
                print("✅ Admin notification function called successfully")
            except Exception as e:
                print(f"❌ Error sending admin notification: {str(e)}")
            
            # Send confirmation email to customer
            try:
                print("🔄 Attempting to send customer confirmation...")
                send_order_confirmation_to_customer(order_details)
                print("✅ Customer confirmation function called successfully")
            except Exception as e:
                print(f"❌ Error sending customer confirmation: {str(e)}")
            
            messages.add_message(request, messages.SUCCESS, 
                f"Order placed successfully! Order ID: #{orderID}. Confirmation email sent to {user['user_email']}")
        else:
            print("⚠️ WARNING: No user details found - emails not sent")
        
        request.session['order_id'] = "0"
        return redirect('order-items/'+str(orderID))
    
    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'payment.html', context)

# Create your views here.
def cancel_order(request, orderID):
    cursor = connection.cursor()
    cursor.execute("""
                UPDATE `order`
                SET order_status= '5' WHERE order_id = %s
            """, (
        orderID
    ))
    messages.add_message(request, messages.INFO, "Your order has been cancelled successfully !!!")
    return redirect('orderlisting')

# Create your views here.
def order_items(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    productlist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerOrderDetails = dictfetchall(cursor)
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "productlist": productlist,
        "customerOrderDetails": customerOrderDetails[0],
        "totalCost":totalCost[0]
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'order-items.html', context)

# Create your views here.
def order_edit(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    productlist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerOrderDetails = dictfetchall(cursor)
    customerOrderDetails = customerOrderDetails[0]
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "productlist": productlist,
        "protypelist":getDropDown('order_status', 'os_id', 'os_title', customerOrderDetails['order_status'], '1'),
        "customerOrderDetails": customerOrderDetails,
        "totalCost":totalCost[0]
    }
    if (request.method == "POST"):
        from FTC.email_utils import send_order_status_update_to_customer
        
        new_status_id = request.POST['order_status']
        order_id = request.POST['order_id']
        
        cursor = connection.cursor()
        cursor.execute("""
                    UPDATE `order`
                    SET order_status= %s WHERE order_id = %s
                """, (
            new_status_id,
            order_id
        ))
        
        # Get the status name and customer details for email
        cursor.execute("SELECT os_title FROM order_status WHERE os_id = " + str(new_status_id))
        status_result = dictfetchall(cursor)
        status_name = status_result[0]['os_title'] if status_result else 'Updated'
        
        # Get customer details and order info
        cursor.execute("""SELECT o.*, u.user_name, u.user_email, u.user_add1, u.user_add2, 
                          c.city_name, s.state_name, co.country_name 
                          FROM `order` o 
                          JOIN users_user u ON o.order_user_id = u.user_id 
                          LEFT JOIN users_city c ON u.user_city = c.city_id 
                          LEFT JOIN users_state s ON u.user_state = s.state_id 
                          LEFT JOIN users_country co ON u.user_country = co.country_id 
                          WHERE o.order_id = """ + str(order_id))
        order_info = dictfetchall(cursor)
        
        if order_info:
            order = order_info[0]
            delivery_address = f"{order['user_name']}\n{order['user_add1']}\n{order['user_add2']}\n{order['city_name']}, {order['state_name']}\n{order['country_name']}"
            
            order_details = {
                'order_id': order_id,
                'customer_name': order['user_name'],
                'customer_email': order['user_email'],
                'order_total': order['order_total'],
                'order_date': order['order_date'],
                'delivery_address': delivery_address
            }
            
            # Send status update email to customer
            send_order_status_update_to_customer(order_details, status_name)
        
        messages.add_message(request, messages.SUCCESS, f"Order status updated to '{status_name}' successfully! Customer has been notified via email.")
        return redirect('orderlisting')
    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'order-edit.html', context)

# Create your views here.
def cart_listing(request):
    orderID = request.session.get('order_id', None);
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    productlist = dictfetchall(cursor)
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `products_product`, `order`, order_item, company, type WHERE product_id =  oi_product_id AND oi_order_id = order_id AND company_id = product_company_id AND type_id = product_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "productlist": productlist,
        "totalCost":totalCost[0]
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'carts.html', context)

# Create your views here.
def products(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id")
    productlist = dictfetchall(cursor)

    context = {
        "productlist": productlist
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'products.html', context)

# Create your views here.
def product_filter(request, typeID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id AND type_id = "+ str(typeID))
    productlist = dictfetchall(cursor)

    context = {
        "productlist": productlist
    }

    # Message according Product #
    context['heading'] = "Products Details";
    return render(request, 'products.html', context)

def update(request, productId):
    productdetails = product.objects.get(product_id=productId)
    context = {
        "fn": "add",
        "procompanylist":getDropDown('company', 'company_id', 'company_name', productdetails.product_company_id, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name', productdetails.product_type_id, '1'),
        "productdetails":productdetails
    }
    if (request.method == "POST"):
        try:
            product_image = None
            product_image = productdetails.product_image
            if(request.FILES and request.FILES['product_image']):
                productImage = request.FILES['product_image']
                fs = FileSystemStorage()
                filename = fs.save(productImage.name, productImage)
                product_image = fs.re_path(productImage)

            addProduct = product(
            product_id = productId,
            product_name = request.POST['product_name'],
            product_type_id = request.POST['product_type_id'],
            product_company_id = request.POST['product_company_id'],
            product_price = request.POST['product_price'],
            product_image = product_image,                  
            product_description = request.POST['product_description'],
            product_stock = request.POST['product_stock'])
            addProduct.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["productdetails"] = product.objects.get(product_id = productId)
        messages.add_message(request, messages.INFO, "Product updated succesfully !!!")
        return redirect('productlisting')

    else:
        return render(request,'products-add.html', context)

def product_details(request, productId):
    if(request.session.get('authenticated', False) == False):
        messages.add_message(request, messages.ERROR, "Login to your account, to buy the product !!!")
        return redirect('/users')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM products_product, company, type WHERE company_id = product_company_id AND type_id = product_type_id AND product_id = "+productId)
    productdetails = dictfetchall(cursor)

    context = {
        "fn": "add",
        "productdetails":productdetails[0]
    }
    if (request.method == "POST"):
        try:
            if(request.session.get('order_id', None) == "0" or request.session.get('order_id', False) == False):
                customerID = request.session.get('user_id', None)
                orderDate = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                cursor = connection.cursor()
                cursor.execute("""
                INSERT INTO `order`
                SET order_user_id=%s, order_date=%s, order_status=%s, order_total=%s
                """, (
                    customerID,
                    orderDate,
                    1,
                    0))
                request.session['order_id'] = cursor.lastrowid    
            
            orderID = request.session.get('order_id', None);
            cursor = connection.cursor()
            totalAmount = int(request.POST['product_price']) * int(request.POST['product_quantity']);
            cursor.execute("""
            INSERT INTO order_item
            SET oi_order_id=%s, oi_product_id=%s, oi_price_per_unit=%s, oi_cart_quantity=%s, oi_total=%s
        """, (
            orderID,
            request.POST['product_id'],
            request.POST['product_price'],
            request.POST['product_quantity'],
            totalAmount))
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["productdetails"] = product.objects.get(product_id = productId)
        messages.add_message(request, messages.INFO, "Product updated succesfully !!!")
        return redirect('products:cart_listing')
    else:
        return render(request,'products-details.html', context)

def add(request):
    context = {
        "fn": "add",
        "procompanylist":getDropDown('company', 'company_id', 'company_name',0, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name',0, '1'),
        "heading": 'Product add'
    }
    if (request.method == "POST"):
        try:
            product_image = None

            if(request.FILES and request.FILES['product_image']):
                productImage = request.FILES['product_image']
                fs = FileSystemStorage()
                filename = fs.save(productImage.name, productImage)
                product_image = fs.url(productImage)

            addProduct = product(product_name = request.POST['product_name'],
            product_type_id = request.POST['product_type_id'],
            product_company_id = request.POST['product_company_id'],
            product_price = request.POST['product_price'],
            product_image = product_image,                  
            product_description = request.POST['product_description'],
            product_stock = request.POST['product_stock'])
            addProduct.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('productlisting')

    else:
        return render(request,'products-add.html', context)

def delete_item(request, itemId):
    cursor = connection.cursor()
    sql = 'DELETE FROM order_item WHERE oi_id=' + itemId
    cursor.execute(sql)
    return redirect('products:cart_listing')

def delete(request, prodId):
    try:
        deleteProduct = product.objects.get(product_id = prodId)
        deleteProduct.delete()
    except Exception as e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))
    messages.add_message(request, messages.INFO, "Product Deleted Successfully !!!")
    return redirect('productlisting')

def stock(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM stock, products_product WHERE product_id = stock_product_id")
    stocklist = dictfetchall(cursor)

    context = {
        "stocklist": stocklist
    }

    # Message according Product #
    context['heading'] = "Products Stock Details";
    return render(request, 'stock.html', context)

def deletestock(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM stock WHERE stock_id=' + id
    cursor.execute(sql)
    return redirect('stock')

def companylisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM company")
    companylist = dictfetchall(cursor)

    context = {
        "companylist": companylist
    }

    # Message according Product #
    context['heading'] = "Products Company";
    return render(request, 'viewcompany.html', context)

def deletecompany(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM company WHERE company_id=' + id
    cursor.execute(sql)
    return redirect('company')

def addcompany(request):
    context = {
        "fn": "add",
        "heading": 'Add Company'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO company
		   SET company_name=%s
		""", (
            request.POST['company_name']))
        return redirect('companylisting')
    return render(request, 'addcompany.html', context)

def order(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM order_item")
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Orders #
    context['heading'] = "Products Order Details";
    return render(request, 'orders.html', context)


def email_test_page(request):
    """Email notification test page"""
    return render(request, 'order_email_test.html')
