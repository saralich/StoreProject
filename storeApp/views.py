from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import *
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.db.models import Max
import datetime
from django.contrib import auth

from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, SignInForm, ProductForm, DeleteAccountForm, UpdateAccountForm
from .models import User, Order, Supplier, Product

#@login_required(login_url='/login')
def homePage(request):
	homePage = loader.get_template('HomePage.html')
	context = RequestContext(request)
	return HttpResponse(homePage.render(context))

def contactPage(request):
	print('contact page made it')
	contactPage = loader.get_template('Contact.html')
	context = RequestContext(request)
	return HttpResponse(contactPage.render(context))

def productPage(request):
	#return HttpResponse("Webstore user account page")
	productPage = loader.get_template('Products.html')
	context = RequestContext(request)
	return HttpResponse(productPage.render(context))

def search(request):
	query = request.GET.get('q')
	try:
		query = str(query)
	except ValueError:
		query = None
		results = None
	if query:
		results = Product.objects.order_by('product_name')
		results = results.filter(**{'product_name__icontains':str(query)})
		results_by_price = Product.objects.order_by('product_price')
		results_by_price = results_by_price.filter(**{'product_name__icontains':str(query)})
	else:
		results = None
		results_by_price = None
	context = RequestContext(request)
	return render_to_response('Search.html',{'results':results, 'results_by_price':results_by_price}, context_instance = context)

#@login_required(login_url='/login')
def accountPage(request):
	accountPage = loader.get_template('UserAccount.html')
	context = RequestContext(request)
	return HttpResponse(accountPage.render(context))

def updateAccountPage(request):
	try:
		active = request.session['username']
	except KeyError:
		return loginPage(request)

	password = passwordCheck = email = address = ''
	#admin capabilities & normal users
	#if request.user.is_superuser or request.user.is_authenticated:
	if request.user.is_superuser or request.user.is_authenticated:
		#make sure they logged in
		currentUser = request.user;
		if currentUser.is_authenticated():

	#if request.user.is_authenticated:
		
			if request.method == 'POST':
				if 'updateAccount' in request.POST:
					form = UpdateAccountForm(request.POST)

					if form.is_valid():
						print('update form valid')
						password = request.POST.get('password')
						passwordCheck = request.POST.get('passwordCheck')
						email = request.POST.get('email')
						address = request.POST.get('address')
						print('Password was updated')
						print(email)
						print(address)
						user = authenticate(password = password, passwordCheck = passwordCheck, user_email = email, user_address = address)
						if password != passwordCheck:
							print('passwords didnt match')
							message = "Your passwords did not match, please re-enter matching passwords"
							return render(request, 'UpdateAccount.html',{'form':form,'state':message})
						else:
							print('information updated successfully')
							message = "Your information has been successfully updated"
							return render(request, 'UpdateAccount.html',{'form':form, 'state':message})
					else:
						print('else was triggered A')
						form = UpdateAccountForm()
						message = "Please Re-Enter information with correct values"
						return render(request, 'UpdateAccount.html',{'form':form, 'state':message})
				else:
					print('else was triggered B')
					form = UpdateAccountForm()
					return render(request, 'UpdateAccount.html', {'form':form})
			else:
				print('else was triggered C')
				form = UpdateAccountForm()
				return render(request, 'UpdateAccount.html', {'form':form})
		else:
			form = SignInForm()
			message = "You cannot update your account because you are not logged in!"
			return render(request, 'SignIn.html', {'form':form, 'state':message})


