from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm
# Create your views here.

def user_login(request):
    '''Авторизация пользователя'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                    request,
                    username=cd['username'],
                    password=cd['password'])
            if user is not None:
                if user.is_valid():
                    user_login(request, user)
                    return HttpResponse('Вы успешно вошли в ваш аккаунт')
                else:
                    return HttpResponse('Не активный аккаунт')
        else:
            return HttpResponse('Не правильный логин и пароль')
    else:
        form = LoginForm()
    return render(request, 'register.html', {'form': form})