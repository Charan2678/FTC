# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register existing models
admin.site.register(product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
