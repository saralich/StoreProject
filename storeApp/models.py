from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
#user entity
class User(models.Model):
	user_id = models.AutoField(primary_key=True, blank = False)
	def __unicode__(self):
		return self.user_id
	user_firstname = models.CharField(max_length=50, blank = False)
	def __unicode__(self):
		return self.user_firstname
	user_lastname = models.CharField(max_length=50, blank = False)
	def __unicode__(self):
		return self.user_lastname
	password = models.CharField(max_length=20, 
		blank = False, 
		validators=[MinLengthValidator(8, "Your password must contain at least 8 characters.")],)
	def __unicode__(self):
		return self.password
	user_address = models.CharField(max_length=50, blank = False)
	def __unicode__(self):
		return self.user_address
	user_email = models.CharField(max_length=30, blank = False)
	def __unicode__(self):
		return self.user_email
	username = models.CharField(max_length=50, blank=False)
	def __unicode__(self):
		return self.username
	user_is_staff = models.BooleanField(default=True, blank = False)
	
	pass

#supplier entity
class Supplier(models.Model):
	supplies_id = models.AutoField(primary_key=True)
	def __unicode__(self):
		return self.supplies_id
	supplier_name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.supplier_name

	pass
	#product = models.ManyToManyField(Product)




#product entity
class Product(models.Model):
	product_id = models.AutoField(primary_key=True)
	def __unicode__(self):
		return self.product_id
	product_price = models.IntegerField()
	def __unicode__(self):
		return self.product_price
	product_stock_quantity = models.IntegerField()
	def __unicode__(self):
		return self.product_stock_quantity
	product_description = models.CharField(max_length=400)
	def __unicode__(self):
		return self.product_description
	product_active = models.BooleanField(default=False)
	def __unicode__(self):
		return self.product_active
	#order = models.ManyToManyField(Order)
	#def __str__(self):
	#	return self.order
	#orders = models.ForeignKey(Order, editable=False, default = 1)
	#def __unicode__(self):
	#	return '%s' % (self.orders) 
	product_name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.product_name
	supplier = models.ForeignKey(Supplier)
	def __unicode__(self):
		return '%s' % (self.supplier_id)
	#contains = models.ForeignKey(Contains, editable=False, default = 1)
	#def __unicode__(self):
	#	return '%s' % (self.contains)

	pass



class Contains(models.Model):
	stock = models.IntegerField()
	def __unicode__(self):
		return self.stock
	products = models.ManyToManyField(Product)
	def __unicode__(self):
		return '%s' % (self.products)

#order entity
class Order(models.Model):
	contains = models.ForeignKey(Contains, null=True, blank = True)
	def __unicode__(self):
		return '%s' % (self.contains)

	order_date = models.DateField()
	def __unicode__(self):
		return self.order_date
	order_paid = models.DecimalField(max_digits = 19, decimal_places= 2)
	def __unicode__(self):
		return self.order_paid
	orders = models.ForeignKey(User, editable = False, default = 1)
	def __str__(self):
		return '%s' % (self.orders)
	order_id = models.AutoField(primary_key=True)
	def __unicode__(self):
		return self.order_id
	pass