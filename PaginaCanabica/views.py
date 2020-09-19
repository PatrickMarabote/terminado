from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render




def error_404(request, exception):
    response = render(request, '404.html', {})
    return response

def error_500(request):
    response = render(request, '500.html', {})
    return response

