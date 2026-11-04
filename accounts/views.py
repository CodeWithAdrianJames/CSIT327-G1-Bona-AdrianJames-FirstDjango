from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm, ProfileUpdateForm


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = "Account created successfully! You can now log in."


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "registration/profile_form.html"
    success_url = reverse_lazy("dashboard")
    success_message = "Your profile was updated successfully."

    def get_object(self, queryset=None):
        # Always the logged-in user; no pk in the URL, so no IDOR.
        return self.request.user