def changeOrder(request):
	#find the product the user wenats to order
	productName = request.GET.get('productName')
	validProduct = True

	try:
		productToBuy = Product.objects.get(product_name = productName)
	except:
		validProduct = False

	#checking to see if the store even carries that product
	if validProduct:
		enteredProducts = request.GET.get('orderList')

		if enteredProducts:
			temp = enteredProducts
			temp = temp.replace("'", "")
			productsInOrder = [e.encode('utf-8') for e in temp.strip('[]').split(',')];

			#for the initial list creation
			#anohter precaution in case 
			if 'None' in str(request.GET.get('orderList')):
				orderList = []

		else:
			#creates the initial list to hold the order
			orderList = []

	else:
		hi = request.GET.get('quantity')
		print('this is hi')
		print(hi)
		if not int(request.GET.get('quantity')) is 0:
			productsInOrder = None

		else:
			temp = request.GET.get('productsInOrder')
			temp = temp.replace("'", "")
			orderList = [e.encode('utf-8') for e in temp.strip('[]').split(',')]

	if validProduct:
	################### PART 2 ##################	
		#make sure they entered a valid quantity
		numToOrder = int(request.GET.get('quantity')) 
		
		#if there is at least one item already in the order
		if numToOrder is not 0:

			productsInOrder.append(str(productToBuy.product_name))
			quantity = int(request.GET.get('quantity')) + 1
			totalPrice = int(request.GET.get('price_of_order')) + productToAdd.product_price;
			message = "product added successfully"

		else: #this is the creation of an order
			productsInOrder.append(str(productToBuy.product_name))
			quantity = 1;
			totalPrice = productToBuy.product_price
			message = "product added successfully"

	else: 
		if numToOrder is not 0:
			totalPrice = request.GET.get('totalPrice')

			message = productName + "does not exist"

			temp = request.GET.get('orderList')
			temp = temp.replace("'", "")
			orderList = [e.encode('utf-8') for e in temp.strip('[]').split(',')]

		else:
			#defaults for blank/failed entries
			orderList = None
			totalPrice = 0
			quantity = 0
			message = "Your haven't ordered anything!"

	context = RequestContext(request)
	return render_to_response()


def makeOrder(request):
		#find the product the user wenats to order
	if request.user.is_authenticated():
		activeUser = request.user
		print(activeUser)
		orderList = request.GET.get('orderList')
		#Gets those products from the order
		if orderList:
			#stringOfProductIDs = request.GET.get('productsInOrderByID')
			#list of products
			productList = orderList.replace("[", "").replace("]","")
			specificOrder = []
			while "'" in productList:
				pIDinstance = find_between(productList, "'", "'")
				productIDsInOrder.append(Product.objects.get(product_id=pIDinstance))
				productList = Product.replace("'", "", 2);

		#temp order to be added
		newOrder = Order()
		#max + 1 of all current orders
		dictObject = Order.objects.all().aggregate(Max('order_id'))
		maxID = dictObject['order_id__max']
		if not maxID:
			maxID = 0;
		newOrder.order_id = int(maxID) + 1
		newOrder.order_date = str(datetime.date.today())
		newOrder.order_paid = request.GET.get('price_of_order')
		#get the username to compare
		activeUsername = activeUser.username
		print(activeUsername)
		newOrder.orders = User.objects.get(username = activeUsername)

		quantity = int(request.GET.get('quantity'))
		print('this is quantity value')
		print(quantity)
		orderContains = Contains.objects.create(quantity=quantity)
		stringOfProductIDs = request.GET.get('productsInOrderByID')
		#array of products, parsed from list
		arrayOfProductIDs = stringOfProductIDs.replace("[", "").replace("]","")

		# goes through products. It works, at least for one of them
		#works for all but one
		while "'" in productList:
			pIDinstance = find_between(productList, "'", "'")
			orderProduct = Product.objects.get(product_id=pIDinstance)
			productCount = orderProduct.product_stock_quantity
			# Decrement product quantity and check for low stock
			#productCount = orderProduct.get_field('product_stock_quantity')
			print("producCount: " + str(productCount))
			print("quantity: " + str(quantity))
			if quantity > productCount:
				print("Log: Error: no overselling allowed")
				state ="Insufficient product stock, please wait for staff to restock"
				email = EmailMessage(
					'Webstore: Product stock low',
					(str(orderProduct.product_name) + "stock count is low, please restock"),
					to = [str(request.session['email'])]
				)
				email.send()
				return render(request,"order.html",{"state":state})
			elif productCount < 10:
				# Send severe warning to staff 
				print("Log: severe warning")
			elif productCount < 100:
				# Send warning to staff
				print("Log: minor warning")

			#orderProduct = Product(product_id = int(pIDinstance),product_stock_quantity = int(productCount - 1))
			

			#Product.objects.filter(product_id=pIDinstance).update(product_stock_quantity = productCount - 1)
			orderProduct.product_stock_quantity = (productCount -1)
			orderProduct.save()
			print(Product.objects.get(product_id=pIDinstance).product_stock_quantity)

			orderContains.productsLONGNAME.add(orderProduct)
			arrayOfProductIDs = arrayOfProductIDs.replace("'", "", 2);

			orderProduct.save()

		orderContains.save()

		newOrder.contains = orderContains

		newOrder.save()	
	else:
		form = SignInForm()
		message = "you are not logged in, log in to make an order"
		return render(request, 'SignIn.html', {'state':message, 'form':form})

 
 	orders = Order.objects.order_by('-order_date').filter(orders__user_name__in = activeUser)
 	context = RequestContext(request)
	return render_to_response('orderPlaced.html', {"yourOrder" : newOrder, "productIDsInOrder" : productIDsInOrder, "orders" : orders, }, context_instance=context)#


