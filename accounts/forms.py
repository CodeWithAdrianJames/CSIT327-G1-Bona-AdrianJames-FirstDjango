from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class BootstrapFormMixin:
    """Apply the right Bootstrap 5 class to every widget based on its type."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.CheckboxSelectMultiple)):
                css = "form-check-input"
            elif isinstance(widget, forms.Select):  # also covers SelectMultiple
                css = "form-select"
            else:
                css = "form-control"
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css}".strip()


class BootstrapAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "course")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "course")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email:
            taken = CustomUser.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if taken.exists():
                raise forms.ValidationError("This email address is already in use.")
        return email
