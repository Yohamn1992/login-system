from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Cria e retorna um usuário com email e senha."""
        if not email:
            raise ValueError('O email deve ser definido.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Usar set_password para criptografar a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria e retorna um superusuário com email e senha."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # E-mail único
    username = models.CharField(max_length=150, unique=True)  # Nome de usuário
    email_confirmado = models.BooleanField(default=False)  # Campo para confirmar o e-mail
    is_active = models.BooleanField(default=True)  # Para controlar se o usuário pode se autenticar
    is_staff = models.BooleanField(default=False)  # Se o usuário pode acessar o admin

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UsuarioManager()  # Usar o gerenciador customizado

    def __str__(self):
        return self.email
