from django.shortcuts import render, redirect
from item.models import Category, Item
from django.contrib.auth import logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from item.models import Review
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories' : categories,
        'items' : items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

@user_passes_test(lambda u: u.is_anonymous)
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            review = Review.objects.create(user = user)
            review.save()
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form':form
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:index')