from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import *
from django.views.generic import FormView
from django.core.urlresolvers import reverse

from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, SignInForm, ProductForm
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

def browse(request):

	itemList = Product.objects.order_by('product_id')
	itemPriceList = Product.objects.order_by('product_price')
	productPage = loader.get_template('Products.html')
	context = RequestContext(request, {
		'product_list': itemList,
		'price_sorted_product_list': itemPriceList,
		})
	return HttpResponse(productPage.render(context))


#@login_required(login_url='/login')
def accountPage(request):
	homePage = loader.get_template('SignIn.html')
	context = RequestContext(request)
	return HttpResponse(homePage.render(context))

def updateAccountPage(request):
	homePage = loader.get_template('SignIn.html')
	context = RequestContext(request)
	return HttpResponse(homePage.render(context))

def deleteAccountPage(request):
	homePage = loader.get_template('SignIn.html')
	context = RequestContext(request)
	return HttpResponse(homePage.render(context))

def logoutPage(request):
	try:
		del request.session['username']
	except KeyError:
		pass
	return HttpResponse("You're logged out.")


def loginPage(request):
	#initialize 
	username = password = ''

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
				user = authenticate(username = username, password = password)

				if user:

					if user.is_active:
						login(request, user)
						return render(request, 'HomePage.html')
					else:
						return HttpResponse("Your account is disabled")
				#check and see if the username is valid before moving forward
				#if User.objects.filter(user_name = username).exists():
					#if it exists pull it from the database
				#	specificUser = User.objects.get(user_name = username)

					#check to see if the passwrods match up
				#	if specificUser.user_password == password:
				#		message = "You successfully logged in!"
				#		request.session['username'] = specificUser.user_name
				#		print('Login successful')
						#need to authenticate beforehand
						#login(request, specificUser)
				#		return render(request, 'HomePage.html')
				#	else:
				#		message = "Incorrect username and password!"
				#		print("Incorrect username and password!")	
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
			productID = str(request.POST.get('productID'))
			print('this is productId')
			print(productID)
			#update Product Values
			productName = str(request.POST.get('productName'))
			productDescr = str(request.POST.get('productDescription'))
			productPrice = int(request.POST.get('productPrice'))
			active = bool(request.POST.get('productActive'))
			print(active)
			productQuantity = int(request.POST.get('productQuantity'))
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