from django.shortcuts import render
from .models import Page
from django.http import Http404
# Create your views here.
def index(request):

    pages = Page.objects.all().order_by('-id')
    context = {
        "pages": pages
    }
    return render(request, 'pages/index.html',context)

def about(request):
    return render(request, 'pages/about.html')

def courses(request,pk):
    try:
        course = Page.objects.get(pk=pk)
    except Page.DoesNotExist:
        raise Http404("Course not found")
    context = {
        "course": course
    }
    return render(request, 'pages/courses.html',context=context)