def deleteAccount(request):
	try:
		active = request.session['username']
	except KeyError:
		return loginPage(request)

	#admin capabilities
	if request.user.is_superuser or request.user.is_authenticated:
		#make sure they logged in
		currentUser = request.user;
		if currentUser.is_authenticated():
			doubleCheck = ""

			if request.method == 'POST':
				form = DeleteAccountForm(request.POST)

				if form.is_valid():

					#doubleCheck should be the users password
					doubleCheck = request.POST.get('doubleCheck')

					#grab user we are deleting
					userToDelete = User.objects.get(username= currentUser.username)

					if doubleCheck == currentUser.password:
						message = "Successfully deleted account!"
						print("Account deleted")

						User.objects.filter(username = currentUser.username).delete()
						del request.session['username']
						return render(request, 'DeleteAccount.html', {'form': form, 'state':message})
					else:
						message = "Your password was entered incorrectly to delete your account"
						return render(request, 'DeleteAccount.html', {'form':form, 'state':message})
				else:
					print("delete account form was invalid")
					form = DeleteAccountForm()
					return render(request, 'DeleteAccount.html')
		else:
			form = SignInForm()
			message = "You cannot delete your account because you are not logged in!"
			return render(request, 'SignIn.html', {'form':form, 'state':message})

def logoutPage(request):
	try:
		del request.session['username']
		#logout(request)
		print("logout worked")
	except KeyError:
		print("etnered except")
		pass

	form = SignInForm()
	message = "You successfully logged out!"
	return render(request, 'SignIn.html', {'form':form, 'state':message})


def loginPage(request):
	#initialize 
	username = password = ''
	try:
			del request.session['username']
			del request.session['staff']
			del request.session['email']
	except KeyError:
		pass

	if request.method == 'POST':
		if 'loginUser' in request.POST:
			form = SignInForm(request.POST)

		#if i didnt screw up
			if form.is_valid():	
				print('login form valid')
				#grab the info from the html
				username = request.POST.get('username')
				password = request.POST.get('password')
				print(username)
				print(password)
				user = User.objects.get(username = username)
				#if User.objects.filter(username = username).exists()
				#user = auth.authenticate(username = "pocathoughts", password = "jkjkjkjk")
				print('this is username and password')
				print(user.password)
				print(password)
				if user:
					if user.password == password:
						message = "You've logged in!"
						request.session['staff']=user.user_is_staff
						request.session['username'] = user.username
						request.session['email'] = user.user_email
						#HttpResponseRedirect('HomePage.html')
						return render(request, 'UserAccount.html', {'state': message})
					else:
						#password doesnt match
						print('invalid password')
						message="Your password did not match your username"
						return render(request, "SignIn.html", {'form': form, 'state':message})
					#if user.is_active:
					#	login(request, user)
					#	return render(request, 'HomePage.html')
					#else:
					#	return HttpResponse("Your account is disabled")	
				else:
					message = "Invalid username."
					print("Invalid username")
					return render(request, 'SignIn.html', {'form':form, 'state':message})
			else:
				form = SignInForm()
				print('else was triggered')
		else:
			form = SignInForm()
			print('else was triggered')
	else:
		print('else was triggered')
		form = SignInForm()
	message = "Enter login information below"		
	return render(request, 'SignIn.html',{'form':form,'state':message})

