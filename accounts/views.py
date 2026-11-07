from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm, ProfileUpdateForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully! Please log in.")
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "registration/profile_form.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        # Always the logged-in user; no pk in the URL, so no IDOR.
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been updated successfully!")
        return response
