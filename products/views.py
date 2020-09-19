from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product 
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError



def buscar(request):
	if "busca" in request.GET and request.GET["busca"]:
		consulta = request.GET["busca"]
		Products = Product.objects.filter(title__icontains=consulta)
		return render(request, 'products/resultados.html', {'res':Products})
	else:
		return render(request, 'products/resultados.html')	




def home(request):
	return render(request, 'products/home.html')

def imagenes(request):
	products = Product.objects
	return render(request, 'products/imagenes.html', {'products':products})

def nosotros(request):
	return render(request, 'products/nosotros.html')





@login_required(login_url="/accounts/signup")
def create(request):
	if request.method == 'POST':
		if request.POST['title'] and request.POST['body']:
			product = Product()
			try:
				fm = request.FILES['image']
			except MultiValueDictKeyError:
				return render(request, 'products/create.html',{'error': 'Icono o image  no es incorrecto'})
			product.title = request.POST['title']
			product.body = request.POST['body']
			#if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
			#	product.url = request.POST['title']
			#else:
			#	product.url = 'http://' + request.POST['url']
			product.pub_date = timezone.datetime.now()
			product.image = request.FILES['image']
			#product.icon = request.FILES['icon'] en caso de que quiera agerar un incono
			product.hunter = request.user
			product.save()
			return redirect('/products/' + str(product.id))
		else:
 			return render(request,'products/create.html'),{'error':'Todos los campos son necesarios'}
	else:
		return render(request, 'products/create.html')


def detail(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	return render (request, 'products/detail.html', {'product':product})
	

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
	if request.method == 'POST':
		product = get_object_or_404(Product, pk=product_id)
		product.votes_total += 1 
		product.save()
		return redirect('/products/' + str(product.id))