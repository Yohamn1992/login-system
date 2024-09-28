from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from .models import Usuario  # Certifique-se de que você importou o modelo correto

def home(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autentica o usuário após o registro
            return redirect('login')  # Redireciona para a página de login
    else:
        form = UserRegistrationForm()
    return render(request, 'user/home.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            usuario = authenticate(request, email=email, password=senha)
            if usuario is not None:
                login(request, usuario)
                return redirect('confirmacao_login')  # Redireciona para a página de confirmação
            else:
                form.add_error(None, 'E-mail ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

def confirmacao_login(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém a sessão ativa após a mudança de senha
            messages.success(request, 'Sua senha foi alterada com sucesso! Agora você pode logar novamente.')
            return render(request, 'user/confirmacao_login.html', {'form': form, 'redirect': True})
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user/confirmacao_login.html', {'form': form})

def alterar_login(request):
    if request.method == 'POST':
        novo_login = request.POST.get('novo_login')
        if novo_login:
            # Verifica se o novo e-mail já está em uso
            if Usuario.objects.filter(email=novo_login).exists():
                messages.error(request, 'Este e-mail já está em uso. Tente outro.')
            else:
                request.user.email = novo_login
                request.user.save()
                messages.success(request, 'Seu e-mail foi alterado com sucesso! Agora você pode logar novamente.')
                return render(request, 'user/confirmacao_login.html', {'redirect': True})
    return render(request, 'user/confirmacao_login.html')

