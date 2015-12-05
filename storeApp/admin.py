from django.contrib import admin

from .models import User
from .models import Order
from .models import Product
from .models import Supplier

#class SignUpAdmin(admin.ModelAdmin):
#	class Meta:
#		model = SignUp

#admin.site.register(User, SignUpAdmin)
admin.site.register(User)

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Supplier)
