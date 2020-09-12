from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm
# Create your views here.
from products.models import Product


def user_login(request):
    '''Авторизация пользователя'''
    latest_products = Product.objects.order_by('name')[:3]

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                    request,
                    username=cd['username'],
                    password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('product-list')
                else:
                    return HttpResponse('Не активный аккаунт')
        else:
            return HttpResponse('Не правильный логин и пароль')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'latest_products': latest_products
    }
    return render(request, 'login.html', context)


def register(request):
    latest_products = Product.objects.order_by('name')[:3]

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', context={'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    context = {
        'user_form': user_form,
        'latest_products': latest_products

    }
    return render(request, 'register.html', context)