def loadProducts(request):
	productID = productName = productDescr = '' #supplies = ''
	productPrice = productQuantity = active = 0

	if request.method == 'POST':
		print('we getting here?')
		form = ProductForm(request.POST)

		if form.is_valid():
			print('was the loadproudcts form valid?')
			productID = str(request.POST.get('product_id'))
			print('this is productId')
			print(productID)
			#update Product Values
			productName = str(request.POST.get('product_name'))
			productDescr = str(request.POST.get('product_description'))
			productPrice = int(request.POST.get('product_price'))
			active = bool(request.POST.get('product_active'))
			print(active)
			productQuantity = int(request.POST.get('product_stock_quantity'))
			#supplies = str(request.POST.get('productSupplier'))
			#
			newProduct = Product(product_id=productID, product_name=productName, product_active=active, product_stock_quantity=productQuantity,
				product_description=productDescr, product_price=productPrice)
			newProduct.save()
			return render(request, 'ProductLoaded.html');
		else:
			print('what am i even doing')
			form = ProductForm()

	else:
		form = ProductForm()
		print('nothing needs to be done yet')

	message = "Enter Registration Info below"
	return render(request, 'LoadProducts.html',{'form':form,'state':message})

def registerPage(request):
	#initialize these variables to be used
	username = fName = lName = password = passwordCheck = email = address =  ''
	
	#post send info, GET is like a search or query to pull up page from user
	if request.method == 'POST':
		print('is this even working?')
		if 'registerUser' in request.POST:
			print('is this even working too????')
			form = RegisterForm(request.POST, prefix = 'register')
		
			if form.is_valid():

				print('form is valid')
				enteredUsername = request.POST.get('register-username')
				print('this is enteredUsername')
				print(enteredUsername)
				enteredFName = request.POST.get('register-fName')
				print('this is firstname')
				print(enteredFName)
				enteredLName = request.POST.get('register-lName')

				#filter basically means like check or sift though
				if User.objects.filter(username = enteredUsername).exists():
					message = "This username is already associated with an account"
					print("this username is already associated with an account")
					return render(request, 'RegisterPage.html', {'form':form,'state':message})
				
				enteredEmail = request.POST.get('register-email')
				if User.objects.filter(user_email = enteredEmail).exists():
					message = "This email address is already associated with an account!"
					print("email address is already associated with an account")
					return render(request, 'RegisterPage.html',{'form':form,'state':message})

				enteredPassword = request.POST.get('register-password')
				enteredCheck = request.POST.get('register-passwordCheck')
				enteredAddress = request.POST.get('register-address')
				
				if enteredPassword != enteredCheck:
					print('passwords didnt match')
					message = "Your passwords did not match, please re-enter matching passwords"
					return render(request, 'RegisterPage.html',{'form':form,'state':message})

				#at this point all the chekcs were successful
				else:
					newUser = User(username = enteredUsername, user_firstname = enteredFName, user_lastname = enteredLName, password = enteredPassword, user_email = enteredEmail, user_address = enteredAddress)
					newUser.save()
					print("Account was successfully created!")
					message = "Account was successfully created!"
					return render(request, 'SignIn.html',{'form':form,'state':message})
			else:
				print('form was invalid?');
				form = RegisterForm(prefix='register')
		else:
			print('was this form invalid')
			form = RegisterForm(prefix='register')
	else:
		print('form was invlaid?')
		form = RegisterForm(prefix = 'register')
		
	message = "Enter Registration Info below"
	return render(request, 'RegisterPage.html',{'form':form,'state':message})
