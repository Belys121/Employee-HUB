from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from viewer.forms import SignUpForm


class SignUpView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Displays a form for users to log in to the account.
    """
    template_name = 'forms/form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    permission_required = "viewer.view_userprofile"


class SubmittableLoginView(LoginView):
    """
    Custom login view.
    """
    template_name = 'registration/login.html'


class SubmittablePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Form for password change.
    """
    template_name = 'forms/form.html'
    success_url = reverse_lazy('homepage')