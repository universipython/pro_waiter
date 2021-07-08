from django.contrib.auth.views import LoginView

class LoginUsuario(LoginView):
    template_name = 'usuarios/entrar.html'
