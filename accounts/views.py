from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView



from .forms import LoginForm, ProfileForm, RegisterForm
from .models import User


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        user = form.save()
        send_welcome_email(user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("login")


class LoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class ProfileView(DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"  # Используем это имя в шаблоне

    def get_object(self):
        # Получаем параметр username из URL и находим пользователя
        username = self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем другие данные в контекст, если нужно
        return context


class ProfileEditView(UpdateView):
    form_class = ProfileForm
    template_name = "accounts/profile_form.html"

    def get_success_url(self):
        return reverse_lazy("profile")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Профиль успешно обновлён!")
        return super().form_valid(form)

    def get_object(self):
        return self.request.user


class ProfileDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("home")

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        messages.success(self.request, "Профиль успешно удалён!")
        return super().delete(request, *args, **kwargs)

class PasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    success_url = reverse_lazy("password_reset_done")
    email_template_name = "accounts/password_reset_email.html"


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"



def send_welcome_email(user: User):
    subject = "Добро пожаловать в MahiruStore!"
    message = """
    Спасибо, что присоединились к MahiruStore! Мы рады приветствовать вас в нашем сообществе.

    Вы теперь можете наслаждаться всеми преимуществами нашего магазина, включая:
    - Просмотр и покупку самых популярных товаров в различных категориях.
    - Легкость поиска нужных товаров благодаря удобной навигации по каталогу.
    - Получение эксклюзивных предложений и акций только для зарегистрированных пользователей.

    Чтобы начать, вы можете посетить наш каталог товаров по следующей ссылке:
    https://localhost:8000/catalogs

    Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться к нашей службе поддержки:
    - Email: support@mahirustore.com
    - Телефон: +7(123)456-78-90

    С уважением,
    Команда MahiruStore
    """

    # Email settings from settings.py should be configured
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # from email
        [user.email],  # recipient list
    )
